from datetime import datetime

import hikari
import lightbulb

from mantra.api.animals import make_request
from mantra.core.utils import Colors, create_source_button

animals = lightbulb.Plugin("Animals", "Animal Command Plugin")

animal_choices = [
    "dog",
    "cat",
    "panda",
    "fox",
    "koala",
    "bird",
    "raccoon",
    "kangaroo",
]


@animals.command
@lightbulb.option("type", "Type of animal", choices=animal_choices)
@lightbulb.command("animal", "Get a random animal fact and image", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dog_command(ctx: lightbulb.Context, type: str) -> None:
    animal = await make_request(type)
    button = create_source_button(ctx, "https://some-random-api.ml")
    await ctx.respond(
        embed=hikari.Embed(
            title=f"Here's a random {type} for you!",
            description=f"```{animal.fact}```",
            color=Colors.SUCCESS,
            timestamp=datetime.now().astimezone(),
        )
        .set_thumbnail(ctx.app.application.icon_url)
        .set_image(animal.image)
        .set_footer(text="Mantra© 2022-Present"),
        components=[button],
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(animals)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(animals)
