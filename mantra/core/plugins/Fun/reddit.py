from datetime import datetime

import hikari
import lightbulb

from mantra.core.utils import Colors, CustomPaginator, _chunk

reddit = lightbulb.Plugin("Reddit", "Plugin for reddit commands")


@reddit.command
@lightbulb.command("reddit", "Base Command for reddit commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def reddit_command(_: lightbulb.Context) -> None:
    ...


@reddit_command.child
@lightbulb.command("memes", "Get a random post from the memes subreddit.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def memes_command(ctx: lightbulb.Context) -> None:
    memes = await ctx.bot.reddit_cache.get_data("memes")
    fields = [
        hikari.Embed(
            title=meme[0].title,
            url=f"https://new.reddit.com{meme[0].permalink}",
            color=Colors.GENERIC,
            timestamp=datetime.fromtimestamp(meme[0].timestamp).astimezone(),
        )
        .set_image(meme[0].url)
        .set_footer(
            text=f"⬆️ {meme[0].upvotes} upvotes | 💬 {meme[0].comments} comments"
        )
        .set_author(name=meme[0].author_name)
        for meme in _chunk(memes, 1)
    ]

    navigator = CustomPaginator(ctx, pages=fields)
    await navigator.send(ctx.interaction)
    await navigator.wait()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(reddit)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(reddit)
