import re

import discord

from lib.obj.glass import Glass

client = Glass()


@client.decorate_event("on_message")
async def cubic(message: discord.Message):
    string = re.search(r"^::cubic\s+(['\"])(.*)\1$", message.content, re.MULTILINE | re.IGNORECASE)
    if string:
        string = string.group(2)
        string = cubify(string)
        await client.send_message(message.channel, "`" + string + "`")

    # TODO: Fix max length


def cubify(*args):
    # Concatenate all given parameters
    meme = " ".join(args)

    # Do the thing
    mid = int((len(meme) - 1) / 2)
    cube = ""

    # a b c d e f g
    cube += " ".join(meme)
    cube += "\n"

    # b           f::c
    # c           e
    for i in range(mid - 1):
        cube += meme[i + 1]
        cube += " " * (i * 2 + 1)
        cube += "\\"
        cube += " " * ((len(meme) - 2) * 2 - (i * 2) - 1)
        cube += meme[-2 - i]
        cube += " " * (i * 2 + 1)
        cube += "\\"
        cube += "\n"

    # d     a b c d e f g
    cube += meme[mid]
    cube += " " * (mid * 2 - 1)
    cube += " ".join(meme)
    cube += "\n"

    # e     b     c     f
    # f     c     b     e
    for i in range(len(meme) - mid - 2):
        cube += meme[i + mid + 1]
        cube += " " * (mid * 2 - 1)
        cube += meme[i + 1]
        cube += " " * (((len(meme) - 2) - mid) * 2 + 1)
        cube += meme[-i - mid - 2]
        cube += " " * (mid * 2 - 1)
        cube += meme[-2 - i]
        cube += "\n"

    # g f e d c b a     d
    cube += " ".join(meme[::-1])
    cube += " " * (mid * 2 - 1)
    cube += meme[mid]
    cube += "\n"

    #       e           c
    #       f           b
    for i in range(mid - 1):
        cube += " " * (i * 2 + 2)
        cube += "\\"
        cube += " " * ((mid - i) * 2 - 3)
        cube += meme[-mid + i]
        cube += " " * (((len(meme) - 2) - mid + i) * 2 + 3)
        cube += "\\"
        cube += " " * ((mid - i) * 2 - 3)
        cube += meme[mid - i - 1]
        cube += "\n"

    # g f e d c b a
    cube += " " * (mid * 2)
    cube += " ".join(meme[::-1])
    cube += "\n"

    return cube
