from inspyre_toolbox.syntactic_sweets.properties import validate_type
import PySimpleGUI as psg

from .blueprint import BluePrint
from ..template import Window
from pic_scanner.helpers.locks import flag_lock


class MainWindow(Window):

    class EventHandler:
        def __init__(self, window):
            self.window = window
            self.__last_index = 0

        def __call__(self, event, values):
            if event in [psg.WIN_CLOSED, 'EXIT_BUTTON', None]:
                self.window.close()
            elif event in ['NEXT_BUTTON', 'MouseWheel:Down', 'Down:40', 'Next:34']:
                self.window.file_index += 1
            elif event in ['PREV_BUTTON', 'MouseWheel:Up', 'Up:38', 'Prior:33']:
                self.window.file_index -= 1

        def check_index(self):
            if self.window.file_index != self.__last_index:
                self.__last_index = self.window.file_index
                self.window.blueprint.file_column.change_image(self.window.files[self.window.file_index])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = False

        self.__event_handler = self.EventHandler(self)

    @property
    def file_cursor(self):
        return self.blueprint.file_collection_cursor

    @property
    def files(self):
        return self.blueprint.left_column.file_collection.paths

    def build(self):
        """
        Builds the main window.

        Returns:
             PySimpleGUI.Window
        """
        print('Building main window')
        if not self.building and not self.is_built:
            print(f'`self.building = {self.building} | self.is_built = {self.is_built}`')
            with flag_lock(self, 'building'):
                self._window = psg.Window(
                        self.title,
                        self.layout,
                        return_keyboard_events=True,
                        finalize=True
                        )

            if self.window():
                self._built = True

    @property
    def active_image(self):
        return self.blueprint.file_column.file_path

    @property
    def file_index(self):
        return self.blueprint.file_collection_cursor.cursor

    @file_index.setter
    @validate_type(int)
    def file_index(self, new):

        old = self.file_index

        if new < 0:
            new = len(self.files) - 1
        elif new >= len(self.files):
            new = 0

        if old != new:
            self.blueprint.file_collection_cursor.set_cursor(new)
            self.blueprint.left_column.file_list_box.update(set_to_index=new)
        self.event_handler.check_index()
