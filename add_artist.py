
import sys
import os
import json

sys.path.append(r'C:\Users\Jefferson\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages')
from google_images_download import google_images_download   

def add_photo(artist):
    
    with open("artist.json","r+") as file:
        file_data = json.load(file)
        for artist_dic in file_data["artist"]:
            if artist_dic["name"] == artist:
                return "Artist is already in artist bank"
            
            
    response = google_images_download.googleimagesdownload()   
    
    arguments = {"keywords":artist,
                 "limit":1,
                 "print_urls":True, 
                 "output_directory": "Artist",
                 "no_directory": True,
                 }   

    paths = response.download(arguments)   
    os.rename(str(paths[0][artist][0]),f'Artist/{artist}.png')
    
    return "Artist added"


# note this function was only ever ran once (already ran by jeff)
# because it was used as a way to mass add picture of music artist
# by scanning the songs.json file. After this function was ran
# a command that allows admins to add artist was implemented, 
# so this function shouldn't be used, its here to look cool 
"""
if __name__=="__main__":
    
    artist_list = []
    
    songs_dic = open("songs.json","r")
    songs_dic_data = json.load(songs_dic)
    for song_dic in songs_dic_data["songs"]:
        if song_dic["artist"] not in artist_list:
            artist_list.append(song_dic["artist"])
    songs_dic.close()
    
    
    
    for artist in artist_list:
            
        with open("artist.json","r+") as file:
            file_data = json.load(file)
            artist_dic = {
                "name": artist,
                "path": f"Artist/{artist}"
            }
            
            file_data["artist"].append(artist_dic)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
"""
 
        
    
    


