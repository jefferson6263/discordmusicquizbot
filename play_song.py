import discord
import asyncio

ffmpeg_options = {
    'options': '-vn'
}

async def play_song(song_dic, ctx):
    
    channel = discord.utils.get(ctx.guild.channels, name="General")

    vc = await channel.connect()

    player = discord.FFmpegPCMAudio(executable="C:/PATH_Programs/ffmpeg.exe", source=song_dic["link"], **ffmpeg_options)
    vc.play(player)
    vc.source = discord.PCMVolumeTransformer(vc.source, 0.1)
    
    return vc

