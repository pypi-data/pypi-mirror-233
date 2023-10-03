from __future__ import annotations

from typing import TYPE_CHECKING

from .errors import ErrorsCog

if TYPE_CHECKING:
    from core import Bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(ErrorsCog(bot))
