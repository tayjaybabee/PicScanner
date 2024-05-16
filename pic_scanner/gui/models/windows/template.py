# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:11:16 2024

@author: tayja
"""

import PySimpleGUI as psg
from inspy_logger import InspyLogger, Loggable
from time import sleep

PROG_LOGGER = InspyLogger(name='Program Logger', console_level='debug')

PROG_LOGGER.set_level(console_level='info')


def event_handler(event, values, window):
    log = PROG_LOGGER.get_child()
    log.debug(f'Received {event}')
    if (
            event == 'EXIT_BUTTON' or
            event == psg.WIN_CLOSED or
            event is None
    ) and window.running:
        log.debug('Received close request')
        window.close()


def layout():
    return [
            [psg.Button('Exit', key='EXIT_BUTTON')]
            ]


class Window(Loggable):

    def __init__(self, auto_build=False, auto_run=False, title=None, blueprint=None):
        super().__init__(parent_log_device=PROG_LOGGER)

        self.__auto_build = None
        self.__auto_run = None
        self.__built = False
        self.__event_handler = None
        self.__layout = None
        self.__running = False
        self.__title = None
        self.__window = None

        self.__auto_build = auto_build
        self.__auto_run = auto_run

        self.title = title or 'Test Program'

        if self.auto_run and not self.auto_build:
            raise ValueError('Auto-run cannot be enabled without auto-build')

        if blueprint is not None:
            self.__blueprint = blueprint
            self.__layout = blueprint.layout

        if self.auto_build:
            self.build()
            if self.auto_run:
                self.run()

    def build(self):
        """
        Builds the window.

        Returns:
            None
        """
        if self.built:
            raise ValueError('Window has already been built')

        self.__layout = layout()

        self.__window = psg.Window(self.title, self.layout)

        if self.window:
            self.__built = True
            self.window.finalize()

    def close(self):
        """
        Closes the window.

        Returns:
            None
        """
        self.create_child_logger()
        if self.window:
            if self.running:
                self.running = False
            if not self.window.was_closed():
                self.window.close()

    def run(self):
        """
        Runs the window.

        Returns:
            None
        """
        log = self.create_child_logger()

        if not self.window or not self.built:
            raise RuntimeError('You can not run a non-existant window!')

        self.running = True
        log.debug('Changed running flag to `True`')

        focus_forced = False

        while self.running:
            event, values = self.window.read(timeout=100)

            if not focus_forced:
                log.debug('Forcing focus on unfocused window!')
                self.window.force_focus()
                sleep(.3)
                log.debug('Focus forced.')

                force_focused = True

            event_handler(event, values, self)

    @property
    def auto_build(self):
        """
        Returns the value of the `auto_build` attribute.

        Returns:
            bool:
                The value of the `auto_build` attribute.
        """
        return self.__auto_build

    @property
    def auto_run(self):
        """
        Returns the value of the `auto_run` attribute.

        Returns:
            bool:
                The value of the `auto_run` attribute.
        """
        return self.__auto_run

    @property
    def blueprint(self):
        return self.__blueprint

    @property
    def built(self):
        """
        Returns the value of the `built` attribute.

        Returns:
            bool:
                The value of the `built` attribute.
        """
        return self.__built

    @built.deleter
    def built(self):
        """
        Deletes the `built` attribute.

        Returns:
            None
        """
        if not self.running and not self.window:
            self.__built = False

    @property
    def closed(self):
        """
        Returns the value of the `closed` attribute.

        Returns:
            bool:
                The value of the `closed` attribute.
        """
        return self.window.was_closed() if self.window else False

    @property
    def layout(self):
        """
        Returns the value of the `layout` attribute.

        Returns:
            list:
                The value of the `layout` attribute.

        """
        return self.__layout

    @property
    def running(self):
        """
        Returns the value of the `running` attribute.

        Returns:
            bool:
                The value of the `running` attribute.
        """
        return self.__running

    @running.setter
    def running(self, new):
        """
        Sets the value of the `running` attribute.

        Args:
            new (bool):
                The new value to set the `running` attribute to.

        Returns:
            None
        """
        if not isinstance(new, bool):
            raise TypeError(f'Invalid type ({type(new)}) for `Window.running`. Value must be a bool!')

        self.__running = new

    @property
    def title(self):
        return self.window.Title if self.window else self.__title

    @title.setter
    def title(self, new):
        if isinstance(new, str):
            if self.window and self.window.finalize_in_progress:
                self.window.set_title(new)

            self.__title = new

        else:
            raise TypeError('Title must be a string')

    @property
    def window(self):
        return self.__window


#if __name__ == '__main__':
#    window = Window(auto_build=True, auto_run=True)
