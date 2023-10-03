from __future__ import annotations

from typing import TYPE_CHECKING, Any
from core import Cog

from discord.ext import commands

if TYPE_CHECKING:
    from core import Bot
    from core import Context


class AdminCog(Cog, name="Admin"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.group(name="dev", aliases=["admin"], invoke_without_command=True)
    @commands.is_owner()
    async def dev(self, ctx: Context) -> Any:
        await ctx.send_help(ctx.command)

    @dev.command(name="load")
    @commands.is_owner()
    async def load(self, ctx: Context, cog_name: str) -> Any:
        try:
            await self.bot.load_extension(
                f"cogs.{cog_name.capitalize()}.{cog_name.lower()}"
            )
            await ctx.success(f"Successfully loaded **{cog_name}** cog.")
        except:
            await ctx.error(f"Failed to load **{cog_name}** cog.")

    @dev.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: Context, cog_name: str) -> Any:
        try:
            await self.bot.reload_extension(
                f"cogs.{cog_name.capitalize()}.{cog_name.lower()}"
            )
            await ctx.success(f"Successfully reloaded **{cog_name}** cog.")
        except:
            await ctx.error(f"Failed to reload **{cog_name}** cog.")

    @dev.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx: Context, cog_name: str) -> Any:
        try:
            await self.bot.unload_extension(
                f"cogs.{cog_name.capitalize()}.{cog_name.lower()}"
            )
            await ctx.success(f"Successfully unloaded **{cog_name}** cog.")
        except:
            await ctx.error(f"Failed to unload **{cog_name}** cog.")


async def setup(bot: Bot) -> None:
    await bot.add_cog(AdminCog(bot))
