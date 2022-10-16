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
@lightbulb.command("memes", "Get posts from the memes subreddit.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def memes_command(ctx: lightbulb.Context) -> None:
    memes = await ctx.bot.reddit_cache.get_data("memes")
    fields = [
        hikari.Embed(
            title=meme[0].title,
            url=f"https://new.reddit.com{meme[0].permalink}",
            color=Colors.GENERIC,
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


@reddit_command.child
@lightbulb.command("cursedcomments", "Get posts from the cursedcomments subreddit.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def cursed_comments(ctx: lightbulb.Context) -> None:
    cursedcomments = await ctx.bot.reddit_cache.get_data("cursedcomments")
    fields = [
        hikari.Embed(
            title=cursed_comment[0].title,
            url=f"https://new.reddit.com{cursed_comment[0].permalink}",
            color=Colors.GENERIC,
        )
        .set_image(cursed_comment[0].url)
        .set_footer(
            text=f"⬆️ {cursed_comment[0].upvotes} upvotes | 💬 {cursed_comment[0].comments} comments"
        )
        .set_author(name=cursed_comment[0].author_name)
        for cursed_comment in _chunk(cursedcomments, 1)
    ]

    navigator = CustomPaginator(ctx, pages=fields)
    await navigator.send(ctx.interaction)
    await navigator.wait()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(reddit)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(reddit)
