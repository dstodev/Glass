import re

import discord

from lib.obj.glass import Glass

client = Glass()

trl = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ",
    "e": "ᴇ", "f": "ꜰ", "g": "ɢ", "h": "ʜ",
    "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ",
    "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ",
    "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ",
    "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x",
    "y": "ʏ", "z": "ᴢ",
}


@client.decorate_event("on_message")
async def enemy_stand(message: discord.Message):
    pack = ""

    if re.match("^.*?::stand.+?[\"\'].+?[\"\'].*?$", message.content, re.IGNORECASE):
        string = re.findall("^.*?::stand.+?[\"\'](.+?)[\"\']", message.content, re.IGNORECASE)[0]

        pack += "「"

        for char in string:
            if char in trl:
                pack += trl[char.lower()]
            else:
                pack += char

        pack += "」"

        out = re.findall("^(.+?)::stand.+?[\"\']", message.content, re.IGNORECASE)
        if out:
            out = out[0]
            stand = re.findall("^.+?::(stand).+?[\"\']", message.content, re.IGNORECASE)[0]
            out += stand
        else:
            out = ""

        out += re.findall("^.*?::stand(.+?)[\"\']", message.content, re.IGNORECASE)[0]
        out += pack
        out += re.findall("^.*?::stand.+?[\"\'].+?[\"\'](.*?)$", message.content, re.IGNORECASE)[0]

        pack = out

    if pack:
        await client.send_message(message.channel, pack)
