from typing import Any

Config = dict[str, Any]
NestKey = tuple[str, ...]
NestConfig = dict[NestKey, Any]


def nest_dict(
    config: Config,
    keys: NestKey = (),
) -> NestConfig:
    """
    Function for converting a config object into a flat
    dictionary with nested keys.

    Inputs:
    - config: dict[str, Any]; A config object with nested configs in it.
    - keys: tuple[str, ...]; A nested key, a tuple of keys with which each key
    in the output dictionary will start.

    Outputs:
    - new_dict: dict[tuple[str, ...], Any]; The flattened verion of the dictionary
    with keys flattened as nested keys, orders so as to preserve the nested nature
    of the original config.
    """

    new_dict = {}
    for key, value in config.items():
        assert isinstance(key, str), f"keys must be strings, get {key}"

        if not isinstance(value, dict):
            new_dict.update({keys + (key,): value})
        else:
            new_dict.update(nest_dict(value, keys + (key,)))
    return new_dict
