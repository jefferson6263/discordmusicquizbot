import json
import random

def load_songs():

    list = []

    f = open('songs.json', 'r')

    data = json.load(f)

    for i in data['songs']:

        list.append(i)

    random.shuffle(list)

    return list

class Game:

    def __init__(self):

        self.active = False
        self.mode = 0
        self.songs = load_songs()
        self.current = self.songs.pop(0)

        print(self.current)

    def current_song_name(self):

        return self.current['name']

    def current_song_artist(self):

        return self.current['artist']

    def change_current_song(self):

        self.current = self.songs.pop(0)
    