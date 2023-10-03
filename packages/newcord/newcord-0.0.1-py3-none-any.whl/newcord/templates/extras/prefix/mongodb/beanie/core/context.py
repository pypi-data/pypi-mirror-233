from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Sequence
from discord.ext import commands

if TYPE_CHECKING:
    from .bot import Bot

__all__: Sequence[str] = ("Context",)


class Context(commands.Context):
    bot: ClassVar[Bot]  # type: ignore

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def success(self, content: str, **kwargs: Any) -> Any:
        return await super().send(f"\U00002705 | {content}", **kwargs)

    async def error(self, content: str, **kwargs: Any) -> Any:
        return await super().send(f"\U0000274e | {content}", **kwargs)
