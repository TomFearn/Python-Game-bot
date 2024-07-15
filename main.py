#Imports
import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionAlreadyLoaded, ExtensionNotLoaded

#Set Intents and Client
intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


#Load Cog
@client.command(name="load", aliases=["l"])
@commands.is_owner()
async def load(ctx, extension):
  try:
    await client.load_extension(f"cogs.{extension}")
  except ExtensionNotFound:
    await ctx.send(f"Could not find {extension}")
  except ExtensionAlreadyLoaded:
    await ctx.send(f"{extension} is already loaded")
  else:
    await ctx.send(f"Loaded {extension}")


#Unload Cog
@client.command(name="unload", aliases=["u"])
@commands.is_owner()
async def unload(ctx, extension):
  try:
    await client.unload_extension(f"cog.{extension}")
  except ExtensionNotFound:
    await ctx.send(f"Could not find {extension}")
  except ExtensionNotLoaded:
    await ctx.send(f"{extension} is already unloaded")
  else:
    await ctx.send(f"Unloaded {extension}")


#Reload Cog
@client.command(name="reload", aliases=["r"])
@commands.is_owner()
async def reload(ctx, extension):
  try:
    await client.reload_extension(f"cog.{extension}")
  except ExtensionNotFound:
    await ctx.send(f"Could not find {extension}")
  except ExtensionNotLoaded:
    await client.load_extension(f"cog.{extension}")
    await ctx.send(f"{extension} was already unloaded")
    await ctx.send(f"Loaded {extension}")
  else:
    await ctx.send(f"Reloaded {extension}")


#Load All Cogs
@client.command(name="loadall", aliases=["la"])
@commands.is_owner()
async def loadAll(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await client.load_extension(f"cogs.{filename[:-3]}")
      except ExtensionNotFound:
        pass
      except ExtensionAlreadyLoaded:
        pass
  await ctx.send("Loaded all cogs")


#Unload All Cogs
@client.command(name="unloadall", aliases=["ua"])
@commands.is_owner()
async def unloadAll(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await client.unload_extension(f"cogs.{filename[:-3]}")
      except ExtensionNotFound:
        pass
      except ExtensionNotLoaded:
        pass
  await ctx.send("Unloaded all cogs")


#Reload All Cogs
@client.command(name="reloadall", aliases=["ra"])
@commands.is_owner()
async def reloadAll(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await client.reload_extension(f"cogs.{filename[:-3]}")
      except ExtensionNotFound:
        pass
      except ExtensionNotLoaded:
        await client.load_extension(f"cogs.{filename[:-3]}")
  await ctx.send("Reloaded all cogs")


#Run on Bot Start
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  #Load All Cogs on Start
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await client.load_extension(f"cogs.{filename[:-3]}")
      except ExtensionNotFound:
        pass
      except ExtensionAlreadyLoaded:
        pass


#Start Bot
client.run(os.environ['token'])
