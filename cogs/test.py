#Imports
from discord.ext import commands


#Define Class
class Test(commands.Cog):
  #Initiazlise
  def __init__(self, client):
    self.client = client

  #Commands
  @commands.command(name="ping")
  async def pingcmd(self, ctx):
    await ctx.send(ctx.author.mention)


#Setup
async def setup(client):
  await client.add_cog(Test(client=client))
