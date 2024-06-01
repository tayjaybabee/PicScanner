from pic_scanner.log_engine import Loggable
from . import MOD_LOGGER as PARENT_LOGGER
from PySimpleGUI import Tab


MOD_LOGGER = PARENT_LOGGER.get_child('element_bases')


class TabSchematic(Loggable):
    """
    A class to act as a schematic for a PySimpleGUI Tab element.

    Properties:
        tab (Tab):
            The PySimpleGUI Tab element.

        layout (list):
            The layout of the Tab element.

        key (GUIElementKey)
    """
