import discord
from helper_functions import username_in_list
from user import User
from discord.ext import commands

TOKEN = 'ODc5MzgzOTg1Nzg3MTMzOTcy.YSO8KA.rKBBRrUI0ewQv6TYejpTaNQN7LI'
client = commands.Bot(command_prefix='%')

users = []

@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user: # bot doesn't respond to itself

        return

    if message.channel.name == 'quiz':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello {username}!')
            return

        elif user_message.lower() == 'goodbye':
            await message.channel.send(f'Goodbye {username}!')

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
        

@client.command(name='test',help='displays help menu')
async def help(ctx):
        
    skip = discord.Embed(
        title = "Help Menu for Dummies",
        description = f"Welcome to Jono and Jeff's Music Trivia Bot!! Here is a quick guide.",
        colour = 0x2F329F
    )

    skip.add_field(name='How it works', value="In this Trivia you will be tested in 4 different categories, Audio, Artist, Album Cover and Lyrics.", inline=False)
    skip.add_field(name='Audio', value="In this Category you will be played a short audio clip and you will have identify the Song Name and/or Artist. Bonus marks if you get both!!", inline=False)
    skip.add_field(name='Artist', value="In this Category you will be shown a picture of a music Artist and you will have to identify them.", inline=False)
    skip.add_field(name='Album Cover', value="In this Category you will be shown a picture of an Album Cover and you will have to identify the album.", inline=False)
    skip.add_field(name='Lyrics', value="In this Category you will be shown lyrics from a song and you will have identify the Song Name and/or Artist. Bonus marks if you get both!!", inline=False)
    skip.add_field(name='How to Answer', value="You answer questions simply by typing in the quiz-room chat when a game is active. When answering questions that require a song name and artist, make sure to include a 'by' between the song name and artist to make sure you get bonus marks. Eg: Diamonds by Rihanna.", inline=False)
    skip.add_field(name='How do I gain points?', value="You gain points by typing the correct answer in the quiz-rrom chat. Points are allocated on a first come first served basis.", inline=False)
    await ctx.message.channel.send(embed = skip)
        

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