from helper_functions import is_user_admin
import os
import youtube_dl
import urllib.parse, urllib.request, re
import requests
from bs4 import BeautifulSoup
from helper_functions import is_user_admin
import re
import json

song_dic = {
    "name": "test", 
    "artist": "test",
    "lyrics": "blah blah blah",    
    "link": "test"
}

with open("songs.json","r+") as file:
    file_data = json.load(file)
    file_data["songs"].append(song_dic)
    print(file_data["songs"])
    file.seek(0)
    json.dump(file_data, file, indent = 4)