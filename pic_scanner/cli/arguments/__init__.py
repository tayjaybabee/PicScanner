from argparse import ArgumentParser

from pic_scanner.common.meta.version import parse_version
from pic_scanner.common.constants import PROG_NAME, AUTHORS
from pic_scanner.common.meta import PROG_DESC


class BaseSubCommandHandler:
    pass


class CommandHandler:
    def __init__(self, args):
        self.args = args
        self._handle_args()

    def _handle_args(self):
        if self.args.authors:
            self._display_authors()
        if self.args.description:
            self._display_description()

    def _display_authors(self):
        print('Authors:')
        for author, email in AUTHORS:
            print(f'{author} <{email}>')

    def _display_description(self):
        print(PROG_DESC)



class Parser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_args()

    def _add_args(self):
        self.add_argument(
                '-a', '--authors',
                action='store_true',
                help='Display the authors of the program.'
                )
        self.add_argument(
                '-d', '--description',
                action='store_true',
                help='Display the description of the program.'
                )
        self.add_argument(
                '-v', '--version',
                action='store_true',
                help='Display the version of the program.'
                )

        self.add_argument(
                '-V', '--full-version',
                action='store_true',
                help='Display the full version of the program.'
                )

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)
        CommandHandler(args)
        return args

    def register_subcommand(self, sub_command_handler: SubCommandHandler, *args, **kwargs):
        return self.add_subparsers(*args, **kwargs)
