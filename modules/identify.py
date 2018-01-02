import re

import discord

from lib.obj.arbiter import Arbiter
from lib.obj.glass import Glass

glass = Glass()
arbiter = glass.get_delegate("on_message", Arbiter)


@glass.decorate_event("on_message")
async def identify(message: discord.Message):
    channel = message.channel  # type: discord.Channel

    if re.match("^::id.*$", message.content, re.IGNORECASE):
        for u in message.mentions:  # type: discord.Member
            await glass.send_message(channel, str(u) + " : " + u.id)

        for c in message.channel_mentions:  # type: discord.Channel
            await glass.send_message(channel, str(c) + " : " + c.id)
