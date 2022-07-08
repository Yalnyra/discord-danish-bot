"""
:author: Eugen Vinokur
Simple discord bot designed to respond to users' messages with an certain role with a random gif
"""

import json
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
env_role_list = json.loads(os.environ['ROLE_IDS_LIST'])
env_user_list = json.loads(os.environ['USER_IDS_LIST'])
env_gif_list = json.loads(os.environ['GIF_LIST'])


@client.event
async def on_ready():
    """
    Notify in the console that the bot has started working
    """
    print(f'{client.user} has logged in into the system')

@client.event
async def on_message(message):
    """
    Sends a discord reply to a message by user who has a certain role in this guild
    :param message: the received message
    """
    if message.author == client.user:
        return
    for user_id in env_user_list:
        if message.author.id == user_id:
            await message.add_reaction(":nerd:")
            await message.reply(random.choice(env_gif_list),
                                mention_author=True)
            print(message.author.name + " got pinged!")
            return
    if message.guild:
        member = message.author
    else:
        for joined_guild in client.guilds:
            member = await joined_guild.fetch_member(message.author.id)
            if member:
                for user_role in member.roles:
                    for marked_role_id in env_role_list:
                        if user_role.id == marked_role_id:
                            await message.add_reaction(":nerd:")
                            await message.reply(random.choice(env_gif_list),
                                                mention_author=True)
                            print(member.display_name + " got pinged!")
                            return

    for user_role in member.roles:
        for marked_role_id in env_role_list:
            if user_role.id == marked_role_id:
                await message.add_reaction(":nerd:")
                await message.reply(random.choice(env_gif_list),
                                    mention_author=True)
                print(member.display_name + " got pinged!")
                return

client.run(os.getenv('TOKEN'))
