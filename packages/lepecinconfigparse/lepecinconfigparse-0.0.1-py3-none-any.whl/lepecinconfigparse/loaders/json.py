import json
from typing import Self

from .loader import Config, ConfigLoader


class JsonConfigLoader(ConfigLoader):
    def load(self: Self, config_path: str) -> Config:
        with open(config_path, "r") as file:
            config: Config = json.loads(file.read())
        return config

    def save(self: Self, config_path: str, config: Config):
        with open(config_path, "w") as file:
            file.write(json.dumps(config))
