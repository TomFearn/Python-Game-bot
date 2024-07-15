#Rock Paper Scissors
#imports
import random
from discord.ext import commands
import discord
import asyncio

#misc
rps_outcomes = ["🌑", "🧻", "✂️"]

class exitError(Exception): pass

def determine_winner(user_choice, computer_choice):
  if user_choice == computer_choice:
      return "It's a tie!"
  elif (user_choice == "🌑" and computer_choice == "✂️") or \
       (user_choice == "🧻" and computer_choice == "🌑") or \
       (user_choice == "✂️" and computer_choice == "🧻"):
      return "You win!"
  else:
      return "I win!"

#Define Class
class Game(commands.Cog):
  
  def __init__(self, client):
    self.client = client
  
  #commands
  @commands.command(name="rps")
  async def rpsEmbed(self, ctx):
    embed = discord.Embed(title="RPS", description="Starting.....")
    msg = await ctx.send(embed=embed)

    try:
      while True:
        embed = discord.Embed(title="RPS", 
                              description="Rock, Paper, Scissors.....", 
                              color=0x8f12e3)
        embed.set_footer(text='Press \"❌\" to quit.')
        await msg.edit(embed=embed)
        
        emojis = ["🌑", "🧻", "✂️", "❌"]
        for emoji in emojis:
          await msg.add_reaction(emoji)
          
        while True:
          response, user = await self.client.wait_for('reaction_add', timeout=60)
          if response.emoji == "❌" and user == ctx.message.author:
            raise exitError
          elif response.emoji in emojis and user == ctx.message.author:
            break

        outcome = random.choice(rps_outcomes)
        embed = discord.Embed(title="RPS", 
        description=f'I choose {outcome}, {determine_winner(response.emoji, outcome)}', 
        color=0x8f12e3)
        await msg.edit(embed=embed)
        
        await asyncio.sleep(7)
        await msg.clear_reactions()
    
    except exitError:
      await ctx.send("I had fun playing!", delete_after=7)
    except asyncio.exceptions.TimeoutError:
      await ctx.send("You took too long to respond.", delete_after=7)
    finally:
      await msg.delete()
      await ctx.message.delete()
      

#Setup
async def setup(client):
  await client.add_cog(Game(client=client))