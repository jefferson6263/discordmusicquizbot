import json
from os import remove
import random
from discord.ext import tasks
import discord

def load_songs():

    list = []

    f = open('songs.json', 'r')

    data = json.load(f)

    for i in data['songs']:

        list.append(i)

    random.shuffle(list)

    return list

class Game:

    def __init__(self, users, ctx):

        self.active = False
        self.mode = 0
        self.round = 0
        self.songs = load_songs()
        self.current = self.songs.pop(0)
        self.timer = 30
        self.users = users
        self.ctx = ctx

        print(self.current)
    
    @tasks.loop(seconds=1.0)
    async def start_timer(self):

        channel = discord.utils.get(self.ctx.guild.channels, name="quiz-room")
        self.timer -= 1

        if self.timer == 30:

            bot_message = discord.Embed(
                title = 'Round 1: Guess the Song (Audio)',
                description = "You will be played a short audio clip.\n Guess the song and artist using the format: 'song' by 'artist'\n e.g diamonds by rihanna",
                colour = 0x00A2FF
            )

        elif self.timer >= 10 and self.timer % 5 == 0:

            bot_message = discord.Embed(
                title = 'Timer',
                description = f'{self.timer} seconds left!',
                colour = 0x00A2FF
            )
        
        elif self.timer > 0 and self.timer < 10:

            bot_message = discord.Embed(
                title = 'Timer',
                description = f'{self.timer} seconds left!',
                colour = 0x00A2FF
            )
        
        elif self.timer <= 0:
            
            song_name = self.current_song_name().title()
            song_artist = self.current_song_artist().title()

            bot_message = discord.Embed(
                title = "Time's Up!",
                description = f'The answer was {song_name} by {song_artist}!',
                colour = 0x00A2FF
            )

            bot_message.add_field(name='Leaderboard', value=self.leaderboard(), inline=False)

            self.next_song()
            self.timer = 30

        try:
            await channel.send(embed = bot_message)
        except:
            pass

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

    def next_song(self):

        self.current = self.songs.pop(0)

    def leaderboard(self):

        sorted_users = sorted(self.users, key=lambda x: x.points, reverse=True)
        leaderboard_string = ""

        for count, user in enumerate(sorted_users):

            leaderboard_string += f"{count+1}. {user.username}: {user.points} points\n"

        return leaderboard_string
    
    def add_points(self, username, points):

        for user in self.users:
            
            print(f"user.username={user.username}| username={username}")
            if user.username == username:

                print("added points")
                user.points += points
                break

           
    
    def get_users(self):

        return self.users
