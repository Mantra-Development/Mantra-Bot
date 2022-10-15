import typing as t

import hikari
import lightbulb
import miru
from miru.ext import nav

from mantra.core.utils.colors import Colors
from mantra.core.utils.emojis import Emojis

_ValueT = t.TypeVar("_ValueT")


def _chunk(iterator: t.Iterator[_ValueT], max: int) -> t.Iterator[list[_ValueT]]:
    chunk: list[_ValueT] = []
    for entry in iterator:
        chunk.append(entry)
        if len(chunk) == max:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


class CustomPaginator(nav.NavigatorView):
    def __init__(
        self,
        lctx: lightbulb.Context,
        *,
        pages: list[str | hikari.Embed],
        buttons: t.Optional[list[nav.NavButton]] = None,
        timeout: t.Optional[float] = 120,
        autodefer: bool = True,
    ) -> None:
        self.lctx = lctx
        buttons = buttons or [
            nav.FirstButton(emoji=hikari.Emoji.parse(Emojis.FIRST)),
            nav.PrevButton(emoji=hikari.Emoji.parse(Emojis.PREV)),
            nav.IndicatorButton(),
            nav.NextButton(emoji=hikari.Emoji.parse(Emojis.NEXT)),
            nav.LastButton(emoji=hikari.Emoji.parse(Emojis.LAST)),
        ]

        super().__init__(
            pages=pages, buttons=buttons, timeout=timeout, autodefer=autodefer
        )

    async def view_check(self, ctx: miru.Context) -> bool:
        if ctx.user.id != self.lctx.author.id:
            await ctx.respond(
                embed=hikari.Embed(
                    description=f"{Emojis.WARNING} You cannot interact with this as it belongs to <@{ctx.user.id}>",
                    color=Colors.ERROR,
                ),
                flags=hikari.MessageFlag.EPHEMERAL,
            )

        return ctx.user.id == self.lctx.author.id
