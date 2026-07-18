import json

class ConfigError(Exception):
    pass

def load_config(path):
    try:
        with open(path) as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f'Файл конфига не найден {path}') from e
    except json.JSONDecodeError as e:
        raise ConfigError(f'Файл конфига невалидный: {path}') from e