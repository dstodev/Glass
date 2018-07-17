import re
import sys
import os
import discord

from lib.obj.glass import Glass

glass = Glass()


# TODO: Automatically register this event for every script?
@glass.decorate_event("on_ready")
async def announce():
    print("Module '{}' loaded!".format(os.path.basename(__file__)), file=sys.stderr)


@glass.decorate_event("on_message")
async def identify(message: discord.Message):
    channel = message.channel  # type: discord.Channel

    if re.match("^::id.*$", message.content, re.IGNORECASE):
        for u in message.mentions:  # type: discord.Member
            await glass.send_message(channel, str(u) + " : " + u.id)

        for c in message.channel_mentions:  # type: discord.Channel
            await glass.send_message(channel, str(c) + " : " + c.id)
