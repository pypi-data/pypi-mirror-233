from __future__ import annotations


from typing import Any, Sequence
from discord.ext import commands


__all__: Sequence[str] = ("Cog",)


class Cog(commands.Cog):
    """A custom implementation of commands.Cog class."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
