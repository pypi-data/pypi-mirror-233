from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from discord.ext import commands
from core.models import Task
from core import Cog

if TYPE_CHECKING:
    from core import Bot, Context


class TodoCog(Cog, name="Todo"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.group(aliases=["todo"])
    async def task(self, ctx: Context) -> Any:
        """A command group for managing tasks."""
        if not ctx.subcommand_passed:
            return await ctx.send_help(ctx.command)

    @task.command()
    async def add(self, ctx: Context, title: str, *, description: Optional[str]):
        """Add a new task to your list."""
        # Check if the task already exists in the user's task list.
        # Documentation: http://beanie-odm.dev/tutorial/finding-documents/
        existing_task = await Task.find_one(
            Task.user_id == ctx.author.id and Task.title == title
        )
        if existing_task:
            return await ctx.error(
                f"`{title}` is already in your task list. You can't add duplicate tasks."
            )

        # Insert the new task into the database.
        # Documentation: http://beanie-odm.dev/tutorial/inserting-into-the-database/
        await Task(user_id=ctx.author.id, title=title, description=description).create()
        await ctx.success(f"Task `{title}` has been successfully added to your list.")

    @task.command()
    async def complete(self, ctx: Context, title: str) -> Any:
        """Mark a task as completed."""
        # Find the task in the user's task list.
        # Documentation: http://beanie-odm.dev/tutorial/finding-documents/
        task = await Task.find_one(
            Task.user_id == ctx.author.id and Task.title == title
        )
        if not task:
            return await ctx.error(
                f"No task found with the name `{title}` in your list."
            )

        # Update the task to mark it as completed.
        # Documentation: http://beanie-odm.dev/tutorial/updating-%26-deleting/#update-queries
        await task.set({"completed": True})
        await ctx.success(f"Task `{title}` has been marked as completed.")


async def setup(bot: Bot) -> None:
    await bot.add_cog(TodoCog(bot))
