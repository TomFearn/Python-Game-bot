#Swindlestones
#Imports
import random
import discord
from discord.ext import commands
import asyncio

#misc


class exitError(Exception):
  pass


#roll dice
def roll_Dice(num_sides: int, num_dice: int):
  dice = []
  while len(dice) < num_dice:
    dice.append(random.randint(1, num_sides))
  dice.sort()
  return dice


#call
def call(player_amount, player_face, bot_amount, bot_face, total):
  player_bet = player_amount*10 + player_face
  bot_bet = bot_amount*10 + bot_face

  if player_bet > bot_bet:
    check_hand = total.count(player_face)
    if check_hand >= player_amount:
      return 0, 1
    else:
      return 1, 0
  else:
    check_botHand = total.count(bot_face)
    if check_botHand >= bot_amount:
      return 1, 0
    else:
      return 0, 1


#Define Class
class Gamble(commands.Cog):

  def __init__(self, client):
    self.client = client

  #commands

  @commands.command(name="ss", aliases=["SwindleStones"])
  async def ssEmbed(self, ctx):
    embed = discord.Embed(title="Swindle Stones", description="Starting.....")
    msg = await ctx.send(embed=embed)

    player_dice = 5
    bot_dice = 5

    emojis = ["🔺", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "🔻", "🤥", "❌"]
    for emoji in emojis:
      await msg.add_reaction(emoji)

    bot_dieFace = None
    bot_dieAmount = None
    die_face = 0
    die_amount = 1

    try:
      while (player_dice >= 0 and bot_dice >= 0):

        player_hand = roll_Dice(4, player_dice)
        bot_hand = roll_Dice(4, bot_dice)
        total_hand = player_hand + bot_hand

        playerScore = 0
        botScore = 0

        while playerScore == 0 and botScore == 0:
        
          while True:
  
            embed = discord.Embed(
                title="Swindle Stones",
                description=
                f"Your hand: {player_hand}, Number of selected die: {die_amount}x🎲\nChoose the number of dice with: \"🔺\" or \"🔻\",\nthen select a face number to make the bet.\nCall opponents bet with 🤥."
                + (f'\nOpponent bets: {bot_dieAmount}x🎲 {bot_dieFace}\'s.'
                   if bot_dieFace else '') 
                + (f'\nYour dice: {player_dice}x🎲 Oponents dice: {bot_dice}x🎲.'),
              
                color=15844367)
            embed.set_footer(text='Press \"❌\" to quit.')
            await msg.edit(embed=embed)
  
            response, user = await self.client.wait_for('reaction_add',
                                                        timeout=120)
            if response.emoji == "❌" and user == ctx.message.author:
              raise exitError
            elif response.emoji == "🔻" and user == ctx.message.author:
              await msg.remove_reaction(response, user)
              if die_amount > 1:
                die_amount -= 1
            elif response.emoji == "🔺" and user == ctx.message.author:
              await msg.remove_reaction(response, user)
              if die_amount < (player_dice + bot_dice):
                die_amount += 1
            elif response.emoji == "🤥" and user == ctx.message.author:
              await msg.remove_reaction(response, user)
              
              playerScore, botScore = call(die_amount, die_face, bot_dieAmount, bot_dieFace, total_hand)
              player_dice -= playerScore
              bot_dice -= botScore
  
              embed = discord.Embed(
                title="Swindle Stones",
                description=f"**Call!**\nYour hand: {player_hand}, Opponents hand: {bot_hand}\n"
                +(f"You Won!" if not playerScore else f"Oponent Won!"),
                color=15844367)
  
              await msg.edit(embed=embed)
              await asyncio.sleep(8)
              bot_dieFace = None
              bot_dieAmount = None
              die_face = 0
              die_amount = 1
              break
              
            elif response.emoji in emojis and user == ctx.message.author:
              await msg.remove_reaction(response, user)
              die_face = emojis.index(response.emoji)
              break
  

          
          if die_amount > (player_dice + bot_dice) / 2 + 1:
            playerScore, botScore = call(die_amount, die_face, bot_dieAmount, bot_dieFace, total_hand)
            player_dice -= playerScore
            bot_dice -= botScore
            
            embed = discord.Embed(
              title="Swindle Stones",
              description=f"**Call!**\nYour hand: {player_hand}, Opponents hand: {bot_hand}\n"
              +(f"You Won!" if not playerScore else f"Oponent Won!"),
              color=15844367)
            
            await msg.edit(embed=embed)
            await asyncio.sleep(8)

            bot_dieFace = None
            bot_dieAmount = None
            die_face = 0
            die_amount = 1
          
          else:
            if (die_amount + 1) <= (player_dice + bot_hand.count(die_face)):
              bot_dieAmount = die_amount
              bot_dieFace = die_face
              bot_dieAmount += 1
            elif die_face < 4:
              bot_dieAmount = die_amount
              bot_dieFace = die_face
              bot_dieFace += 1
            else:
              playerScore, botScore = call(die_amount, die_face, bot_dieAmount, bot_dieFace, total_hand)
              player_dice -= playerScore
              bot_dice -= botScore
  
              embed = discord.Embed(
                title="Swindle Stones",
                description=f"**Call!**\nYour hand: {player_hand}, Opponents hand: {bot_hand}\n"
                +(f"You Won!" if not playerScore else f"Oponent Won!"),
                color=15844367)
  
              await msg.edit(embed=embed)
              await asyncio.sleep(8)

              bot_dieFace = None
              bot_dieAmount = None
              die_face = 0
              die_amount = 1
            
          
    
      embed = discord.Embed(title="Swindle Stones",
                            description=f"Player Wins the game!" if bot_dice == 0 else f"Bot Wins the game!",
                            color=15844367)
      await msg.edit(embed=embed)
      await asyncio.sleep(5)
    
    except exitError:
      await ctx.send("I had fun playing!", delete_after=7)
    except asyncio.exceptions.TimeoutError:
      await ctx.send("You took too long to respond.", delete_after=7)
    finally:
      await msg.delete()
      await ctx.message.delete()


#Setup
async def setup(client):
  await client.add_cog(Gamble(client=client))

