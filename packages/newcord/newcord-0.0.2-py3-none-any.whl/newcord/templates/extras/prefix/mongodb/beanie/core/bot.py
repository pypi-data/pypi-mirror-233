from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, Sequence, Type, Union

import discord
from beanie import init_beanie
from discord.ext import commands
from helpers.config import Config
from motor.motor_asyncio import AsyncIOMotorClient

from .context import Context
from .models import models

if TYPE_CHECKING:
    from discord import Interaction, Message


__all__: Sequence[str] = ("Bot",)


log = getLogger(__name__)


class Bot(commands.AutoShardedBot):
    def __init__(self) -> None:
        """Initialize the bot with relevant settings."""
        self.config = Config()
        super().__init__(
            command_prefix=commands.when_mentioned_or(self.config.prefix),
            intents=discord.Intents.all(),
            case_insensitive=True,
            description="A template generated using 'newcord'.",
        )

    async def load_cogs(self) -> None:
        """
        Dynamically load cogs into the bot.

        Iterates through the configured cogs and attempts to load them as
        extensions. Logs any errors encountered during loading.
        """
        for cog in self.config.cogs:
            if not cog.startswith("_"):
                try:
                    await self.load_extension(f"{self.config.cogs_directory}.{cog}")
                    log.info(f"Successfully loaded {cog!r} cog.")
                except Exception as exc:
                    log.error(
                        f"Could not load extension {cog} {exc.__class__.__name__}: {exc}"
                    )

    async def init_database(self) -> None:
        """
        Initialize the database connection.

        Connects to the database using the configured URI and initializes
        Beanie with the document models.
        """
        client = AsyncIOMotorClient(self.config.mongo_uri)
        await init_beanie(
            database=client[self.config.database_name], document_models=models
        )
        log.info(
            f"Successfully connected to the {self.config.database_name!r} database"
        )

    async def setup_hook(self) -> Any:
        await self.init_database()
        await self.load_cogs()

    async def on_ready(self) -> Any:
        """Event handler for when the bot is ready."""
        assert self.user is not None
        return log.info(f"Logged in as {self.user.name} (ID: {self.user.id})")

    async def start(self) -> None:  # type: ignore
        """Start the bot."""
        return await super().start(self.config.token, reconnect=True)

    async def get_context(  # type: ignore
        self,
        origin: Union[Message, Interaction],
        *,
        cls: Type[Context] = Context,
    ) -> Any:  # type: ignore
        return await super().get_context(origin, cls=cls)
