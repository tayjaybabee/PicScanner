# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:11:16 2024

@author: tayja
"""
from abc import ABCMeta, abstractmethod
import PySimpleGUI as psg
from inspy_logger import InspyLogger, Loggable
from time import sleep
from pic_scanner.helpers import is_class

from typing import Optional, Union

from pic_scanner.gui.models.element_bases.metas import AutoBuildRunMeta


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


class Window(Loggable, metaclass=AutoBuildRunMeta):

    def __init__(
            self,
            auto_build=False,
            auto_run=False,
            title=None,
            blueprint: Optional["pic_scanner.BluePrint"] = None,
            blueprint_args: Optional[dict] = None
            ):
        super().__init__(parent_log_device=PROG_LOGGER)

        self._auto_build = auto_build
        self._auto_run = auto_run
        self._building = False
        self.__built = False
        self.__event_handler = self.EventHandler(self)
        self.__layout = None
        self._running = False
        self._title = None
        self._window = None

        self.title = title or 'Test Program'

        if self.auto_run and not self.auto_build:
            raise ValueError('Auto-run cannot be enabled without auto-build')

        if blueprint is not None:
            if is_class(blueprint):

                self._blueprint = blueprint(**blueprint_args) if blueprint_args else blueprint()
            else:
                self._blueprint = blueprint

            self.__layout = self._blueprint.layout

        #if self.auto_build:
        #    print('Auto-building window')
        #    self.build()
        #    if self.auto_run:
        #        print('Auto-running window')
        #        self.run()

    print('Window instance created!')

    @property
    def blueprint(self):
        return self._blueprint

    @abstractmethod
    def build(self):
        """
        Builds the window.

        Returns:
            None
        """
        pass

    @property
    def event_handler(self):
        return self.__event_handler

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

        if not self.window or not self.is_built:
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

                focus_forced = True

            self.event_handler(event, values)

    @property
    def auto_build(self):
        """
        Returns the value of the `auto_build` attribute.

        Returns:
            bool:
                The value of the `auto_build` attribute.
        """
        return self._auto_build

    @property
    def auto_run(self):
        """
        Returns the value of the `auto_run` attribute.

        Returns:
            bool:
                The value of the `auto_run` attribute.
        """
        return self._auto_run

    @property
    def is_built(self):
        """
        Returns the value of the `built` attribute.

        Returns:
            bool:
                The value of the `built` attribute.
        """
        return self._built

    @property
    def building(self):
        """
        Returns the value of the `building` attribute.

        Returns:
            bool:
                The value of the `building` attribute.
        """
        return self._building

    @is_built.deleter
    def is_built(self):
        """
        Deletes the `built` attribute.

        Returns:
            None
        """
        if not self.running and not self.window:
            self._built = False

    @property
    def _built(self):
        return self.__built

    @_built.setter
    def _built(self, new):
        self.__built = new

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

    @layout.setter
    def layout(self, new):
        if not isinstance(new, list):
            raise TypeError('Layout must be a list of lists of PySimpleGUI elements!')

        self.__layout = new

    @property
    def running(self):
        """
        Returns the value of the `running` attribute.

        Returns:
            bool:
                The value of the `running` attribute.
        """
        return self._running

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

        self._running = new

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

    @property
    def _window(self):
        return self.__window

    @_window.setter
    def _window(self, new):
        self.__window = new
