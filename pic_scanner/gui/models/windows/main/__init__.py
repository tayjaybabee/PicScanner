from inspyre_toolbox.syntactic_sweets.properties import validate_type
import PySimpleGUI as psg

from .blueprint import BluePrint
from ..template import Window
from pic_scanner.helpers.locks import flag_lock

from pathlib import Path
from pic_scanner.gui.models.windows import MOD_LOGGER as PARENT_LOGGER
from pic_scanner.log_engine import Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('main')



class MainWindow(Window, Loggable):

    class EventHandler(Loggable):
        def __init__(self, window):

            self.window = window
            super().__init__(parent_log_device=self.window.log_device)
            self.__last_index = None
            self.__announced_start = False

        def __call__(self, event, values):
            log_name = f'{self.log_device.name}:__call__'

            log = (
                    self.log_device.find_child_by_name(log_name)[0]
                ) if self.log_device.has_child(log_name) else self.create_child_logger()

            if not self.announced_start:
                log.debug('Starting event handler')
                self.__announced_start = True

            if self.window.running:

                if event in [psg.WIN_CLOSED, 'EXIT_BUTTON', None]:
                    log.debug('Received close request')
                    self.window.close()
                    log.debug('Window closed, exiting event handler')
                    return

                if 'TIMEOUT' not in event:
                    log.debug(f'Handling event: {event}')

                if event in ['NEXT_BUTTON', 'MouseWheel:Down', 'Down:40', 'Next:34']:
                    log.debug('Next file event')
                    self.window.file_index += 1
                    log.debug(f'New index: {self.window.file_index}')

                elif event in ['PREV_BUTTON', 'MouseWheel:Up', 'Up:38', 'Prior:33']:
                    log.debug('Prev file event')
                    self.window.file_index -= 1
                    log.debug(f'New index: {self.window.file_index}')

                elif event in ['REMOVE_BUTTON']:
                    log.debug('Remove event')

                    log.debug(f'Current file: {self.window.active_image}')

                    # Remove the current file from the collection
                    self.window.blueprint.file_collection_cursor.remove_current()

                    # Reprocess the files in the collection
                    self.window.blueprint.file_collection_cursor.collection.reprocess_files()

                    # Get the new index
                    self.window.blueprint.left_column.file_list_box.update(values=self.window.files)

                    # Set the new index
                    self.window.blueprint.left_column.file_list_box.update(set_to_index=self.window.file_index )

                elif event == 'FILE_LIST_BOX':
                    log.debug(f'File list box event: {values[event][0]}')

                    self.window.file_index = values[event][0]

                elif 'TIMEOUT' not in event:
                    log.warning(f'Unhandled event: {event}, {values}')

                self.window.check_prev_button()
                self.window.check_remove_button()

        @property
        def announced_start(self):
            return self.__announced_start

    def check_index(self):
        if self.file_index != self.__last_index:
            self.__last_index = self.file_index
            #self.blueprint.file_column.change_image(self.files[self.file_index])

    def check_prev_button(self):
        if self.file_index == 0:
            self.blueprint.left_column.prev_button.update(disabled=True)
        else:
            self.blueprint.left_column.prev_button.update(disabled=False)

    def check_remove_button(self):
        """
        Checks if the remove button should be enabled or disabled.

        If no image is selected, the button is disabled. If an image is selected, the button is
        enabled.

        Returns:
            None
        """
        log_name = f'{self.log_device.name}:check_remove_button'

        log = (
                self.log_device.find_child_by_name(log_name)[0]
            ) if self.log_device.has_child(log_name) else self.create_child_logger()

        if self.file_index is not None and len(self.files) > 0:
            if self.__remove_button_state is False:
                log.debug('Index is not None and files are present, enabling remove button')
                self.__remove_button_state = True
                self.update_remove_button_state(True)

        elif self.__remove_button_state:
            log.debug('Index is None or no files are present')
            self.__remove_button_state = False
            self.update_remove_button_state(False)


    def __init__(self, *args, **kwargs):
        Window.__init__(self, *args, **kwargs)
        Loggable.__init__(self, parent_log_device=MOD_LOGGER)
        self.__running = False
        self._setting_index = False
        self.__last_index = None
        self.__remove_button_state = False
        self.__prev_button_state = False

        self.__event_handler = self.EventHandler(self)

        log = self.log_device

        log.debug('MainWindow initialized')

    @property
    def event_handler(self):
        return self.__event_handler

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
        log = self.create_child_logger()
        log.debug('Building main window')
        if not self.building and not self.is_built:
            log.debug(f'`self.building = {self.building} | self.is_built = {self.is_built}`')
            with flag_lock(self, 'building'):
                self._window = psg.Window(
                        self.title,
                        self.layout,
                        return_keyboard_events=True,
                        finalize=True
                        )
                log.debug(f'Window built: {hex(id(self.window))}')

                self.__file_collection_cursor = self.blueprint.file_collection_cursor

            if self.window():

                self._built = True

    def close(self):
        """
        Closes the window.

        This method is called when the window is closed by the user or by the program. It facilitates
        the safe closing of the window and the logging of the event. It also sets the `running` flag
        to `False`.

        Returns:
            None
        """
        log = self.create_child_logger()

        if self.window and self.running:
            log.debug('Closing window')
            self.running = False
            log.debug('Changed running flag to `False`')
            self.window.close()
            log.debug('Window closed')
            self._window = None

    def remove_current_file(self):
        cursor = self.window.blueprint.file_collection_cursor
        cursor.remove_current()
        cursor.collection.reprocess_files()

        new_index = cursor.cursor if cursor.cursor < len(self.window.files) else len(self.window.files) - 1

        self.window.file_index = new_index
        self.window.blueprint.left_column.file_list_box.update(set_to_index=new_index)
        self.check_index()
        self.check_prev_button()
        self.check_remove_button()

    def update_remove_button_state(self, state: bool):
        """
        Updates the state of the remove button.

        This method takes a boolean value and sets the 'disabled' state of the remove button to the
        opposite of that value. If this value is `True`, the button is enabled. If the value is
        `False`, the button is disabled. This method is used to enable or disable the remove button
        based on the state of the window. If no image is selected, this method will ensure the button
        remains disabled. If the user has an image selected, this method will enable the `Remove`
        button.

        Parameters:
            state (bool):
                The state to set the button to.

        Returns:
            None
        """
        self.blueprint.left_column.remove_button.update(disabled=not state)


    @property
    def active_image(self):
        return self.blueprint.file_column.file_path

    @property
    def file_index(self):
        return self.blueprint.file_collection_cursor.cursor

    @file_index.setter
    @validate_type(
            int, str, Path
            )
    def file_index(self, new):

        if isinstance(new, (str, Path)):
            new = self.files.index(new)

        old = self.file_index

        if new < 0:
            new = len(self.files) - 1
        elif new >= len(self.files):
            new = 0

        if not self.setting_index:
            with flag_lock(self, 'setting_index'):
                self.blueprint.file_collection_cursor.set_cursor(new)
                self.blueprint.left_column.file_list_box.update(set_to_index=new)
                self.check_index()

    @property
    def setting_index(self) -> bool:
        return self._setting_index
