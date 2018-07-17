import random
import re

import discord

from lib.obj.glass import Glass

client = Glass()

games = [
    "Yelling Simulator",
    "Bit Shifter 2000",
    "Expansion Pack 4",
    "Cube Generator",
]

old_game = None
new_game = None


@client.decorate_event("on_ready")
async def playing_game_ready():
    random.seed()
    await client.change_presence(game=discord.Game(name=random.choice(games)))


@client.decorate_event("on_message")
async def playing_game_refresh(message: discord.Message):
    global old_game, new_game

    match = re.match(r"^::newgame(?:\s+\"(.+)\")?$", message.content, re.IGNORECASE)
    if match:
        new_game = old_game = match.groups()[0]
        if not new_game:
            while new_game == old_game:
                new_game = random.choice(games)
            old_game = new_game

        await client.change_presence(game=discord.Game(name=new_game))
