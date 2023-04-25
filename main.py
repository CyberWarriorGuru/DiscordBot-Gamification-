import os
import discord
import asyncio
import openai
import os
from pathlib import Path
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import json
from datetime import datetime

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

APPLICATION_ID = '1078926941987545109'
PUBLIC_KEY = '44a3878a8aee628567652b56fa6468ba2f2e9d154ac8d70f8bec8ddc8652c521'
TOKEN = 'MTA3ODkyNjk0MTk4NzU0NTEwOQ.GJs2Pt.uxpR2sDfKQHVEPnm9op8eP-A1yRw0sOcbC0Ej0'
openai.api_key = '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'
# new_apikey = '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'
# openai.api_key = new_apikey

def fnGetName(str_text):
  arr_name = []

  nltk_results = ne_chunk(pos_tag(word_tokenize(str_text)))
  for nltk_result in nltk_results:
      if type(nltk_result) == Tree:
          name = ''
          for nltk_result_leaf in nltk_result.leaves():
              name += nltk_result_leaf[0] + ' '
          try:
            x1 = name.find("Hello")
            x2 = name.find("Hi")
            x3 = name.find("hello")
            x4 = name.find("hi")
            x5 = name.find("Okay")
            if x1 == -1 and x2 == -1 and x3 == -1 and x4 == -1 and x5 == -1:
               arr_name.append(name)
          except:
             pass
  return arr_name


intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    user_name = []
    if message.author == client.user:
      return
    # if client.user in message.mentions:
    print(message.content)
    path = Path(f"History\\{message.author}.txt")
    if path.is_file() == False:
      await message.channel.send("Hello! My name is Philostyx\n Welcome to visit our service \n Could you let me know what is your name?")
      with open(f"History\\{message.author}.txt", "a") as fp:
        fp.write(
            f"Bot say {str(datetime.now())}:: Hello! My name is Philostyx. Welcome to visit our service. Could you let me know what is your name?")
        fp.write("\n")
    else:
      with open(f"History\\{message.author}.txt", "r") as fp:
          history_txt = fp.readlines()
          if len(history_txt) == 1:
            user_name = fnGetName(message.content)
            if len(user_name) != 0:
              await message.channel.send(f"Welcome {user_name[0]}! What would you like to understand today?")
              with open(f"History\\{message.author}.txt", "a") as fp:
                fp.write(
                    f"Bot say {str(datetime.now())}:: Welcome {user_name[0]}! If you want change your name please input '/changename newname'")
                fp.write("\n")
              with open("users_list.json") as fp:
                original_json = json.load(fp)
              new_json = {f"{message.author}": user_name[0]}
              original_json.update(new_json)
              with open('users_list.json', 'w') as f:
                json.dump(original_json, f)
            else:
              await message.channel.send(f"Sorry, Please let me know your name first. Thank you.")
            return
          else:
              if message.content[0:11] == "/changename":
                new_name = message.content.split(" ")[1]
                with open("users_list.json") as fp:
                  original_json = json.load(fp)
                original_json[str(message.author)] = new_name
                with open('users_list.json', 'w') as f:
                  json.dump(original_json, f)
                await message.channel.send(f"{new_name}, Success change your name")

              else:
                with open("users_list.json") as fp:
                    original_json = json.load(fp)
                real_username = original_json[f"{message.author}"]
                response = openai.Completion.create(
                    # engine = "davinci:ft-personal-2023-02-25-13-58-37",
                    # engine = "davinci:ft-personal-2023-02-25-04-57-26",
                    # engine = "davinci:ft-discordbot-2023-03-02-18-58-18",
                    # engine = "davinci:ft-discordbot-2023-03-06-14-27-02",
                    engine="davinci:ft-discordbot-2023-03-07-06-52-44",
                    # engine = "text-davinci-003",
                    prompt=f"{message.content}"+"\n\n###\n\n",
                    temperature=0.5,
                    max_tokens=100,
                    stop=["###"]
                )
                # Send the response as a message
                await message.channel.send(real_username + ", " + response.choices[0].text)

                with open(f"History\\{message.author}.txt", "a") as fp:
                  fp.write(f"I say {str(datetime.now())}: {message.content}")
                  fp.write("\n")
                  fp.write(
                      f"bot says {str(datetime.now())}::  {str(response.choices[0].text)}")
                  fp.write("\n")


client.run(TOKEN)
