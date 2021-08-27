from helper_functions import is_user_admin
import os
import youtube_dl
import urllib.parse, urllib.request, re
import requests
from bs4 import BeautifulSoup
from helper_functions import is_user_admin
import re
from json import dumps, dump

song_dic = {
    "name": "test", 
    "artist": "test",
    "lyrics": "blah blah blah",    
    "link": "test"
}

with open("songs.json", "w") as file:
    dump(song_dic, file)