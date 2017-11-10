import re

import discord

from lib.obj.glass import Glass

client = Glass()


@client.decorate_event("on_message")
async def id(message: discord.Message):
    channel = message.channel  # type: discord.Channel

    if re.match("^::id.*$", message.content, re.IGNORECASE):
        for u in message.mentions:  # type: discord.Member
            await client.send_message(channel, str(u) + " : " + u.id)

        for c in message.channel_mentions:  # type: discord.Channel
            await client.send_message(channel, str(c) + " : " + c.id)
