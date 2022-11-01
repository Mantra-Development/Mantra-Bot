from datetime import datetime

import hikari
import lightbulb

from mantra.core.utils.colors import Colors
from mantra.core.utils.emojis import Emojis

info = lightbulb.Plugin("Info", "Plugin that contains all the info commands")


@info.command
@lightbulb.command("serverinfo", "Get info about a server")
@lightbulb.implements(lightbulb.SlashCommand)
async def serverinfo_command(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    assert guild is not None
    created_at = int(guild.created_at.timestamp())

    members = [member for member in guild.get_members().values() if not member.is_bot]
    bots = [member for member in guild.get_members().values() if member.is_bot]
    description = ""
    server_invite = await ctx.app.rest.create_invite(ctx.channel_id)
    fields = [
        ("ID", guild.id),
        ("Server Creation Date", f"<t:{created_at}:F>"),
        ("Server Owner", f"<@{guild.owner_id}>"),
        ("Bot Count", len(bots)),
        ("Member Count", len(members)),
        ("Channel Count", len(guild.get_channels())),
        ("Role Count", len(guild.get_roles())),
        ("Boost Count", guild.premium_subscription_count),
        (
            "Invite URL",
            f"https://discord.gg/{guild.vanity_url_code}"
            if guild.vanity_url_code
            else server_invite,
        ),
    ]

    for name, value in fields:
        description += f"**• {name}** `:` {value}\n"

    await ctx.respond(
        embed=hikari.Embed(
            title=f"Info of {guild.name}",
            description=description,
            color=Colors.INFO,
            timestamp=datetime.now().astimezone(),
        )
        .set_thumbnail(guild.icon_url)
        .set_author(name=f"{ctx.author}", icon=ctx.author.avatar_url)
        .set_footer(
            text=f"{Emojis.COPY} Mantra Development",
            icon=ctx.bot.get_me().avatar_url,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@info.command
@lightbulb.command("Userinfo", "Get info of a user", pass_options=True)
@lightbulb.implements(lightbulb.UserCommand)
async def userinfo_command(ctx: lightbulb.Context, target: hikari.Member) -> None:

    assert ctx.guild_id is not None
    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]
    member_presence = target.get_presence()
    perms = hikari.Permissions.NONE
    for r in roles:
        perms |= r.permissions

    permissions = str(perms).split("|")

    if target.id == ctx.get_guild().owner_id:
        acknowlegdement = "Server Owner"
    elif "ADMINISTRATOR" in permissions:
        acknowlegdement = "Administrator"
    elif "MANAGE_GUILD" in permissions:
        acknowlegdement = "Moderator"
    elif "MANAGE_MESSAGES" in permissions:
        acknowlegdement = "Staff"
    else:
        acknowlegdement = "Member"

    status = (
        member_presence.visible_status if member_presence is not None else "Offline"
    )
    description = ""
    fields = [
        ("ID", target.id),
        ("Joined at", f"<t:{joined_at}:F> • <t:{joined_at}:R>"),
        ("Created at", f"<t:{created_at}:F> • <t:{created_at}:R>"),
        ("Acknowledgement", acknowlegdement),
        ("Nickname", target.nickname if target.nickname else "None"),
        ("Status", status.title()),
    ]
    for name, value in fields:
        description += f"**{name}** : {value}\n"
    embed = (
        hikari.Embed(
            title=f"Userinfo of {str(target) + ' 👑' if ctx.get_guild().owner_id == target.id else target}",
            description=description,
            color=Colors.INFO,
            timestamp=datetime.now().astimezone(),
        )
        .set_thumbnail(target.display_avatar_url)
        .set_author(name=f"{ctx.author}", icon=ctx.author.avatar_url)
    )
    if permissions:
        embed.add_field(
            name="Permissions",
            value=",".join(perm.replace("_", " ").title() for perm in permissions),
            inline=False,
        )
    if roles:
        embed.add_field(name="Roles", value=",".join(r.mention for r in roles))

    await ctx.respond(
        embed=embed.set_footer(
            f"{Emojis.COPY} Mantra Development", icon=ctx.bot.get_me().avatar_url
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(info)
