from enum import Enum


class VoxylApiEndpoint(Enum):
    PLAYER_INFO = "player/info/{uuid}"
    PLAYER_OVERALL = "player/stats/overall/{uuid}"
    PLAYER_STATS = "player/stats/game/{uuid}"
    PLAYER_GUILD = "player/guild/{uuid}"