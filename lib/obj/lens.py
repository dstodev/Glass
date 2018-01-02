import sys
import typing

from lib.obj.glass import Delegate


class Lens(Delegate):
    """Example Delegate class.
    Provides information about called events if registered."""

    def modify_handler(self, handler: typing.Callable) -> typing.Callable:
        async def modifier(*args):
            print("Event '{}' invoked! Calling handler '{}' in module '{}'!"
                  .format(self.event, handler.__name__, handler.__module__), file=sys.stderr)
            await handler(*args)

        return modifier
