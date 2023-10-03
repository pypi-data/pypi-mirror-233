#!/usr/bin/env python3

from __future__ import annotations

import asyncio
from core import Bot


async def main() -> None:
    from discord import utils

    utils.setup_logging()
    async with Bot() as bot:
        await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
