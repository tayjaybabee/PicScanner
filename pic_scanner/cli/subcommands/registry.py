import argparse
from pic_scanner.common.meta.constants import PROG_NAME, AUTHORS
from pic_scanner.common.meta import PROG_DESC


class Registry:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=PROG_NAME, description=PROG_DESC)
        self.subparsers = self.parser.add_subparsers(dest='command', help='Sub-Command Help')

    def register_subcommand(self, name, help_text, handler, arguments):
        subparser = self.subparsers.add_parser(name, help=help_text)
        for arg, params in arguments.items():
            subparser.add_argument(arg, **params)
        subparser.set_defaults(func=handler)


REGISTRY = Registry()
