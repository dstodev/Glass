import typing

from discord import Client

from lib.util.singleton import Singleton


class Glass(Client, metaclass=Singleton):
    def __init__(self):
        super().__init__()

        self.handlers = {}

    def _handler(self, name: str) -> typing.Callable:
        handlers = self.handlers[name]

        async def handle(*args, **kwargs) -> None:
            for handler in handlers:
                await handler(*args, **kwargs)

        handle.__name__ = name
        return handle

    def run(self, *args, **kwargs):
        """Register all events and start Glass."""

        # Register all events
        for event in self.handlers:
            super().event(self._handler(event))
        # [super().event(self._handler(event)) for event in self.handlers]

        # Start Glass
        super().run(*args, **kwargs)

    def register_event(self, event: str, f: typing.Callable) -> None:
        """Register the given function as a handler of the given event."""

        # Add event handler list if it doesn't exist yet
        if event not in self.handlers:
            self.handlers[event] = []

        # Add handler to event handler list
        self.handlers[event].append(f)

    def decorate_event(self, event: str) -> typing.Callable:
        """Discord event registration decorator."""

        def dec(f: typing.Callable):
            self.register_event(event, f)

        return dec
