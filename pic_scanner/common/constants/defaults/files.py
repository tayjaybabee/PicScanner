from .dirs import PROG_DIRS


__all__ = [
        'CONFIG_FILE_NAME',
        'CONFIG_FILE_PATH',
        'CACHE_FILE_NAME',
        'CACHE_FILE_PATH',
        'DEFAULT_BACKUP_EXTENSION',
        'HISTORY_FILE_NAME',
        'HISTORY_FILE_PATH',
    ]


CONFIG_FILE_NAME = 'config.ini'
CONFIG_FILE_PATH = PROG_DIRS.user_config_path / CONFIG_FILE_NAME

CACHE_FILE_NAME = 'cache.json'

CACHE_FILE_PATH = PROG_DIRS.user_cache_path / CACHE_FILE_NAME

DEFAULT_BACKUP_EXTENSION = '.bak'

HISTORY_FILE_NAME = 'history.json'
HISTORY_FILE_PATH = PROG_DIRS.user_data_path / HISTORY_FILE_NAME
