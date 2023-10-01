NAME_CONFIG = "config"
NAME_NAMESPACE = "args"

from .nesting import NestConfig, Config
from .keyconvert import (
    key_to_constant,
    key_to_dictindex,
    key_to_identifier,
)


def gen_getdict(
    nest_dict: NestConfig,
) -> Config:
    return {key_to_constant(key): value for key, value in nest_dict.items()}


def gen_setdict(
    nest_dict: NestConfig,
    name_config: str = NAME_CONFIG,
    name_namespace: str = NAME_NAMESPACE,
) -> list[str]:
    lines: list[str] = []
    for key in nest_dict:
        name_identifier = name_namespace + "." + key_to_identifier(key)
        name_dict = name_config + key_to_dictindex(key)
        lines.append(f"{name_dict} = {name_identifier}")

    return lines


def gen_constants(nest_dict: NestConfig) -> list[str]:
    lines: list[str] = []
    for key, value in nest_dict.items():
        name_constant = key_to_constant(key)
        name_data = value.__class__.__name__
        lines.append(f"{name_constant}: {name_data}" + "\n")

    return lines
