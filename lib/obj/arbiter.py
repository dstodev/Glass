import typing

from lib.obj.glass import Delegate

import discord


class Arbiter(Delegate):
    """Delegate for the "on_message" event. Adds functionality:
    ♦ Permissions
    """

    def __init__(self, event, *args):
        if event != "on_message":
            raise ValueError("Delegate 'Arbiter' must own event 'on_message'!")

        self.users = {}  # user ID: permission level
        self.restricted = {}  # handler name: required permission level

        super().__init__(event, *args)

    def modify_handler(self, handler: typing.Callable) -> typing.Callable:

        async def modifier(message: discord.Message):
            author = message.author  # type: discord.User
            await handler(message)

        return modifier
