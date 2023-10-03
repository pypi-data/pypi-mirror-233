from __future__ import annotations

from typing import Sequence

from discord.ext import commands


__all__: Sequence[str] = ("NotGuildOwner",)


class NotGuildOwner(commands.CheckFailure):
    """Only guild owner can use this command."""
