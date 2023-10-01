from typing import Self

from .argparsing import get_config_path, get_args, askfor_config_path
from .nesting import Config, gen_setdict, nest_dict, gen_getdict, gen_constants
from .loaders import ConfigLoader


class ConfigManager:
    """
    Class responsible for storing all variables and methods
    relevant to setting, saving and loading configuration files.
    """

    path_internal: str

    def __init__(
        self: Self,
        path_internal: str,
        config_loader: ConfigLoader,
    ) -> None:
        self.path_internal = path_internal
        self.config_loader = config_loader

    def load_config_from(self: Self, config_path: str) -> Config:
        return self.config_loader.load(config_path)

    def save_config_at(self: Self, internal_path: str, config: Config):
        self.config_loader.save(internal_path, config)

    def set_internal_config(self: Self, path_config: str | None = None):
        if path_config is None:
            args, rest = get_config_path()
        else:
            args, rest = askfor_config_path(path_config)

        config_path: str = args.config_path

        config = self.load_config_from(config_path)

        args = get_args(config, rest)

        lines = gen_setdict(nest_dict(config))
        for line in lines:
            exec(line)

        self.save_config_at(self.path_internal, config)

    def load_internal_config(self: Self) -> Config:
        config = self.load_config_from(self.path_internal)

        return gen_getdict(nest_dict(config))

    def save_internal_constants(self: Self, path_constants: str):
        config = self.load_config_from(self.path_internal)

        lines = gen_constants(nest_dict(config))
        with open(path_constants, "w") as file:
            file.writelines(lines)
