
import json
import time
import sys
import re

# neede so python knows where to find lyricsgenius folder
# not the best way to do this as this means this function only works for jefferson but its whatever
sys.path.append(r'C:\Users\Jefferson\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages')
import lyricsgenius



with open("songs.json","r+") as file:
    genius = lyricsgenius.Genius("wK20z6Y2-LnreDmZ1vEKuapUsNHIYtEAVvJ0zyUg8qOWyduf6LJ4qi4oBnh5c8-c")
    file_data = json.load(file)
    
    # looking through all songs stored in songs.json
    for song_dic in file_data["songs"]:
        # if song already has lyrics
        if song_dic["lyrics"] != 'blah blah blah':
            print("this song already has lyrics")
        else:
            song = genius.search_song(song_dic["name"], song_dic["artist"])
            lyrics = str(song.lyrics)
            lyrics = re.split("\[[^\]]*\]", lyrics)
            lyric_list = []
            
            # goes through the lyrics and removes only uses verse that have more than 100 characters
            for verse in lyrics:
                if len(verse) > 100:
                    verse = verse.replace("72EmbedShare URLCopyEmbedCopy",'')
                    lyric_list.append(verse)
                
            file_data["songs"].remove(song_dic)
            song_dic["lyrics"] = lyric_list
            file_data["songs"].append(song_dic)
        
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            time.sleep(3)
        
            
