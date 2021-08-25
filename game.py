import json
import random
from discord.ext import tasks

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
        self.timer = 5

        print(self.current)
    
    @tasks.loop(seconds=1.0)
    async def start_timer(self):

        self.timer -= 1

        if self.timer <= 0:

            self.timer = 5
            self.start_timer.stop()

    def current_timer(self):

        return self.timer

    def is_active(self):

        return self.active
    
    def start_game(self):

        self.active = True
        self.start_timer.start()

    def current_song_name(self):

        return self.current['name']

    def current_song_artist(self):

        return self.current['artist']

    def change_current_song(self):

        self.current = self.songs.pop(0)
    