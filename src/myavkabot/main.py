import discord
import gtts.lang
from discord.ext import commands

from .config import Config, get_config

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="&", intents=intents)


config: Config = get_config()


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("✅")


@bot.tree.command(name="join")
async def join(
    interaction: discord.Interaction, voice: discord.VoiceChannel | None = None
):

    if voice is None:
        if not interaction.user.voice:
            await interaction.response.send_message(
                "ты не в гс либо укажи его", ephemeral=True
            )
            return
        voice = interaction.user.voice.channel

    channel = voice

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
):
    if interaction.guild.voice_client:
        supported_languages = gtts.lang.tts_langs()

        voice_client = interaction.guild.voice_client
        audio = tts.tts_buffer(sentence, lang=lang)
        audio_source = discord.FFmpegPCMAudio(audio, pipe=True)

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


bot.run(token=config.BOT_TOKEN)
