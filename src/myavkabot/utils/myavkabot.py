from typing import Self

from discord import Intents
from discord.ext.commands import Bot


class MyavkaBot:
    _instance: Bot | None = None

    @classmethod
    def setup(cls: type[Self], owner_id: int, description: str | None = None) -> None:
        if cls._instance is not None:
            raise ValueError("already initialized")

        intents: Intents = Intents.default()
        intents.voice_states = True
        cls._instance = Bot(
            command_prefix="",
            help_command=None,
            description=description,
            intents=intents,
            owner_id=owner_id,
        )

    @classmethod
    def run(cls: type[Self], token: str) -> None:
        if cls._instance is None:
            raise ValueError("bot is not initialized, run setup first")

        cls._instance.run(token=token)
