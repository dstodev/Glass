import typing

from discord import Client

from lib.obj.singleton import Singleton


class Glass(Client, metaclass=Singleton):
    def __init__(self):
        super().__init__()

        self.handlers = {}

    def _handler(self, event: str) -> typing.Callable:
        """Implements a Discord event handler factory."""
        handlers = self.handlers[event]

        async def handle(*args, **kwargs) -> None:
            for handler in handlers:
                try:
                    await handler(*args, **kwargs)
                except Exception as e:
                    print(e)

        handle.__name__ = event
        return handle

    def register_event(self, event: str, f: typing.Callable) -> None:
        """Register the given function as a handler of the given event."""

        if event not in self.handlers:
            self.handlers[event] = []
            super().event(self._handler(event))

        self.handlers[event].append(f)

    def decorate_event(self, event: str) -> typing.Callable:
        """Discord event registration decorator."""

        def wrap(f: typing.Callable):
            self.register_event(event, f)

        return wrap
