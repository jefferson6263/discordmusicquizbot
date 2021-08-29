import json
import random
from discord.ext import tasks
import discord
from play_song import play_song

NUM_QUESTIONS = 20
TIMER_LENGTH = 30

def load_songs():

    list = []

    f = open('songs.json', 'r')

    data = json.load(f)

    for i in data['songs']:

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

                if channel.name == 'lobby' or channel.name == 'add-songs' or channel.name == 'General' or channel.name == 'welcome':

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

                    if self.question >= NUM_QUESTIONS-1: # change this when adding more modes

                        winner = sorted(self.users, key=lambda x: x.points, reverse=True)[0]

                        bot_message = discord.Embed(
                            title = "Game has Finished!",
                            description = f'The winner is {winner.username} with {winner.points} points!',
                            colour = 0x00A2FF
                        )

                        bot_message.add_field(name='Final Leaderboard\n', value=self.leaderboard(), inline=False)
                        await channel.send(embed = bot_message)

            if self.timer > 0:

                await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")

                if self.all_answered() == True: # question ends if all users have guessed correctly

                    self.timer = 0

                else:

                    self.timer -= 1
            
            elif self.timer <= 0:
                
                await self.ctx.guild.me.edit(nick=f"{self.timer} seconds left!")

                self.reset_user_guesses()
                self.next_song()

                if self.question < NUM_QUESTIONS-1:

                    self.question += 1

                    if self.mode == 0:
                        await self.vc.disconnect()
                        self.vc = await play_song(self.current, self.ctx)

                    self.timer = TIMER_LENGTH

                else: # currently ends the game, but can add more modes later
                    
                    self.question = 0
                    '''
                    self.mode += 1
                    '''

                    await self.ctx.guild.me.edit(nick=f"Game Finished!")
                    await self.vc.disconnect()
                    self.active = False
            
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

            if self.mode == 0:

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

