import discord
from helper_functions import username_in_list
from game import Game
from user import User
from discord.ext import commands

TOKEN = 'ODc5MzgzOTg1Nzg3MTMzOTcy.YSO8KA.rKBBRrUI0ewQv6TYejpTaNQN7LI'
client = commands.Bot(command_prefix='%')

users = []
game = Game()

@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    username = str(message.author).split('#')[0]
    user_message = str(message.content).split(' by ')

    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    try:
        print(f'{user_message[0]}, {user_message[1]}')
    except:
        pass

    if message.author == client.user: # bot doesn't respond to itself

        return

    if message.channel.name == 'quiz-room':

        try:

            if user_message[0].lower() == game.current_song_name() and user_message[1].lower() == game.current_song_artist():
                await message.channel.send(f'{username} has guessed the correct song and artist! +20 points')

            elif user_message[1].lower() == game.current_song_artist():
                await message.channel.send(f'{username} has guessed the correct artist, but not the correct song! +5 points')
        
        except:

            if user_message[0].lower() == game.current_song_name():
                await message.channel.send(f'{username} has guessed the correct song, but not the correct artist! +10 points')
            
            elif user_message[0].lower() == game.current_song_artist():
                await message.channel.send(f'{username} has guessed the correct artist, but not the correct song! +5 points')



    await client.process_commands(message)

@client.command()
async def join(ctx):

    username = str(ctx.author).split('#')[0]
    print('Checking')

    if ctx.channel.name == 'lobby' and username_in_list(username, users) == False:

        print('User not in game yet')
        if len(users) == 0:

            users.append(User(username, True))
            await ctx.send(f'{username} (admin) has joined the game!')

        else: 

            users.append(User(username, False))
            await ctx.send(f'{username} has joined the game!')

    elif ctx.channel.name == 'lobby' and username_in_list(username, users) == True:

        await ctx.send(f'{username} has already joined the game!')

        

@client.command()
async def leave(ctx):

    username = str(ctx.author).split('#')[0]

    if ctx.channel.name == 'lobby' and username_in_list(username, users) == False:

        await ctx.send(f'{username} has not joined the game!')
    
    elif ctx.channel.name == 'lobby' and username_in_list(username, users) == True:

        for u in users:

            if u.username == str(ctx.author).split('#')[0]:

                users.remove(u) 
                await ctx.send(f'{username} has left the game!')
                break

        print(users)
       
client.run(TOKEN)