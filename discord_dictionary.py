import discord
import requests
from discord.utils import get


global definitions
global active_index
active_index = 0
active_definition = 0
client = discord.Client()
  

#turn on the discord bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#when someone asks for a definition, synonym, or antonym, get the definition and send the appropriate message
@client.event
async def on_message(message):
    words = message.content.split(" ")
    word_id = ' '.join([words[i] for i in range(len(words)) if i != 0])

    if message.author == client.user:
        return

    if message.content.startswith('define') or message.content.startswith('Define'):
        
        definitions = get_oxford_definitions(word_id)

        if definitions is None:
          await message.channel.send("404: Word Not Found")
        else:
          sent = await message.channel.send(definitions[0])
          await sent.add_reaction('⬅️')
          await sent.add_reaction('➡️')
          await sent.add_reaction('🗑️')
    elif message.content.startswith('urban-define') or message.content.startswith('Urban-define'):

        definitions = get_urban_definitions(word_id)

        if definitions is None:
          await message.channel.send("404: Word Not Found")
        else:
          sent = await message.channel.send(definitions[0])
          await sent.add_reaction('⬅️')
          await sent.add_reaction('➡️')
          await sent.add_reaction('🗑️')
    elif message.content.startswith('synonym') or message.content.startswith('Synonym'):

      definitions = get_synonyms(word_id)
      if definitions is None:
        await message.channel.send("404: Word Not Found")
      else:
        sent = await message.channel.send(definitions[0])
        await sent.add_reaction('⬅️')
        await sent.add_reaction('➡️')
        await sent.add_reaction('🗑️')
    elif message.content.startswith('antonym') or message.content.startswith('Antonym'):

      definitions = get_antonyms(word_id)
      if definitions is None:
        await message.channel.send("404: Word Not Found")
      else:
        sent = await message.channel.send(definitions[0])
        await sent.add_reaction('⬅️')
        await sent.add_reaction('➡️')
        await sent.add_reaction('🗑️')

#cycle through all definitions of a word
def get_definitions(i):
  if len(definitions) == 1:
    return definitions[0]
  if active_index == len(definitions)-1:
    if i == 1:
      index = 0
    else:
      index = len(definitions)-2
  elif active_index == 0:
    if i == -1:
      index = len(definitions)-1
    else:
      index = 1
  else:
    index = active_index+i
  return definitions[index]

#use the Oxford Dictionary to get a word definition
def get_oxford_definitions(word_id):
  app_id = "37649a9a"
  app_key = "15e3748a364f3e2bc9bb2337ec223086"
  language = 'en-us'

  fields = 'definitions'
  strictMatch = 'false'

  url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;

  r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})



  json = r.json()
  try:
    definition = json["results"][0]["lexicalEntries"][0]["entries"][0]['senses'][0]['definitions'][0]
  except KeyError:
    return None
  global definitions
  definitions = []

  

  for i in range(len(json["results"])):
    for j in range(len(json["results"][i]["lexicalEntries"])):
      pos = json["results"][i]["lexicalEntries"][j]['lexicalCategory']['id']
      for k in range(len(json["results"][i]["lexicalEntries"][j]['entries'])):
        for l in range(len(json["results"][i]["lexicalEntries"][j]["entries"][k]["senses"])):
          for m in range(len(json["results"][i]["lexicalEntries"][j]["entries"][k]['senses'][l]['definitions'])):
            definitions.append(" *"+pos+"* - "+json["results"][i]["lexicalEntries"][j]["entries"][k]['senses'][l]['definitions'][m]+"\n")
  return definitions

#use the urban dictionary to get urban definitions
def get_urban_definitions(word_id):
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

  querystring = {"term":word_id}

  headers = {
      'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
      'x-rapidapi-key': "888c2a0b14mshddadf1834cda429p19e25ejsnebfca99c0c39"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  data = response.json()

  global definitions
  definitions = []
  try:
    for i in range(len(data['list'])):
      definitions.append(''.join([char for char in data['list'][i]['definition']+"\n" if char != "[" and char != "]"]))
  except KeyError:
    return None

  return definitions


#use the merriam webster api to get synomynms
def get_synonyms(word_id):
  

  url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/"+word_id+"?key=9771ab70-6ed4-4e17-ac35-10e7b9ee60a4"

  r = requests.get(url)

  json = [choice for choice  in r.json() if ' ' not in choice['meta']['id']]

  global definitions
  definitions = []
  

  for i in range(len(json)):
    display = ""
    pos = json[i]['fl']
    display += word_id+"*("+pos+")* - "+ json[i]['shortdef'][0]+"\n"
    syn_list = []
    if json[i]['meta']['syns'] == []:
      continue
    for j in range(len(json[i]['meta']['syns'])):
      for k in range(len(json[i]['meta']['syns'][j])):
        if len(syn_list) == 7:
          definitions.append(display)
          display = word_id+"*("+pos+")* - "+ json[i]['shortdef'][0]+"\n"
          syn_list = []
        
        syn_list.append(json[i]['meta']['syns'][j][k])
        display +="\t"+json[i]['meta']['syns'][j][k]+"\n"
    definitions.append(display)
  return definitions


#use the merriam webster api to get antonyms
def get_antonyms(word_id):
  url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/"+word_id+"?key=9771ab70-6ed4-4e17-ac35-10e7b9ee60a4"

  r = requests.get(url)

  json = [choice for choice  in r.json() if ' ' not in choice['meta']['id']]

  global definitions
  definitions = []
  

  for i in range(len(json)):
    display = ""
    pos = json[i]['fl']
    display += word_id+"*("+pos+")* - "+ json[i]['shortdef'][0]+"\n"
    if json[i]['meta']['ants'] == []:
      continue
    for j in range(len(json[i]['meta']['ants'])):
      for k in range(len(json[i]['meta']['ants'][j])):
        display +="\t"+json[i]['meta']['ants'][j][k]+"\n"
    definitions.append(display)
  
  return definitions
    



#let people cycle through definitions or synonyms
@client.event
async def on_reaction_add(reaction, user):
  global active_index
  if user != client.user:
        if str(reaction.emoji) == "➡️":
            new_def = get_definitions(1)
            await reaction.message.remove_reaction("➡️", user)
            if (active_index + 1) == len(definitions):
              active_index = 0
            else:
              active_index += 1
            await reaction.message.edit(content=new_def)
        if str(reaction.emoji) == "⬅️":
            new_def = get_definitions(-1)
            await reaction.message.remove_reaction("⬅️", user)
            if (active_index - 1) == -1:
              active_index = len(definitions)
            else:
              active_index -= 1
            await reaction.message.edit(content=new_def)
        if str(reaction.emoji) == "🗑️":
          await reaction.message.delete()


