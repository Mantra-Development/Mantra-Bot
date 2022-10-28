import hikari
import lightbulb


async def create_tickets_channel(ctx: lightbulb.Context) -> hikari.GuildChannel:
    return await ctx.get_guild().create_text_channel(
        "tickets",
        permission_overwrites=[
            hikari.PermissionOverwrite(
                id=ctx.guild_id,
                type=0,
                deny=hikari.Permissions.SEND_MESSAGES,
            )
        ],
    )
