from os import remove
import discord
from helper_functions import username_in_list, remove_leading_and_trailing_spaces
from game import Game
from user import User
from discord.ext import commands
from add_song import addSong

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
    user_message = str(message.content).split('by')
    user_message = remove_leading_and_trailing_spaces(user_message)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})') # debug

    for msg in user_message:

        if msg == game.current_song_name() or msg == game.current_song_artist():

            await message.delete()
            break
        
    for msg in user_message: # debug

        print(msg)

    if message.author == client.user: # bot doesn't respond to itself

        return

    if message.channel.name == 'quiz-room':

        try:

            if user_message[0].lower() == game.current_song_name() and user_message[1].lower() == game.current_song_artist():
                bot_message = discord.Embed(
                    description = f'{username} has guessed the correct SONG and ARTIST! +10 points',
                    colour = 0x00FF08
                )

            elif user_message[1].lower() == game.current_song_artist():
                bot_message = discord.Embed(
                    description = f'{username} has guessed the correct SONG! +5 points',
                    colour = 0xFF9B00
                )

            await message.channel.send(embed = bot_message)
        
        except:
            
            if user_message[0].lower() == game.current_song_name():
                bot_message = discord.Embed(
                    description = f'{username} has guessed the correct SONG! +5 points',
                    colour = 0xFF9B00
                )
            
            elif user_message[0].lower() == game.current_song_artist():
                bot_message = discord.Embed(
                    description = f'{username} has guessed the correct ARTIST! +5 points',
                    colour = 0xFF9B00
                )

            await message.channel.send(embed = bot_message)

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
        

@client.command(name='helpmenu',help='displays help menu')
async def help(ctx):
        
    helpmenu = discord.Embed(
        title = "Help Menu for Dummies",
        description = f"Welcome to Jono and Jeff's Music Trivia Bot!! Here is a quick guide.",
        colour = 0x2F329F
    )

    helpmenu.add_field(name='How it works', value="In this Trivia you will be tested in 4 different categories, Audio, Artist, Album Cover and Lyrics.", inline=False)
    helpmenu.add_field(name='Audio', value="In this Category you will be played a short audio clip and you will have identify the Song Name and/or Artist. Bonus marks if you get both!!", inline=False)
    helpmenu.add_field(name='Artist', value="In this Category you will be shown a picture of a music Artist and you will have to identify them.", inline=False)
    helpmenu.add_field(name='Album Cover', value="In this Category you will be shown a picture of an Album Cover and you will have to identify the Album name and/or Artist.", inline=False)
    helpmenu.add_field(name='Lyrics', value="In this Category you will be shown lyrics from a song and you will have identify the Song Name and/or Artist. Bonus marks if you get both!!", inline=False)
    helpmenu.add_field(name='How to Answer', value="You answer questions simply by typing in the quiz-room chat when a game is active. When answering questions that require a song name and artist, make sure to include a 'by' between the song name and artist to make sure you get bonus marks. Eg: diamonds by rihanna.", inline=False)
    helpmenu.add_field(name='How do I gain points?', value="You gain points by typing the correct answer in the quiz-room chat. Points are allocated on a first come first served basis.", inline=False)
    await ctx.message.channel.send(embed = helpmenu)
        

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


@client.command(name='addsong',help='add a song to the song bank')
async def add(ctx):
    addsong = addSong(ctx)
    await addsong.add()
       
client.run(TOKEN)