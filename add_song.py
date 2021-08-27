
from helper_functions import is_user_admin
import os
import youtube_dl
import urllib.parse, urllib.request, re
import requests
from bs4 import BeautifulSoup
from helper_functions import is_user_admin
import re
import json

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
        
        
        title = title.replace("(Official Video)", '')
        title = title.replace("(Official Music Video)", '')
        title = title.replace("(Official Lyric)", '')
        title = title.replace("(Lyric)", '')
        title = title.replace("(Audio)",'')
        title = title.replace("(Official)", '')
        title = title.replace("(Offical Audio)",'')
        title = title.replace("[Official Music Video]",'')
        title = title.replace("[Official Video]",'')
        title = title.strip()
        
        """
        title = title.split("ft.", 1)
        title = title[0]     
        regex = re.compile(".*?\((.*?)\)")
        title = re.findall(regex, title)
        """
        
        search = str(self.ctx.message.content) + "lyircs"
        search = search.replace('%addsong', '')
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        

        
        if f'{title}.mp3' in os.listdir("Songs/"):
            await self.ctx.message.channel.send(f'Song is already in song bank')
        else:
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                file= ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(file)
                print(filename)
                
            os.rename(filename, f'Songs/{title}.mp3')
            name = title.partition('-')[2]
            name = re.sub(r'\([^)]*\)', '', name)
            
            name = name.strip()
            artist = title.partition('-')[0].strip()
            artist = title.partition('with')[0].strip()
            artist = artist.partition('and')[0].strip()
            artist = artist.partition(',')[0].strip()
            artist = artist.partition('ft.')[0].strip()
            
            song_dic = {
                "name": name, 
                "artist": artist,
                "lyrics": "blah blah blah",    
                "link": f'Songs/{title}.mp3'
            }
            
            with open("songs.json","r+") as file:
                file_data = json.load(file)
                file_data["songs"].append(song_dic)
                file.seek(0)
                json.dump(file_data, file, indent = 4)
                
            await self.ctx.message.channel.send(f'Added {title} to SongBank')

