import json
import random
from discord.ext import tasks
import discord
from play_song import play_song

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
        self.question = 0
        self.songs = load_songs()
        self.current = self.songs.pop(0)
        self.timer = 30
        self.users = users
        self.ctx = ctx
        self.vc = None

        print(self.current)
    
    @tasks.loop(seconds=1.0)
    async def start_timer(self):

        if self.active == False:
    
            self.start_timer.stop()

        channel = discord.utils.get(self.ctx.guild.channels, name="quiz-room")

        if self.mode == 0 and self.timer == 30:

            await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")
            if self.question == 0:
                bot_message = discord.Embed(
                    title = 'Round 1: Guess the Song (Audio)\n',
                    description = 'You will be played a short audio clip.\n Guess the song and artist using the format:\n song by artist e.g diamonds by rihanna',
                    colour = 0x00A2FF
                )
                await channel.send(embed = bot_message)

            if self.timer == 30:
                bot_message = discord.Embed(
                    title = f'Question {self.question+1} (Audio)',
                    colour = 0x00A2FF
                )
                await channel.send(embed = bot_message)

            self.timer -= 1

        elif self.timer > 0:

            await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")
            self.timer -= 1
        
        elif self.timer <= 0:
            
            await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")

            song_name = self.current_song_name().title()
            song_artist = self.current_song_artist().title()

            bot_message = discord.Embed(
                title = "Time's Up!",
                description = f'The answer was {song_name} by {song_artist}',
                colour = 0x00A2FF
            )

            bot_message.add_field(name='Leaderboard\n', value=self.leaderboard(), inline=False)

            await channel.send(embed = bot_message)

            self.reset_user_guesses()
            self.next_song()

            if self.question < 10:

                self.question += 1

                if self.mode == 0:
                    await self.vc.disconnect()
                    self.vc = await play_song(self.current, self.ctx)

            else: # currently ends the game, but can add more modes later
                
                self.question = 0
                '''
                self.mode += 1
                '''

                winner = sorted(self.users, key=lambda x: x.points, reverse=True)[0]

                bot_message = discord.Embed(
                    title = "Game has Finished!",
                    description = f'The winner is {winner} with {winner.points} points!',
                    colour = 0x00A2FF
                )

                bot_message.add_field(name='Final Leaderboard\n', value=self.leaderboard(), inline=False)
                
                await self.vc.disconnect()

            self.timer = 30
        
        else: 

            self.timer -= 1

    def get_timer(self):

        return self.timer

    def is_active(self):

        return self.active
    
    async def start_game(self):

        self.active = True
        self.start_timer.start()
        self.vc = await play_song(self.current, self.ctx)
    
    def stop_game(self):
    
        self.active = False
        self.start_timer.stop()
        self.vc 

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
    
    def get_users(self):

        return self.users

    def get_user(self, username):

        for user in self.users:

            if user.username == username:

                return user

    def reset_user_guesses(self):

        for user in self.users:

            user.set_guessed_song(False)
            user.set_guessed_artist(False)
            user.set_guessed_album(False)

