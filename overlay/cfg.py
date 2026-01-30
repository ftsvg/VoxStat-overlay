import json
import sys
from pathlib import Path


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


CONFIG_PATH = app_dir() / "config.json"


class Config:
    def __init__(self):
        self.log_path = None
        self.api_key = None
        self.load()

    def load(self):
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text())
            self.log_path = data.get("log_path")
            self.api_key = data.get("api_key")

    def save(self):
        CONFIG_PATH.write_text(json.dumps({
            "log_path": self.log_path,
            "api_key": self.api_key,
        }, indent=2))


config = Config()