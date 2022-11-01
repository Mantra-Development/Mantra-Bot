import logging

import hikari
import lightbulb
from tortoise.transactions import atomic

from mantra.core.models import TicketConfig
from mantra.core.utils.buttons import create_ticket_button
from mantra.core.utils.colors import Colors
from mantra.core.utils.emojis import Emojis

from . import create_tickets_channel

tickets = lightbulb.Plugin("Tickets", "Plugin that handles ticket commands")


@tickets.command
@lightbulb.command("ticket", "Command group containing ticket commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def ticket_command(_: lightbulb.Context) -> None:
    ...


@atomic
@ticket_command.child
@lightbulb.option("message", "Custom message to include in the embed", required=False)
@lightbulb.command("startup", "Create a ticket embed in a channel", pass_options=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def create_ticket(
    ctx: lightbulb.Context,
    message: str | None,
) -> None:
    ticket_config = await TicketConfig.get_or_none(guild_id=ctx.guild_id)
    if not ticket_config:
        channel = await create_tickets_channel(ctx)

        await TicketConfig.create(
            guild_id=ctx.guild_id,
            message=message,
            channel=channel.id,
        )
    else:
        channel = ctx.get_guild().get_channel(ticket_config.channel)
        if not channel:
            channel = await create_tickets_channel(ctx)
            ticket_config.channel = channel.id
            await ticket_config.save()

    last_message = await channel.fetch_history().limit(1)
    if not last_message:
        await channel.send(
            embed=hikari.Embed(
                title="Ticket",
                description=message or "Click the button below to create the Ticket!",
                color=Colors.GENERIC,
            ),
            components=[create_ticket_button(ctx)],
        )

    await ctx.respond(
        embed=hikari.Embed(
            description=f"{ Emojis.SUCCESS} Tickets channel has been created successfully!",
            color=Colors.SUCCESS,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@tickets.listener(hikari.InteractionCreateEvent)
async def handle_create_ticket(event: hikari.InteractionCreateEvent) -> None:
    if (
        not isinstance(event.interaction, hikari.ComponentInteraction)
        or event.interaction.custom_id != "new_ticket"
    ):
        return

    await event.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        "Button clicked!",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tickets)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tickets)
