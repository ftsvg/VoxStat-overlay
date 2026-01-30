import asyncio
from typing import Any

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientError,
    ContentTypeError,
    InvalidURL,
    ServerTimeoutError,
)

from settings import Settings
from .errors import (
    APIError,
    BadRequestError,
    RateLimitError,
    UnexpectedStatusError,
)


class VoxylAPI:
    def __init__(self):
        self.base_url = Settings.BASE_URL
        self.session: ClientSession | None = None

    async def close(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def _make_request(
        self,
        session: ClientSession,
        endpoint: Any,
        **kwargs: Any,
    ) -> Any:
        api_key = Settings.get_api_key()
        if not api_key:
            raise RuntimeError("API key not set")

        url = f"{self.base_url}/{endpoint.value.format(**kwargs)}"
        params = {"api": api_key}
        params.update({k: v for k, v in kwargs.items() if v is not None})

        resp = await session.get(url, params=params)
        try:
            try:
                data = await resp.json(content_type=None)
            except Exception:
                data = await resp.text()

            if resp.status == 200:
                return data

            if resp.status == 400:
                raise BadRequestError()

            if resp.status == 429:
                raise RateLimitError()

            raise UnexpectedStatusError(
                f"Unexpected status {resp.status}: {data}"
            )
        finally:
            resp.release()

    async def make_request(
        self,
        endpoint: Any,
        *,
        retries: int = 3,
        retry_delay: int = 5,
        **kwargs: Any,
    ) -> Any:
        for attempt in range(retries + 1):
            try:
                if self.session is None:
                    self.session = ClientSession(
                        timeout=ClientTimeout(total=10)
                    )

                return await self._make_request(
                    self.session, endpoint, **kwargs
                )

            except RateLimitError:
                if attempt >= retries:
                    raise
                await asyncio.sleep(retry_delay)

            except (
                ClientError,
                ClientConnectorError,
                InvalidURL,
                ServerTimeoutError,
                ContentTypeError,
            ) as exc:
                if attempt >= retries:
                    raise APIError(str(exc)) from exc
                await asyncio.sleep(retry_delay)


API = VoxylAPI()
