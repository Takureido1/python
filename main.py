import discord
import os
from dotenv import load_dotenv
from gloss import easyGloss
from gloss import hardGloss
from gloss import printRootInfo
from gloss import printAffixInfo

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)


def correct(word):
  word = word.replace("ş", "ș")
  word = word.replace("ı", "i")
  word = word.replace("’", "\'")
  word = word.lower()
  print(word)
  return word

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
      return
    if message.content.startswith('.gloss '):
      gloss = ''
      argument = message.content.removeprefix('.gloss ')
      args = argument.split()
      for i in args:
        i = correct(i)
        gloss += '**'+i+'**: ' + easyGloss(i) + '\n'
      print(f'Argument parsed: {argument}')
      await message.channel.send(gloss)
      
    elif message.content.startswith('.full '):
      gloss = ''
      argument = message.content.removeprefix('.full ')
      args = argument.split()
      for i in args:
        gloss += '**'+i+'**: ' + hardGloss(i) + '\n'
      print(f'Argument parsed: {argument}')
      await message.channel.send(gloss)
      
    elif message.content.startswith('.root '):
      argument = message.content.removeprefix('.root ')
      await message.channel.send(printRootInfo(argument))
      
    elif message.content.startswith('.affix '):
      argument = message.content.removeprefix('.affix ')
      await message.channel.send(printAffixInfo(argument))

client.run(TOKEN)
