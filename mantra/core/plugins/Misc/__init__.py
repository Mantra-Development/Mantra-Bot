import lightbulb


async def send_remainder(ctx: lightbulb.Context, text: str) -> None:
    await ctx.respond(
        f"{ctx.author.mention} Remainder: `{text}`",
        user_mentions=True,
    )
