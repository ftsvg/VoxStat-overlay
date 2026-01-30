import asyncio
import re
from pathlib import Path
from mcfetch import Player

from api.helpers import PlayerInfo
from overlay.display import get_prestige_color, get_displayname
from overlay.cfg import config


PLAYER_REGEX = re.compile(r"Players in this game:\s*(.*)")


async def build_player_data(players):
    result = []

    for player in players:
        try:
            uuid = Player(player=player).uuid
            stats = await PlayerInfo.fetch(uuid)

            if not all(
                isinstance(x, dict)
                for x in (
                    stats.player_info,
                    stats.overall_stats,
                    stats.game_stats,
                )
            ):
                result.append((f"&e[Nicked] &7{player}", None))
                continue

            display_name = (
                get_prestige_color(stats.level)
                + get_displayname(player, stats.role)
            )

            result.append((display_name, stats))

        except Exception:
            result.append((f"&e[Nicked] &7{player}", None))

    return result


async def watch_log(overlay):
    file_pos = 0
    last_path: Path | None = None

    while True:
        await asyncio.sleep(0.3)

        if not config.log_path:
            continue

        path = Path(config.log_path)

        if not path.exists():
            continue

        if last_path != path:
            file_pos = path.stat().st_size
            last_path = path
            continue

        size = path.stat().st_size
        if size < file_pos:
            file_pos = 0

        with path.open("r", encoding="utf-8", errors="ignore") as f:
            f.seek(file_pos)
            lines = f.readlines()
            file_pos = f.tell()

        for line in lines:
            match = PLAYER_REGEX.search(line)
            if match:
                players = match.group(1).split()
                data = await build_player_data(players)
                overlay.signals.update_players.emit(data)
