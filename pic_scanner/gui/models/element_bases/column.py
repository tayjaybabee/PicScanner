import PySimpleGUI as psg

from pic_scanner.helpers.properties import FrozenProperty, freeze_property
from pic_scanner.gui.models.element_bases.metas import AutoBuildMeta, abstractmethod


@freeze_property
class Column(metaclass=AutoBuildMeta):
    column_key = FrozenProperty('column_key', allowed_types=str)

    def __init__(self, column_key: str, auto_build=False):
        self._building = False
        self.__column = None
        self.column_key = column_key
        self.__auto_build = auto_build
        self.__built = False
        self.__layout = []

    @property
    def auto_build(self):
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, value):
        raise NotImplementedError('The `auto_build` attribute is read-only.')

    @abstractmethod
    def build(self):
        pass

    @property
    def building(self):
        return self._building

    @property
    def _built(self):
        return self.__built

    @_built.setter
    def _built(self, new):
        self.__built = new

    @property
    def column(self):
        if self.layout and self.building and not self.is_built and self.__column is None:
            self.__column = psg.Column(self.layout, key=self.column_key)
        return self.__column

    @property
    def _column(self):
        return self.__column

    @_column.setter
    def _column(self, new):
        self.__column = new

    @property
    def layout(self):
        return self.__layout

    @property
    def _layout(self):
        return self.__layout

    @_layout.setter
    def _layout(self, new):
        self.__layout = new

    @property
    def is_built(self):
        return bool(self.layout)
