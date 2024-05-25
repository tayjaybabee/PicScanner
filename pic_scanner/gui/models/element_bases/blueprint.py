from pic_scanner.gui.models.element_bases.metas import AutoBuildMeta, abstractmethod


class BaseBlueprint(metaclass=AutoBuildMeta):

    def __init__(self, auto_build=False):
        self._building = False
        self.__built = False
        self._layout = []
        self.__auto_build = auto_build if isinstance(auto_build, bool) else False

    @property
    def auto_build(self):
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, value):
        raise NotImplementedError('The `auto_build` attribute is read-only.')

    @property
    def building(self):
        return self._building

    @building.deleter
    def building(self):
        self._building = False

    @property
    def _built(self):
        return self.__built

    @_built.setter
    def _built(self, new):
        self.__built = new

    @property
    def is_built(self):
        return self._built

    @property
    def layout(self):
        return self._layout

    @abstractmethod
    def build(self):
        pass
