import hikari
import lightbulb

from mantra.api.urban import make_urban_request
from mantra.core.utils import Colors, CustomPaginator, _chunk

fun = lightbulb.Plugin("Fun", "Fun Commands Plugin")


@fun.command
@lightbulb.option("term", "The term to search for")
@lightbulb.command("urban", "Search the urban dictionary", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def urban_command(ctx: lightbulb.Context, term: str) -> None:
    data_list = await make_urban_request(term)

    fields = [
        hikari.Embed(
            title=f"Definition for {term}",
            color=Colors.INFO,
            url=data[0].permalink,
        )
        .add_field(name="Definition", value=data[0].definition)
        .add_field(name="Example", value=data[0].example)
        .set_footer("Powered by Urban API")
        for data in _chunk(data_list, 1)
    ]

    navigator = CustomPaginator(ctx, pages=fields)
    await navigator.send(ctx.interaction, ephemeral=True)
    await navigator.wait()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fun)
