
from helper_functions import is_user_admin
import os
import youtube_dl
import urllib.parse, urllib.request, re
import requests
from bs4 import BeautifulSoup
from helper_functions import is_user_admin
import re
import json
import discord

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
        
        #checks if user is admin or not
        if not is_user_admin(self.ctx):
            not_admin= discord.Embed(
                description = f'You are not an admin and cannot add songs to the question bank',
                colour = 0xF40000
            )
            await self.ctx.message.channel.send(embed = not_admin)
            return
        
        # searches for the offical version of the song but doesn't download
        # the offical music video because the offical music videos might
        # have long intros. Offical music videos also follow the form
        # artist - song, which allows the title to be easily parsed
        search = str(self.ctx.message.content) + " offical music"
        search = search.replace('%addsong', '')
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        
        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")
        title = str(s.head.title)
        
        title = title.replace("amp;", '')
        title = title.replace("<title>", '')
        title = title.replace("</title>", '')
        title = title.replace(" - YouTube", '')
        
        # could be simpilfied with regex but idk how to use regex
        title = title.replace("(Official Video)", '')
        title = title.replace("(Official Music Video)", '')
        title = title.replace("(Official Lyric)", '')
        title = title.replace("(Lyric)", '')
        title = title.replace("(Audio)",'')
        title = title.replace("(Official)", '')
        title = title.replace("(Offical Audio)",'')
        
        title = title.replace("[Official Music Video]",'')
        title = title.replace("[Official Video]",'')
        title = title.replace("[Official Lyric]",'')
        title = title.replace("[Official]",'')
        title = title.replace("[Official Audio]",'')
        title = title.replace("[Audio]",'')
        title = title.replace("[Lyirc]",'')
        
        
        title = title.strip()
        
        """
        title = title.split("ft.", 1)
        title = title[0]     
        regex = re.compile(".*?\((.*?)\)")
        title = re.findall(regex, title)
        """
        

        # checks if song is already in song bank
        if f'{title}.mp3' in os.listdir("Songs/"):
            already_in_bank = discord.Embed(
                description = f'Song is already in song bank',
                colour = 0xF40000
            )
            await self.ctx.message.channel.send(embed = already_in_bank)
        else:
            
            # searches for the lyric music video
            search = str(self.ctx.message.content) + "lyircs"
            search = search.replace('%addsong', '')
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
            url = 'http://www.youtube.com/watch?v=' + search_results[0]

            # downloads the lyricsmusic video
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                file = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(file)

                
            os.rename(filename, f'Songs/{title}.mp3')
            name = title.partition('-')[2]
            name = re.sub(r'\([^)]*\)', '', name)
            
            name = name.strip()
            print(title)
            artist = title.partition('-')[0].strip()
            artist = artist.partition('with')[0].strip()
            artist = artist.partition('and')[0].strip()
            artist = artist.partition(',')[0].strip()
            artist = artist.partition('ft.')[0].strip()
            artist = artist.partition('&')[0].strip()
            
            song_dic = {
                "name": name, 
                "artist": artist,
                "lyrics": "blah blah blah",    
                "link": f'Songs/{title}.mp3'
            }
            
            # writes to songs.json
            with open("songs.json","r+") as file:
                file_data = json.load(file)
                file_data["songs"].append(song_dic)
                file.seek(0)
                json.dump(file_data, file, indent = 4)
                
            bot_message = discord.Embed(
                description = f'Added {title} to SongBank',
                colour = 0x00FF08
            )
            
            await self.ctx.message.channel.send(embed = bot_message)

