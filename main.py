import importlib
import pathlib
import sys

from lib.obj.glass import Glass
from secret.auth import TOKEN

if __name__ == "__main__":

    # Get Glass instance (note that Glass is a singleton)
    glass = Glass()

    # Import all modules so that they can register their events
    modules = [f.stem for f in pathlib.Path("modules").iterdir() if f.is_file()]
    for mod in modules:
        importlib.import_module("modules.{}".format(mod))


    # Example registration of an event handler, also indicates that all modules were successfully imported
    @glass.decorate_event("on_ready")
    async def initialize():
        print("Glass online!", file=sys.stderr)


    # Start Glass!
    glass.run(TOKEN)
