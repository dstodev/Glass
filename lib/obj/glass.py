import sys
import typing

from discord import Client

from lib.obj.singleton import Singleton


class Delegate:
    """Handles any single event."""

    override_warning = True

    def __init__(self, event: str, owner: "Glass"):
        self.event = event
        self.owner = owner
        self.handlers = []

    @staticmethod
    def _handler(event: str, handlers: typing.List[typing.Callable]) -> typing.Callable:
        """Implements a Discord event handler factory."""

        async def handle(*args, **kwargs) -> None:
            for handler in handlers:
                try:
                    await handler(*args, **kwargs)
                except Exception as e:
                    print(e, file=sys.stderr)

        handle.__name__ = event
        return handle

    def confirm(self):
        """Confirm event placement, register all given handlers."""

        decorated = []
        for handler in self.handlers:
            handler = self.modify_handler(handler)
            decorated.append(handler)

        super(Glass, self.owner).event(self._handler(self.event, decorated))

    def modify_handler(self, handler: typing.Callable) -> typing.Callable:
        """Modify the given handler to change how this delegate uses the handler.
        Must return an asynchronous (awaitable) callable."""

        if type(self) is not Delegate and self.override_warning:
            print("Subclass '{}' of class 'Delegate' should override method 'modify_handler'!"
                  .format(self.__class__.__name__), file=sys.stderr)
            self.override_warning = False

        return handler


class Glass(Client, metaclass=Singleton):
    def __init__(self):
        super().__init__()

        self.delegates = {}  # type: typing.Dict[str, Delegate]

    def run(self, *args, **kwargs):
        """Confirm Delegate event placement and start Glass."""

        # Finalize all delegate handlers
        for delegate in self.delegates.values():
            delegate.confirm()

        super().run(*args, **kwargs)

    def register_delegate(self, event: str, delegate: typing.Type[Delegate]):
        """Register a delegate class to handler a specific event."""

        delegate = delegate(event, self)

        if type(delegate) is Delegate:
            raise ValueError("parameter 'delegate' must be subclass of class 'Delegate'!")
        else:
            if event in self.delegates:
                if type(self.delegates[event] is Delegate):
                    handlers = self.delegates[event].handlers
                    delegate.handlers.extend(handlers)
                else:
                    raise ValueError("Delegate for '{}' already exists!".format(event))

            self.delegates[event] = delegate

    def register_event(self, event: str, handler: typing.Callable) -> None:
        """Register the given function as a handler of the given event."""

        if event not in self.delegates:
            self.delegates[event] = Delegate(event, self)

        self.delegates[event].handlers.append(handler)

    def decorate_event(self, event: str) -> typing.Callable:
        """Discord event registration decorator."""

        def wrap(f: typing.Callable):
            self.register_event(event, f)

        return wrap
