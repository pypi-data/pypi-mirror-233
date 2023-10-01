from .nesting import NestKey


def key_to_identifier(key: NestKey) -> str:
    identifier = "_".join(key)
    assert identifier.isidentifier(), f"'{identifier}' is not an identifier"
    return identifier


def key_to_constant(key: NestKey) -> str:
    return key_to_identifier(key).upper()


def key_to_dictindex(key: NestKey) -> str:
    return "".join([f"[{name.__repr__()}]" for name in key])
