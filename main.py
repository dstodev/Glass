import importlib
import pathlib
import sys

from lib.obj.arbiter import Arbiter
from lib.obj.glass import Glass
from lib.obj.lens import Lens
from secret.auth import TOKEN

if __name__ == "__main__":

    module_dir = "modules"

    # Get Glass instance (note that Glass is a singleton)
    glass = Glass()

    # Note that if a module requires the use of a specific delegate,
    # that delegate must be registered before the module!
    glass.register_delegate("on_ready", Lens)
    glass.register_delegate("on_message", Arbiter)

    # Import all modules so that they can register their events
    modules = [f.stem for f in pathlib.Path(module_dir).iterdir() if f.is_file()]
    for module in modules:
        importlib.import_module("{}.{}".format(module_dir, module))


    @glass.decorate_event("on_ready")
    async def initialize():
        # Example registration of an event handler.
        # Also indicates that all modules were successfully imported.
        print("Glass online!", file=sys.stderr)


    # Start Glass!
    glass.run(TOKEN)
