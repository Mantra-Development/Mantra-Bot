import asyncio
import random
from datetime import datetime
from typing import TYPE_CHECKING, cast

import aiohttp
import hikari
import lightbulb

from mantra.api.urban import make_urban_request
from mantra.core.utils import Colors, CustomPaginator, _chunk

if TYPE_CHECKING:
    from mantra.core.bot import Mantra

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


@fun.command
@lightbulb.option("word", "The word to reverse")
@lightbulb.command("reverse", "Reverse a given word", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reverse_command(ctx: lightbulb.Context, word: str) -> None:
    reversed = word[::-1]

    await ctx.respond(
        embed=hikari.Embed(
            description=f"**Original Word**: `{word}`\n**Reversed Word**: `{reversed}`",
            color=Colors.SUCCESS,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@fun.command
@lightbulb.command("flip", "Flip a coin")
@lightbulb.implements(lightbulb.SlashCommand)
async def flip_coin_command(ctx: lightbulb.Context) -> None:
    choices = {
        "Heads": "https://cdn.discordapp.com/attachments/1026861948274483221/1037314925074325594/heads.png",
        "Tails": "https://cdn.discordapp.com/attachments/1026861948274483221/1037314924780728370/tails.png",
    }

    choice = random.choice(list(choices.keys()))
    await ctx.respond(
        embed=hikari.Embed(title="Flipping a coin...", color=Colors.INFO).set_image(
            "https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif"
        )
    )

    await asyncio.sleep(2)

    await ctx.edit_last_response(
        embed=hikari.Embed(
            title=f"You got {choice}!",
            color=Colors.SUCCESS,
        )
        .set_image(choices[choice])
        .set_footer(
            text="Flipped a coin in Nepali Style ;)",
            icon=ctx.author.avatar_url,
        )
    )


@fun.command
@lightbulb.option("question", "The question to ask the magic 8Ball")
@lightbulb.command("8ball", "Ask the magic 8Ball some questions", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ball_command(ctx: lightbulb.Context, question: str) -> None:
    bot = cast("Mantra", ctx.app)
    async with bot.aiohttp_session.get(f"https://www.eightballapi.com/api") as response:
        data = await response.json()

    await ctx.respond(
        embed=hikari.Embed(
            title="The Magic 8Ball responded...",
            description=f"**❓ Question:**\n```{question}```\n**💬 Answer:**\n```{data['reading']}```",
            color=Colors.SUCCESS,
            timestamp=datetime.now().astimezone(),
        ).set_footer(
            f"Requested by {ctx.author}",
            icon=ctx.author.avatar_url,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fun)
