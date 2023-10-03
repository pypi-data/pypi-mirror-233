from __future__ import annotations

from typing import TYPE_CHECKING, Any

import discord
from discord.ext import commands
from helpers import errors
from core import Cog

if TYPE_CHECKING:
    from core import Bot, Context


class ErrorsCog(Cog, name="Errors"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> Any:
        ignored = (
            commands.CommandNotFound,
            commands.NoPrivateMessage,
            discord.Forbidden,
            discord.NotFound,
        )

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CheckFailure):
            if isinstance(error, errors.NotGuildOwner):
                owner_mention = (
                    f"<@{ctx.guild.owner_id}>" if ctx.guild else "server owner(s)"
                )
                return await ctx.error(
                    f"Only {owner_mention} have permission to use this command."
                )
            return await ctx.error(error.args[0])


async def setup(bot: Bot) -> None:
    await bot.add_cog(ErrorsCog(bot))
