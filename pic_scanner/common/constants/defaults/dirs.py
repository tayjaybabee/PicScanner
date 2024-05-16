from platformdirs import PlatformDirs

from pic_scanner.common.__about__ import PROG_NAME, AUTHOR


__all__ = [
        'DEFAULT_BACKUP_DIR',
        'PROG_DIRS',
        'TEMP_DIR',
    ]


# ----- Constants START -----

PROG_DIRS = PlatformDirs(appname=PROG_NAME, appauthor=AUTHOR)

DEFAULT_BACKUP_DIR = PROG_DIRS.user_data_path / 'backups'

TEMP_DIR = PROG_DIRS.user_cache_path / 'temp'
