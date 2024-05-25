from ..common.constants import *
from ..common.constants.defaults.dirs import PROG_DIRS
from inspy_logger import InspyLogger, LEVELS, Loggable


ROOT_LOGGER = InspyLogger(
        PROG_NAME,
        console_level='debug',
        file_level='debug',
        file_path=PROG_DIRS.user_data_path / 'logs' / 'pic_scanner.log',
        )

MAIN_MOD_LOGGER = ROOT_LOGGER.get_child('pic_scanner')
MOD_LOGGER = MAIN_MOD_LOGGER.get_child('log_engine')
