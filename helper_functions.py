import discord
from discord import message
from discord.utils import get

def username_in_list(user, list):

    for i in list:

        if i.username == user:

            return True

    return False

def remove_leading_and_trailing_spaces(list):

    modified_list = []

    for i in list:

        str = i.strip()

        modified_list.append(str)
    
    return modified_list


def is_user_admin(ctx):
    user = ctx.message.author
    
    role = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
    print(role)
    print(user.roles)
    if role in user.roles:
        return True
    else:
        return False

def is_user_game_leader(user, users):

    username = user.name

    for i in users:

        if i.username == username and i.is_leader() == True:

            return True

    return False



    


        