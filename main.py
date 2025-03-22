import discord
import os
import sys
from dotenv import load_dotenv
from gloss import easyGloss
from gloss import hardGloss
from gloss import printRootInfo
from gloss import printAffixInfo
from misc import ipaV4
from misc import getCategory
from misc import getHelp
from misc import findv4Words

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

def reload():
  python = sys.executable
  os.execl(python, python, *sys.argv)
  
def correct(word):
  word = word.replace("ş", "ș")
  word = word.replace("ı", "i")
  word = word.replace("’", "\'")
  word = word.replace("ʼ", "\'")
  word = word.replace("ļ", "ḷ")
  word = word.lower()
  return word

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name=".help for info"))

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
        if i[-1] == '\\':
          gloss += '**'+i+' **: ' + easyGloss(i) + '\n'
        else:
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

    elif message.content.startswith('.!reload'):
      await message.channel.send('Successfully reloaded external resources.')
      reload()

    elif message.content.startswith('?meaning '):
      argument = message.content.removeprefix('?meaning ')
      await message.channel.send(getCategory(argument))

    elif message.content.startswith('.help'):
      await message.author.send(getHelp('TXT'))
      
    elif message.content.startswith('?ipa '):
      ipa = '/'
      argument = message.content.removeprefix('?ipa ')
      args = argument.split()
      for i in args:
        ipa += ipaV4(correct(i)) + ' '
      ipa = ipa[:-1]
      ipa += '/'
      await message.channel.send(ipa)

    elif message.content.startswith('?find '):
      argument = 'zxcvbnm'
      argument = message.content.removeprefix('?find ')
      await message.channel.send(findv4Words(argument))

client.run(TOKEN)
