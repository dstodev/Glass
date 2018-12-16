import argparse
import sys
import logging

from lib import PATH_DEFAULT_MODULES
from lib.obj.glass import Glass
from lib.util import modules

if __name__ == "__main__":
    # Get CLI parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", help="Enables verbose output")
    parser.add_argument("token", help="Server token for Glass")
    parser.add_argument("-m", "--module_dir", default="./modules", help="Directory for Glass modules")
    space = parser.parse_args()  # type: argparse.Namespace

    # Set up logging
    cfg_format = "%(asctime)s [%(levelname)-8s @ %(filename)s\t] \'%(message)s\'"
    cfg_datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=cfg_format, datefmt=cfg_datefmt, level=logging.INFO)

    # Get Glass instance (note that Glass is a singleton)
    glass = Glass()

    # Import all modules so that they can register their event
    modules.import_from_path(PATH_DEFAULT_MODULES, verbose=space.verbose)
    modules.import_from_path(space.module_dir, verbose=space.verbose)


    @glass.decorate_event("on_ready", hello="world!")
    async def initialize():
        # Example registration of an event handler.
        # Also indicates that all modules were successfully imported.
        logging.getLogger(__name__).info("Glass online!")


    # Start Glass!
    glass.run(space.token)
