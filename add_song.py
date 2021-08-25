from helper_functions import is_user_admin
import discord
import os
import youtube_dl
from discord.voice_client import VoiceClient
import urllib.parse, urllib.request, re
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from helper_functions import is_user_admin

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'Songs/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'yesplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', 
}


class addSong: 
    def __init__(self, ctx):
        self.ctx = ctx
        
    async def add(self):
        if not is_user_admin(self.ctx):
            await self.ctx.message.channel.send("you are not a server admin and cannot add songs to the song bank")
            return
        
        search = str(self.ctx.message.content) + "lyrics"
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        
        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")
        title = str(s.head.title)
        print(title)
        title = ''.join(filter(str.isalnum, title))
        title = title.replace("<title>", '')
        title = title.replace("</title>", '')
        title = title.replace("(Lyrics)", '')
        title = title.replace("Lyrics", '')
        title = title.replace("(lyrics)", '')
        title = title.replace("lyrics", '')
        
        
        
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            file = ydl.extract_info(url, download=True)
            test = ydl.prepare_filename(file)
            
            #os.rename(test, f'Songs/{songname}_by_{artist}.mp3' )
        
        await self.ctx.message.channel.send(title)
    
    