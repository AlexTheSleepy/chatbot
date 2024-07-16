# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 23:39:05 2023

@author: Aleja
"""
from mailbox import Message
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import warnings
warnings.filterwarnings("ignore")

import discord
import json
import requests
from discord.ext import commands as cds
from os.path import exists
from bs4 import BeautifulSoup
import logging
import aiohttp
import base64


logging.basicConfig(level=logging.ERROR)

global host 
host = '127.0.0.1:5000'

URI = f"http://{host}/v1/chat/completions"
global history 
global rules


if exists("history.json"):
    with open('history.json', 'r') as openfile:
        history = json.load(openfile)
else:
    history = {'history': []}
    f = open("history.json", "w")
    json_object = json.dumps(history, indent=4)
    f.write(json_object)

if exists("rules.json"):
    with open('rules.json', 'r') as openfile:
        rules = json.load(openfile)
else:
    rules = {}
    rules["change_twitter"] = False
    f = open("rules.json", "w")
    json_object = json.dumps(rules, indent=4)
    f.write(json_object)



async def run_chat_async(user_input, username):

    headers = {
        "Content-Type": "application/json"
    }

    history["history"].append({"role": "user", "content": user_input})

    request = {
        "mode": "chat",
        "character": "Mel",
        "messages": history["history"]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URI, json = request, headers = headers) as response:
            if response.status == 200:
                result_json = await response.json()
                result = result_json['choices'][0]['message']
                history["history"].append(result)
                f = open("response.json", "w")
                json_object = json.dumps(result_json, indent=4)
                f.write(json_object)
                return result
    
BOT_TOKEN = input('Insert bot token:\n')

bot = cds.Bot(command_prefix="!", intents=discord.Intents.all())

game = discord.Game("with statistics.")


@bot.listen() 
async def on_message(message):
    if message.author == bot.user or (not rules["change_twitter"]):
        return 
    message_ = message.content.split()

    message_send = ""

    embedders = ['https://twitter.com/', 'https://x.com/','https://pixiv.net/', 'https://www.pixiv.net/']
    embeds = {
        'https://twitter.com/': 'https://vxtwitter.com/',
        'https://x.com/': 'https://vxtwitter.com/',
        'https://pixiv.net/': 'https://phixiv.net/',
        'https://www.pixiv.net/': 'https://phixiv.net/'
    }

    send = False

    for message_link in message_:
        for embedder in embedders:
            if embedder in message_link:
                clean_link = message_link.split('?')[0]
                if not (message_link[0] == '<' and message_link[-1] == '>'):
                    if '||' in clean_link:
                        message_send +='||' + ('<' + clean_link +'>[.]('+ clean_link.replace(embedder, embeds[embedder]) + ")\n").replace('||', '') + '||'
                    else:
                        message_send += '<' + clean_link +'>[.]('+ clean_link.replace(embedder, embeds[embedder]) + ")\n"
                    send = True

    if not send:
        return
    
    print(message_send)

    await message.edit(suppress=True)
    await message.channel.send(content = message_send)
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.command()
async def check(ctx):
    print(ctx.author.global_name)

@bot.command()
async def image(ctx, *arr):
    url = "http://127.0.0.1:7860"

    user_input = ""
    for x in arr:
        user_input += str(x) + " "

    prompt = user_input
    neg_prompt = 'FastNegativeV2, (low quality:1.3), (worst quality:1.3),(monochrome:0.8),(deformed:1.3),(malformed hands:1.4),(poorly drawn hands:1.4),(mutated fingers:1.4),(bad anatomy:1.3),(extra limbs:1.35),(poorly drawn face:1.4),(watermark:1.3)'
    
    request = {
        'prompt': prompt,
        'negative_prompt': neg_prompt,
        'steps': 40,
        'sampler_name': 'DPM++ 2M SDE',
        'sd_model_checkpoint': 'meinapastel_v6Pastel',
        'enable_hr': True,
        'hr_second_pass_steps': 20,
        'denoising_strength': 0.6
        
    }
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}/sdapi/v1/txt2img', json = request) as response:
                print(response.status)
                if response.status == 200:
                    r = await response.json()                

        with open("output_default.png", 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

        await ctx.send(file = discord.File('output_default.png'))

@bot.command()
async def image_landscape(ctx, *arr):
    url = "http://127.0.0.1:7860"

    user_input = ""
    for x in arr:
        user_input += str(x) + " "

    prompt = user_input
    neg_prompt = 'FastNegativeV2, (low quality:1.3), (worst quality:1.3),(monochrome:0.8),(deformed:1.3),(malformed hands:1.4),(poorly drawn hands:1.4),(mutated fingers:1.4),(bad anatomy:1.3),(extra limbs:1.35),(poorly drawn face:1.4),(watermark:1.3)'
    
    request = {
        'prompt': prompt,
        'negative_prompt': neg_prompt,
        'steps': 40,
        'width': 800,
        'sampler_name': 'DPM++ 2M SDE',
        'sd_model_checkpoint': 'meinapastel_v6Pastel',
        'enable_hr': True,
        'hr_second_pass_steps': 20,
        'denoising_strength': 0.6
        
    }
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}/sdapi/v1/txt2img', json = request) as response:
                print(response.status)
                if response.status == 200:
                    r = await response.json()                

        with open("output_landscape.png", 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

        await ctx.send(file = discord.File('output_landscape.png'))

@bot.command()
async def image_portrait(ctx, *arr):
    url = "http://127.0.0.1:7860"

    user_input = ""
    for x in arr:
        user_input += str(x) + " "

    prompt = user_input
    neg_prompt = 'FastNegativeV2, (low quality:1.3), (worst quality:1.3),(monochrome:0.8),(deformed:1.3),(malformed hands:1.4),(poorly drawn hands:1.4),(mutated fingers:1.4),(bad anatomy:1.3),(extra limbs:1.35),(poorly drawn face:1.4),(watermark:1.3)'
    
    request = {
        'prompt': prompt,
        'negative_prompt': neg_prompt,
        'steps': 40,
        'height': 800, 
        'sampler_name': 'DPM++ 2M SDE',
        'sd_model_checkpoint': 'meinapastel_v6Pastel',
        'enable_hr': True,
        'hr_second_pass_steps': 20,
        'denoising_strength': 0.6
        
    }
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}/sdapi/v1/txt2img', json = request) as response:
                print(response.status)
                if response.status == 200:
                    r = await response.json()                

        with open("output_portrait.png", 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

        await ctx.send(file = discord.File('output_portrait.png'))

@bot.command()
async def enable_embedding(ctx, *arr):
    rules["change_twitter"] = True
    await ctx.send("Site embedding enabled.")
    
    f = open("rules.json", "w")
    json_object = json.dumps(rules, indent=4)
    f.write(json_object)

@bot.command()
async def disable_embedding(ctx, *arr):
    rules["change_twitter"] = False
    await ctx.send("Site embedding disabled.")
    
    f = open("rules.json", "w")
    json_object = json.dumps(rules, indent=4)
    f.write(json_object)

@bot.command()
async def eh(ctx, *arr):
    history["history"] = []
    await ctx.send("History erased!")

@bot.command()
async def talk(ctx, *arr):
    user = str(ctx.author.global_name)
    user_input = ""
    for x in arr:
        user_input += str(x) + " "
    print(f"{user}: {user_input}")

    async with ctx.typing():
        result = await run_chat_async(user_input, user)

    response = result['content']
    

    f = open("history.json", "w")
    json_object = json.dumps(history, indent=4)
    f.write(json_object)

    response = BeautifulSoup(response, "html.parser").prettify()
    print("Mel: " + response)
    
    await ctx.send(response)
    
bot.run(BOT_TOKEN)
logging.basicConfig(level=logging.ERROR)
