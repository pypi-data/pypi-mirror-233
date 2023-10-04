import os
import asyncio
import logging
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv() # Loads the environmental variables

PREFIX = os.getenv('PREFIX') # Gets environmental variables from .env file.
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all() # Declaring bot privileges.
bot = commands.Bot(command_prefix=PREFIX, intents=intents) # Creates the bot object with configuration.


async def init(): # Function to be called when collection of commands (cog) are initialized.
    for cog_file in os.listdir('src/cog'):
        if cog_file.endswith(".py"):
            await bot.load_extension(f"cog.{cog_file[:-3]}")


@bot.event # This will log once the bot is running.
async def on_ready():
    logging.info(f"{bot.user.name} is now running!")


@bot.event # Basic error handling.
async def on_command_error(ctx, error):
    if ctx.guild:
        print(f"{ctx.guild.name}:  {error}")


@bot.command()
# @commands.is_owner() // You can add owners by replacing bot = commands.Bot(command_prefix=PREFIX, intents=intents) with
#                                                         bot = commands.Bot(command_prefix=PREFIX, owner_ids=set(OWNERS), intents=intents)
# Set OWNER to a set of user id like [19834138572394, 234681693874622] etc.
async def reload(ctx): # Reload your collection of commands in cog folder (Do !reload if your prefix is '!' etc.)
    for cog_file in os.listdir('src/cog'):
        if cog_file.endswith(".py"):
            await bot.reload_extension(f"cog.{cog_file[:-3]}")
    logging.info(f"{bot.user.name} is now reloaded!")
    await ctx.send(f"{bot.user.name} is now reloaded!")

if __name__ == "__main__": # Main function of your bot.
    asyncio.run(init())
    bot.run(TOKEN, root_logger=True)