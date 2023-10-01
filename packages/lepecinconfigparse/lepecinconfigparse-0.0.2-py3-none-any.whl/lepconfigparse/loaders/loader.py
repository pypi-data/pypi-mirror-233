from typing import Any, Self

Config = dict[str, Any]


class ConfigLoader:
    def load(self: Self, config_path: str) -> Config:
        print(f"Pretend load from {config_path}")
        return {"hello": {"hey": 2, "ho": 3, "yeet": {"halo": 9}}, "sup": 5}

    def save(self: Self, config_path: str, config: Config):
        print(f"Pretend saved to {config_path}")
