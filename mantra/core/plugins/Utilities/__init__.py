from datetime import datetime

import hikari

from mantra.core.utils import Colors

STAR_TYPES = {
    "⭐": 0,
    "🌟": 5,
    "✨": 10,
    "💫": 15,
}


def starboard_embed_handler(
    message: hikari.Message, star_count: int
) -> tuple[str, hikari.Embed]:
    emojis = [emoji for emoji, value in STAR_TYPES.items() if value <= star_count][-1]
    content = "{} {} | <#{}>".format(emojis, star_count, message.channel_id)
    embed = hikari.Embed(
        title="Jump to original message!",
        url=message.make_link(message.guild_id),
        description="{}\n".format(message.content),
        color=Colors.GOLDEN,
        timestamp=datetime.now().astimezone(),
    ).set_author(name=message.author.username, icon=message.author.avatar_url)
    if message.attachments:
        embed.set_image(message.attachments[0].url)

    return content, embed
