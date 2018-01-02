import typing

from lib.obj.glass import Delegate


class Lens(Delegate):
    """Example Delegate class.
    Provides information about called events if registered."""

    def modify_handler(self, handler: typing.Callable):
        async def wrap(*args):
            print("Event '{}' invoked! Calling handler '{}' in module '{}'!"
                  .format(self.event, handler.__name__, handler.__module__))
            await handler(*args)

        return wrap
