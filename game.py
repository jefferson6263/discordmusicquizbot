import json
import random
from discord.ext import tasks
import discord
from play_song import play_song

NUM_QUESTIONS = 2
TIMER_LENGTH = 30

def load_songs():

    list = []

    f = open('songs.json', 'r')

    data = json.load(f)

    for i in data['songs']:

        list.append(i)

    random.shuffle(list)
    
    for i in list:

        random.shuffle(i['lyrics'])

        if len(i['lyrics'][0]) > 4000 : # character lyrics for embeds

            i['lyrics'].pop(0)

    return list

def load_artists():

    list = []

    f = open('artist.json', 'r')

    data = json.load(f)

    for i in data['artist']:

        list.append(i)

    random.shuffle(list)

    return list

class Game:
    
    def __init__(self, users, ctx, channels):

        self.active = False
        self.mode = 0
        self.question = 0
        self.songs = load_songs()
        self.current = self.songs.pop(0)
        self.artists = load_artists()
        self.current_artist = self.artists.pop(0)
        self.timer = TIMER_LENGTH
        self.users = users
        self.ctx = ctx
        self.vc = None
        self.channels = channels

        print(self.current)
    
    @tasks.loop(seconds=1.0)
    async def start_timer(self):

        if self.active != False:

            for channel in self.channels:

                if channel.name == 'lobby' or channel.name == 'add-songs' or channel.name == 'General' or channel.name == 'welcome' or channel.name == 'past-games':

                    continue

                if self.mode == 0 and self.timer == TIMER_LENGTH:

                    if self.question == 0:
                        bot_message = discord.Embed(
                            title = 'Round 1: Guess the Song (Audio)\n',
                            description = 'You will be played a short audio clip.\n Guess the song and artist',
                            colour = 0x00A2FF
                        )
                        await channel.send(embed = bot_message)

                    if self.timer == TIMER_LENGTH:
                        bot_message = discord.Embed(
                            title = f'Question {self.question+1} (Audio)',
                            colour = 0x00A2FF
                        )
                        await channel.send(embed = bot_message)

                elif self.mode == 0 and self.timer <= 0:

                    song_name = self.current_song_name().title()
                    song_artist = self.current_song_artist().title()

                    bot_message = discord.Embed(
                        title = "Time's Up!",
                        description = f'The answer was {song_name} by {song_artist}',
                        colour = 0x00A2FF
                    )

                    bot_message.add_field(name='Leaderboard\n', value=self.leaderboard(), inline=False)

                    await channel.send(embed = bot_message)

                elif self.mode == 1 and self.timer == TIMER_LENGTH:

                    if self.question == 0:
                        bot_message = discord.Embed(
                            title = 'Round 2: Guess the Song (Lyrics)\n',
                            description = 'You will be given a section of the lyrics.\n Guess the song and artist',
                            colour = 0x00A2FF
                        )
                        await channel.send(embed = bot_message)

                    if self.timer == TIMER_LENGTH:
                        bot_message = discord.Embed(
                            title = f'Question {self.question+1} (Lyrics)',
                            colour = 0x00A2FF
                        )

                        bot_message.add_field(name = 'Lyrics\n', value = self.current['lyrics'][0])
                        await channel.send(embed = bot_message)

                elif self.mode == 1 and self.timer <= 0:

                    song_name = self.current_song_name().title()
                    song_artist = self.current_song_artist().title()

                    bot_message = discord.Embed(
                        title = "Time's Up!",
                        description = f'The answer was {song_name} by {song_artist}',
                        colour = 0x00A2FF
                    )

                    bot_message.add_field(name='Leaderboard\n', value=self.leaderboard(), inline=False)

                    await channel.send(embed = bot_message)

                elif self.mode == 2 and self.timer == TIMER_LENGTH:

                    if self.question == 0:
                        bot_message = discord.Embed(
                            title = 'Round 3: Guess the artist (Picture)\n',
                            description = 'You will be given a picture of the artist.\n Guess the artist',
                            colour = 0x00A2FF
                        )
                        await channel.send(embed = bot_message)

                    if self.timer == TIMER_LENGTH:
                        bot_message = discord.Embed(
                            title = f'Question {self.question+1} (Picture)',
                            colour = 0x00A2FF
                        )
                        await channel.send(embed = bot_message)

                elif self.mode == 2 and self.timer <= 0:

                    artist = self.current_artist['name']

                    bot_message = discord.Embed(
                        title = "Time's Up!",
                        description = f'The answer was {artist}',
                        colour = 0x00A2FF
                    )

                    bot_message.add_field(name='Leaderboard\n', value=self.leaderboard(), inline=False)

                    await channel.send(embed = bot_message)

                    if self.question >= NUM_QUESTIONS-1 and self.mode == 2: # change this when adding more modes

                        winner = sorted(self.users, key=lambda x: x.points, reverse=True)[0]

                        bot_message = discord.Embed(
                            title = "Game has Finished!",
                            description = f'The winner is {winner.username} with {winner.points} points!',
                            colour = 0x00A2FF
                        )

                        bot_message.add_field(name='Final Leaderboard\n', value=self.leaderboard(), inline=False)
                        await channel.send(embed = bot_message)

                        past_games = discord.utils.get(self.ctx.guild.channels, name = f"past-games")

                        bot_message = discord.Embed(
                            title = "Game has Finished!",
                            description = f'The winner is {winner.username} with {winner.points} points!',
                            colour = 0x00A2FF
                        )

                        bot_message.add_field(name='Final Leaderboard\n', value=self.leaderboard(), inline=False)
                        await past_games.send(embed = bot_message)


            if self.timer > 0:

                await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")

                if self.all_answered() == True: # question ends if all users have guessed correctly
                    print("all answered")
                    self.timer = 0

                else:

                    self.timer -= 1
            
            elif self.timer <= 0:
                
                await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")

                self.reset_user_guesses()

                if self.mode == 0 or self.mode == 1:

                    self.next_song()

                if self.question < NUM_QUESTIONS-1:

                    self.question += 1

                    if self.mode == 0:
                        await self.vc.disconnect()
                        self.vc = await play_song(self.current, self.ctx)

                    self.timer = TIMER_LENGTH

                else: # currently ends the game, but can add more modes later
                    
                    self.question = 0

                    if self.mode == 0:

                        await self.vc.disconnect()
                        self.timer = TIMER_LENGTH

                    elif self.mode == 1:
                        
                        self.timer = TIMER_LENGTH

                    elif self.mode == 2:

                        self.timer = TIMER_LENGTH
                            
                    elif self.mode == 3: # change this when adding more 
                        
                        await self.ctx.guild.me.edit(nick=f"Game Finished!")
                        
                        self.active = False

                    self.mode += 1
                        
            else: 

                self.timer -= 1

        else:

            self.start_timer.stop()

    def get_timer(self):

        return self.timer

    def is_active(self):

        return self.active

    def all_answered(self):

        for user in self.users:

            if self.mode == 0 or self.mode == 1:

                if user.get_guessed_song() == False or user.get_guessed_artist() == False:

                    return False
        
        return True

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

    def next_artist(self):

        self.current_artist = self.artists.pop(0)
    
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

    def get_mode(self):

        return self.mode
    
