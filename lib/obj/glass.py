import sys
import typing

from discord import Client

from lib.util.singleton import Singleton


class Delegate(metaclass=Singleton):
    """Handles any single event."""

    _override_warning = True  # Ensures 'modify_handler' warning only outputs once per delegate

    def __init__(self, event: str, owner: "Glass"):
        self.event = event
        self.owner = owner
        self.handlers = []

    @staticmethod
    def _handler(event: str, handlers: typing.List[typing.Callable]) -> typing.Callable:
        """Implements a Discord event handler builder."""

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

        if self._override_warning and type(self) is not Delegate:
            print("Subclass '{}' of class 'Delegate' should override method 'modify_handler'!"
                  .format(self.__class__.__name__), file=sys.stderr)
            self._override_warning = False

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

    def register_delegate(self, event: str, delegate: typing.Type[Delegate]) -> None:
        """Register a delegate class to handle a specific event."""

        # TODO: Use priority system for multiple delegates, persistent data object (dict) passed from highest to lowest
        # TODO: priorities

        delegate = delegate(event, self)

        if type(delegate) is Delegate:
            raise ValueError("Parameter 'delegate' must be subclass of class 'Delegate'!")
        else:
            # TODO: Duplicate check fails if Delegate class is not a singleton
            if event in self.delegates and self.delegates[event] is not delegate:
                # If currently using a default delegate, move handlers to the new delegate
                if type(self.delegates[event]) is Delegate:
                    handlers = self.delegates[event].handlers
                    delegate.handlers.extend(handlers)
                else:
                    # A non-default delegate already exists
                    raise ValueError("Delegate for '{}' already exists!".format(event))

            self.delegates[event] = delegate

    def get_delegate(self, event: str, type_assertion: typing.Type = None) -> typing.Union[None, Delegate]:
        """Returns the delegate for the given event, if one exists."""
        if event in self.delegates:
            if type_assertion and not issubclass(type_assertion, type(self.delegates[event])):
                raise ValueError("Delegate for event '{}' is not of type '{}'!".format(event, type_assertion.__name__))

            return self.delegates[event]

    def register_event(self, event: str, handler: typing.Callable) -> None:
        """Register the given function as a handler of the given event."""

        # Set function attribute for future reference
        handler.event = event

        # Create default delegate if none exist
        if event not in self.delegates:
            self.delegates[event] = Delegate(event, self)

        self.delegates[event].handlers.append(handler)

    def decorate_event(self, event: str) -> typing.Callable:
        """Discord event registration decorator."""

        def dec(f: typing.Callable):
            self.register_event(event, f)

        return dec
