from os import remove
import discord
from helper_functions import username_in_list, remove_leading_and_trailing_spaces, is_user_game_leader
from game import Game
from user import User
from discord.ext import commands
from add_song import addSong

intents = discord.Intents.default()
intents.members = True

TOKEN = 'ODc5MzgzOTg1Nzg3MTMzOTcy.YSO8KA.rKBBRrUI0ewQv6TYejpTaNQN7LI'
client = commands.Bot(command_prefix='%', intents = intents)

users = []
game = None

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

    if message.author == client.user: # bot doesn't respond to itself

        return

    for msg in user_message: # debug

        print(msg)

    if game != None:

        for msg in user_message:

            if msg == game.current_song_name() or msg == game.current_song_artist():

                await message.delete()
                break

        if message.channel.name == 'quiz-room':

            user = game.get_user(username)

            try:

                if user_message[0].lower() == game.current_song_name() and user_message[1].lower() == game.current_song_artist():
                    
                    if user.get_guessed_artist() == False and user.get_guessed_song() == False:
                        
                        points = game.get_timer()
                        user.add_points(points)
                        user.set_guessed_song(True)
                        user.set_guessed_artist(True)

                        bot_message = discord.Embed(
                            description = f'{username} has guessed the correct SONG and ARTIST! +{points:.1f} points',
                            colour = 0x00FF08
                        )

                        await message.channel.send(embed = bot_message)
                        await message.author.edit(nick=f"[{user.get_points():.1f}] {username}")

                elif user_message[1].lower() == game.current_song_artist() and user.get_guessed_artist() == False:
                    
                    points = game.get_timer() / 2
                    user.add_points(points)
                    user.set_guessed_artist(True)

                    bot_message = discord.Embed(
                        description = f'{username} has guessed the correct ARTIST! +{points:.1f} points',
                        colour = 0xFF9B00
                    )

                    await message.channel.send(embed = bot_message) 
                    await message.author.edit(nick=f"[{user.get_points():.1f}] {username}")
            
            except:

                if user_message[0].lower() == game.current_song_name() and user.get_guessed_song() == False:

                    points = game.get_timer() / 2
                    user.add_points(points)
                    user.set_guessed_song(True)

                    bot_message = discord.Embed(
                        description = f'{username} has guessed the correct SONG! +{points:.1f} points',
                        colour = 0xFF9B00
                    )

                    await message.channel.send(embed = bot_message)
                    await message.author.edit(nick=f"[{user.get_points():.1f}] {username}")
                
                elif user_message[0].lower() == game.current_song_artist() and user.get_guessed_artist() == False:

                    points = game.get_timer() / 2
                    user.add_points(points)
                    user.set_guessed_artist(True)

                    bot_message = discord.Embed(
                        description = f'{username} has guessed the correct ARTIST! +{points:.1f} points',
                        colour = 0xFF9B00
                    )

                    await message.channel.send(embed = bot_message)
                    await message.author.edit(nick=f"[{user.get_points():.1f}] {username}")

    await client.process_commands(message)

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
    skip.add_field(name='Album Cover', value="In this Category you will be shown a picture of an Album Cover and you will have to identify the Album name and/or Artist.", inline=False)
    skip.add_field(name='Lyrics', value="In this Category you will be shown lyrics from a song and you will have identify the Song Name and/or Artist. Bonus marks if you get both!!", inline=False)
    skip.add_field(name='How to Answer', value="You answer questions simply by typing in the quiz-room chat when a game is active. When answering questions that require a song name and artist, make sure to include a 'by' between the song name and artist to make sure you get bonus marks. Eg: diamonds by rihanna.", inline=False)
    skip.add_field(name='How do I gain points?', value="You gain points by typing the correct answer in the quiz-room chat. Points are allocated on a first come first served basis.", inline=False)
    await ctx.message.channel.send(embed = skip)
        

@client.command()
async def join(ctx):

    username = str(ctx.author).split('#')[0]
    member = ctx.message.author
    role = discord.utils.get(ctx.guild.roles, name = 'Joined Players')

    print('Checking')

    if ctx.channel.name == 'lobby' and username_in_list(username, users) == False:

        print('User not in game yet')
        if len(users) == 0:

            users.append(User(username, True))
            bot_message = discord.Embed(
                title = 'Leader has Joined',
                description = f'{username} (Leader) has joined the game!',
                colour = 0x00FF08
            )

            await member.edit(nick=f"👑 [0.0] {username}")
        else: 

            users.append(User(username, False))
            bot_message = discord.Embed(
                title = 'Player has Joined',
                description = f'{username} has joined the game!',
                colour = 0x00FF08
            )

            await member.edit(nick=f"[0.0] {username}")

        await ctx.send(embed = bot_message)
        await member.add_roles(role)
        

    elif ctx.channel.name == 'lobby' and username_in_list(username, users) == True:

        bot_message = discord.Embed(
                title = 'Player Already Joined',
                description = f'{username} has already joined the game!',
                colour = 0x00FF08
            )

        await ctx.send(embed = bot_message)
        

@client.command()
async def leave(ctx):

    username = str(ctx.author).split('#')[0]
    member = ctx.message.author
    role = discord.utils.get(ctx.guild.roles, name = 'Joined Players')

    if ctx.channel.name == 'lobby' and username_in_list(username, users) == False:
        
        bot_message = discord.Embed(
            title = 'Error',
            description = f'{username} has not joined the game!',
            colour = 0xFF0000
        )
        
        await ctx.send(embed = bot_message)
    
    elif ctx.channel.name == 'lobby' and username_in_list(username, users) == True:

        for u in users:

            if u.username == str(ctx.author).split('#')[0]:

                users.remove(u) 
                bot_message = discord.Embed(
                    title = 'Player has Left',
                    description = f'{username} has left the game!',
                    colour = 0xFF0000
                )
                break

        await ctx.send(embed = bot_message) 
        await member.remove_roles(role)
        await member.edit(nick=f"{username}")

        print(users)
    
@client.command()
async def players(ctx):

    if ctx.channel.name == 'lobby':

        string = ""

        if game == None: # if game hasn't started
            for i in users:

                if i.leader:
                    string += f"• {i.username} (Leader)\n"
                else:
                    string += f"• {i.username}\n"
        else: # if games has started
            for i in game.get_users():

                if i.leader:
                    string += f"• {i.username} (Leader)\n"
                else:
                    string += f"• {i.username}\n"
            
        if len(string) == 0:

            string = "No players have joined yet!\n"

        bot_message = discord.Embed(
            title = 'Joined Players',
            description = string,
            colour = 0x00A2FF
        )

        await ctx.send(embed = bot_message)

@client.command()
async def start(ctx):
    global users, game

    if ctx.channel.name == 'lobby' and is_user_game_leader(ctx.author, users) == True:

        game = Game(users, ctx)
    
        bot_message = discord.Embed(
            title = 'Game has Started!',
            description = "Move to the text channel 'quiz-room' to play\n",
            colour = 0x00A2FF
        )

        await ctx.send(embed = bot_message)
        await ctx.guild.create_text_channel('quiz-room')

        game.start_game()

@client.command(name='addsong',help='add a song to the song bank')
async def add(ctx):
    addsong = addSong(ctx)
    await addsong.add()

@client.command()
async def reset(ctx):

    admin_role = discord.utils.get(ctx.guild.roles, name = 'Admin')

    if admin_role in ctx.author.roles:

        if game != None:

            game.stop_game()

        channel = discord.utils.get(ctx.guild.channels, name="quiz-room")
        role = discord.utils.get(ctx.guild.roles, name = 'Joined Players')

        if channel != None:
            await channel.delete()
        else:
            print("Channel 'quiz room' doesn't exist")

        members = await ctx.guild.fetch_members().flatten() # fetches all guild members and then flattens into a list of member objects

        for member in members:

            if member.id != ctx.guild.owner_id: # bot can't change details of guild owner

                await member.edit(nick=member.name)
                await member.remove_roles(role)

        await ctx.me.edit(nick=ctx.me.name)

client.run(TOKEN)

