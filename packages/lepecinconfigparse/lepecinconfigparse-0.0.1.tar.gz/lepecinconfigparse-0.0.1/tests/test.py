from seelconfigparse import ConfigManager, ConfigLoader

import pathlib


path_internal = (pathlib.Path(__file__).parent / "internal-config.json").__str__()
path_constants = (pathlib.Path(__file__).parent / "constants.py").__str__()


manager = ConfigManager(
    path_internal,
    ConfigLoader(),
)


if __name__ == "__main__":
    manager.set_internal_config()
    manager.save_internal_constants(path_constants)
    globals().update(manager.load_internal_config())

    print(HELLO_HEY)
