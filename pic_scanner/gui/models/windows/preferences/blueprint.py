from pic_scanner.gui.models.element_bases.blueprint import BaseBlueprint
from pic_scanner.helpers.locks import flag_lock


class BluePrint(BaseBlueprint):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__gui_settings_tab = None


    @property
    def gui_settings_tab(self):
        return self.__gui_settings_tab

    def build(self):
        if not self._built and not self._building:
            with flag_lock:
                self._building = True
                self._layout = [
                    self.gui_settings_tab
                ]
                self._built = True
                self._building = False
