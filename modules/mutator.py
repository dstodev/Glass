import discord

from lib.obj.glass import Glass, Delegate

client = Glass()


@client.decorate_delegate("on_message")
def permit(ctx: Delegate):
    fire = ctx.fire

    ctx.test = 123
    print(ctx.test)

    async def permitted_event(message: discord.Message):
        author = message.author  # type: discord.User
        if author.permissions_in(message.channel):
            await fire(message)

    ctx.fire = permitted_event

    return ctx
