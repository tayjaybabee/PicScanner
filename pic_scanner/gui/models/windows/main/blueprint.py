import PySimpleGUI as psg



class LeftColumn:
    def __init__(self, file_names, auto_build=False):
        self.__auto_build = None
        self.__layout = None
        self.__file_names = file_names

    @property
    def auto_build(self):
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, value):
        raise NotImplementedError('The `auto_build` attribute is read-only.')

    @property
    def built(self):
        return self.layout is not None and self.layout != []

    @property
    def file_names(self):
        return self.__file_names

    @property
    def file_num_display_elem(self):
        return psg.Text(
                f'File 1 of {}'
                )

    @property


    @property
    def layout(self):
        return self.__layout

    def build(self):
        if self.built:
            return self.layout
        if not self.built:
            self.__layout = [
                    [filename_display_elem ]
                    ]


class BluePrint:
    def __init__(self):
        self.__built = False
        self.__layout = None
