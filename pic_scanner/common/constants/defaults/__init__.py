from .dirs import *
from .files import *


# Here a list of names imported from each module:
__all__ = [
        'FILE_SYSTEM_DEFAULTS',
        ]


DEFAULT_DIRS = {
        'backup': DEFAULT_BACKUP_DIR,
        'cache': PROG_DIRS.user_cache_path,
        'config': PROG_DIRS.user_config_path,
        'data': PROG_DIRS.user_data_path,
        'pictures': PROG_DIRS.user_pictures_path,
        'temp': TEMP_DIR,
        }


DEFAULT_FILES = {
        'cache': CACHE_FILE_PATH,
        'config': CONFIG_FILE_PATH,
        'history': HISTORY_FILE_PATH,

        }


FILE_SYSTEM_DEFAULTS = {
        'dirs': DEFAULT_DIRS,
        'files': DEFAULT_FILES,
        }
