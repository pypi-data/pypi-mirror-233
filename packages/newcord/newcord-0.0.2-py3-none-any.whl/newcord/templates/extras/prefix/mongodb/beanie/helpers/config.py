from __future__ import annotations

from typing import Final, Sequence, Tuple, final
from dataclasses import dataclass


__all__: Sequence[str] = ("Config",)


@final
@dataclass
class Config:
    token: Final[str] = "Your bot token"
    prefix: Final[str] = "Your bot prefix"
    cogs_directory: Final[str] = "cogs"
    mongo_uri: Final[str] = "Your mongo uri"
    database_name: Final[str] = "main"
    cogs: Tuple[str, ...] = ("Admin", "Events", "Todo")
