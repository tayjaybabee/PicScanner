import importlib
import os
import pkgutil
from pic_scanner.cli.subcommands.registry import REGISTRY


def load_modules():
    package_dir = os.path.join(os.path.dirname(__file__), '../cli/subcommands/community')

    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        importlib.import_module(f'pic_scanner.cli.subcommands.community.{module_name}')


def main():
    # Load core modules
    import pic_scanner.cli.subcommands
