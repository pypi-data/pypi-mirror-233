import argparse
from argparse import Namespace

from .nesting import nest_dict, key_to_identifier, Config

ARG_PREFIX = "--"
ARG_CONFIG_PATH = "config_path"


def get_config_path(
    arg_prefix: str = ARG_PREFIX,
    arg_config_path: str = ARG_CONFIG_PATH,
) -> tuple[Namespace, list[str]]:
    parser = argparse.ArgumentParser()

    argument = arg_prefix + arg_config_path

    parser.add_argument(
        argument,
        required=True,
        type=str,
        help="Path to config file of experiment",
    )

    return parser.parse_known_args()


def askfor_config_path(
    path_config: str,
    arg_prefix: str = ARG_PREFIX,
    arg_config_path: str = ARG_CONFIG_PATH,
) -> tuple[Namespace, list[str]]:
    parser = argparse.ArgumentParser()

    argument = arg_prefix + arg_config_path

    parser.add_argument(
        argument,
        nargs="?",
        const=path_config,
        type=str,
        help="Path to config file of experiment",
    )

    return parser.parse_known_args()


def get_args(
    config: Config,
    rest: list[str],
    arg_prefix: str = ARG_PREFIX,
) -> Namespace:
    parser = argparse.ArgumentParser()

    config_nest = nest_dict(config)
    config = {key_to_identifier(key): value for key, value in config_nest.items()}

    for arg_key, value in config.items():
        argument = arg_prefix + arg_key

        if isinstance(value, bool):
            parser.add_argument(
                argument,
                required=False,
                action=argparse.BooleanOptionalAction,
            )

        else:
            parser.add_argument(
                argument,
                required=False,
                type=value.__class__,
            )

    args = parser.parse_args(rest)

    for key, value in args.__dict__.items():
        if not value is None:
            config.update({key: value})

    return Namespace(**config)
