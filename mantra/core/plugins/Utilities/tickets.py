from math import perm

import hikari
import lightbulb
import miru

from mantra.core.models import TicketConfig
from mantra.core.utils.buttons import create_ticket_button
from mantra.core.utils.colors import Colors

tickets = lightbulb.Plugin("Tickets", "Plugin that handles ticket commands")


@tickets.command
@lightbulb.command("ticket", "Command group containing ticket commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def ticket_command(_: lightbulb.Context) -> None:
    ...


@ticket_command.child
@lightbulb.option("message", "Custom message to include in the embed", required=False)
@lightbulb.command("create", "Create a ticket embed in a channel", pass_options=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def create_ticket(
    ctx: lightbulb.Context,
    message: str | None,
) -> None:
    ticket_config = await TicketConfig.get_or_none(guild_id=ctx.guild_id)
    if not ticket_config:
        category = await ctx.get_guild().create_category("Tickets")
        channel = await ctx.get_guild().create_text_channel(
            "tickets",
            category=category,
            permission_overwrites=[
                hikari.PermissionOverwrite(
                    id=ctx.guild_id,
                    type=0,
                    deny=hikari.Permissions.SEND_MESSAGES,
                )
            ],
        )

        await TicketConfig.create(
            guild_id=ctx.guild_id,
            message=message,
            channel=channel.id,
        )
    else:
        channel = ctx.get_guild().get_channel(ticket_config.channel)

    await channel.send(
        embed=hikari.Embed(
            title="Ticket",
            description=message or "Click the button below to create the Ticket!",
            color=Colors.GENERIC,
        ),
        components=[create_ticket_button(ctx)],
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tickets)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tickets)
