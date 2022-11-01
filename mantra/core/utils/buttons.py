import hikari
import lightbulb
from hikari.api.special_endpoints import ActionRowBuilder


def create_source_button(ctx: lightbulb.Context, source: str) -> ActionRowBuilder:
    return (
        ctx.app.rest.build_action_row()
        .add_button(hikari.ButtonStyle.LINK, source)
        .set_label("Source")
        .set_emoji("🔗")
        .add_to_container()
    )


def create_ticket_button(ctx: lightbulb.Context) -> ActionRowBuilder:
    return (
        ctx.app.rest.build_action_row()
        .add_button(hikari.ButtonStyle.PRIMARY, "new_ticket")
        .set_label("Create Ticket")
        .set_emoji("📩")
        .add_to_container()
    )
