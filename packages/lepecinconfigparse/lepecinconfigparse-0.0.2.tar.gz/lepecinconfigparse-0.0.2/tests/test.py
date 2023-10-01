from src import ConfigManager, JsonConfigLoader

import pathlib

path_config = (pathlib.Path(__file__).parent / "config.json").__str__()
path_internal = (pathlib.Path(__file__).parent / "internal-config.json").__str__()
path_constants = (pathlib.Path(__file__).parent / "constants.py").__str__()


manager = ConfigManager(
    path_internal,
    JsonConfigLoader(),
)

if __name__ == "__main__":
    manager.set_internal_config(path_config)
    manager.save_internal_constants(path_constants)
    globals().update(manager.load_internal_config())

    print(HELLO_HEY)
