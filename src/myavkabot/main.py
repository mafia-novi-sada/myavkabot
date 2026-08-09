from typing import Any

import discord
import gtts.lang
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.flags import Intents
from discord.player import FFmpegPCMAudio
from discord.voice_client import VoiceProtocol

from src.myavkabot.utils import tts

intents: Intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True


bot: Bot = commands.Bot(command_prefix="&", intents=intents)

tts.TextToSpeech.tts_buffer()


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print("✅")


@bot.tree.command(name="join")
async def join(
    interaction: discord.Interaction, voice: discord.VoiceChannel | None = None
) -> None:

    if voice is None:
        if not interaction.user.id:
            await interaction.response.send_message(
                "ты не в гс либо укажи его", ephemeral=True
            )
            return
        voice: VoiceChannel | None = interaction.user.voice.channel

    channel: VoiceChannel | None = voice

    if not channel:
        await interaction.response.send_message("канал не найден", ephemeral=True)
        return

    if not isinstance(channel, discord.VoiceChannel):
        await interaction.response.send_message("это не гс", ephemeral=True)
        return

    try:
        await channel.connect()
        await interaction.response.send_message("коннектед")
    except Exception as _ex:
        await interaction.response.send_message(f"ошибка! {_ex}", ephemeral=True)


@bot.tree.command(name="say")
async def say(
    interaction: discord.Interaction, sentence: str = "нормас", lang: str = "ru"
) -> None:
    if interaction.guild.voice_client:
        supported_languages: dict[Any, Any] = gtts.lang.tts_langs()

        voice_client: VoiceProtocol = interaction.guild.voice_client
        audio: Any = tts.tts_buffer(sentence, lang=lang)
        audio_source: FFmpegPCMAudio = discord.FFmpegPCMAudio(audio, pipe=True)

        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(audio_source)

        await interaction.response.send_message(
            f"сказано: {sentence} (язык: {supported_languages[lang]})"
        )
    else:
        await interaction.response.send_message("не в войсе", ephemeral=True)


@bot.tree.command(name="leave")
async def leave(interaction: discord.Interaction):
    print(interaction.guild.voice_client)
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("отключен")
    else:
        await interaction.response.send_message("нет в канале", ephemeral=True)


bot.run()
