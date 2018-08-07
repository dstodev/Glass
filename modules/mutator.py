import discord

from lib.obj.glass import Glass, Delegate

client = Glass()


# TODO: Regex match as part of delegate decorator
@client.decorate_delegate("on_message")
def permit(ctx: Delegate):
    # Create fire closure
    fire = ctx.fire

    # Create permissions object
    if ctx.permission is None:
        permissions = discord.Permissions.none()
    else:
        if isinstance(ctx.permissions, dict):
            permissions = discord.Permissions()
            permissions.update(**ctx.permissions)
        elif isinstance(ctx.permissions, discord.Permissions):
            permissions = ctx.permissions

    # Create wrapped function with permissions
    async def permitted_event(message: discord.Message):
        channel = message.channel  # type: discord.Channel
        author = message.author  # type: discord.User

        # Apply permissions
        if author.permissions_in(channel) >= permissions:
            print(author.permissions_in(channel).value, permissions.value)
            await fire(message)

        # TODO: Notify user of lack of permission?

    # Overwrite handler with one with permissions
    ctx.fire = permitted_event

    return ctx
