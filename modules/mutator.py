import discord

from lib.obj.glass import Glass, Delegate

client = Glass()


@client.decorate_delegate("on_message")
def permit(ctx: Delegate):
    fire = ctx.fire
    if ctx.permission is None:
        permission = discord.Permissions.none()
    else:
        permission = ctx.permission

    async def permitted_event(message: discord.Message):
        channel = message.channel  # type: discord.Channel
        author = message.author  # type: discord.User

        # Apply permissions
        if permission and author.permissions_in(channel) >= permission:
            await fire(message)

    ctx.fire = permitted_event

    return ctx
