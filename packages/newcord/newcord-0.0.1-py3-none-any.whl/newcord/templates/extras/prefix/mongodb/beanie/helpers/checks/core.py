from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from discord.ext import commands
from helpers.errors import NotGuildOwner

if TYPE_CHECKING:
    from core.context import Context
    from discord import User
    from discord.ext.commands._types import Check

__all__: Sequence[str] = ("is_guild_owner",)


def is_guild_owner() -> Check:
    async def predicate(ctx: Context) -> bool:
        if ctx.guild is None or ctx.guild.owner_id == ctx.author.id:
            return True

        raise NotGuildOwner("Only guild owner can use this command.")

    return commands.check(predicate)
