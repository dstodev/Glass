import discord

from lib.obj.glass import Glass, Delegate

client = Glass()


@client.decorate_delegate("on_message")
def permit(ctx: Delegate):
    # Create fire closure
    fire = ctx.fire

    # Create permission objects
    if ctx.permission is None:
        permission = discord.Permissions.none()
    else:
        permission = ctx.permission

    # Create wrapped function with permissions
    async def permitted_event(message: discord.Message):
        channel = message.channel  # type: discord.Channel
        author = message.author  # type: discord.User

        # Apply permissions
        if author.permissions_in(channel) >= permission:
            print(author.permissions_in(channel).value, permission.value)
            await fire(message)

        # TODO: Notify user of lack of permission?

    # Overwrite handler with one with permissions
    ctx.fire = permitted_event

    return ctx
