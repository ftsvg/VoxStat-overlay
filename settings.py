from overlay.cfg import config

class Settings:
    BASE_URL = "https://api.voxyl.net"

    @classmethod
    def get_api_key(cls) -> str | None:
        return config.api_key

    @classmethod
    def validate(cls) -> None:
        if not cls.get_api_key():
            raise RuntimeError("API key has not been set")