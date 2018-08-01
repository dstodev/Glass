import sys
import typing

from discord import Client

from lib.util.singleton import Singleton


class Delegate:
    __slots__ = ("event", "fire", "meta")

    def __init__(self, event: str, fire: callable, meta: dict):
        self.event = event
        self.fire = fire
        self.meta = meta

    def __setattr__(self, key, value):
        """To set items using delegate.key = value"""
        if key in self.__slots__:
            object.__setattr__(self, key, value)
        else:
            self.meta[key] = value

    def __getattr__(self, item):
        """To access items using delegate.key"""
        return self.meta[item]

    def __setitem__(self, key, value):
        """To set items using delegate[key] = value"""
        self.meta[key] = value

    def __getitem__(self, item):
        """To access items using delegate[key]"""
        return self.meta[item]


class Glass(Client, metaclass=Singleton):
    __slots__ = {"handlers", "delegates"}

    def __init__(self):
        super().__init__()

        self.handlers = {}
        self.delegates = {}

    def _handler(self, name: str) -> typing.Callable:
        handlers = self.handlers[name]

        async def handle(*args, **kwargs) -> None:
            for handler in handlers:
                try:
                    await handler.fire(*args, **kwargs)
                except Exception as e:
                    print(e, file=sys.stderr)

        handle.__name__ = name
        return handle

    def run(self, *args, **kwargs):
        """Register all events and start Glass."""

        # Mutate all events according to the registered mutators
        for event, mutators in self.delegates.items():
            for mutate in mutators:
                self.handlers[event] = [mutate(handler) for handler in self.handlers[event]]

        # Register all events
        for event in self.handlers:
            super().event(self._handler(event))
        # [super().event(self._handler(event)) for event in self.handlers]

        # Start Glass
        super().run(*args, **kwargs)

    def register_event(self, event: str, f: typing.Callable, **kwargs) -> None:
        """Register the given function as a handler of the given event."""

        # Add event handler list if it doesn't exist yet
        if event not in self.handlers:
            self.handlers[event] = []

        # Attach extra data to the handler
        context = Delegate(event, f, kwargs)

        # context = types.SimpleNamespace(**kwargs)
        # context.event = event
        # context.fire = f

        # Add handler to event handler list
        self.handlers[event].append(context)

    def decorate_event(self, event: str, **kwargs) -> typing.Callable:
        """Discord event registration decorator."""

        def dec(f: typing.Callable):
            self.register_event(event, f, **kwargs)

        return dec

    def register_delegate(self, event: str, f: typing.Callable) -> None:
        """Register the given function as a mutator of the given event."""

        if event not in self.delegates:
            self.delegates[event] = []

        self.delegates[event].append(f)

    def decorate_delegate(self, event: str) -> typing.Callable:
        """Discord event mutation decorator."""

        def dec(f: typing.Callable):
            self.register_delegate(event, f)

        return dec
