import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import os
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())
url = os.getenv('URL')
apikey = os.getenv('API')
user = []
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)
client = commands.Bot(command_prefix = "cuidador! ")

@client.event
async def on_ready():
    print("o cuidador chego")

@client.event
async def on_message(message):
    global user
    await client.process_commands(message)
    if message.author == client.user:
        return
    print(message.author.name,"#",message.author.discriminator,"-",message.content)
    voice = message.guild.voice_client
    if (int(message.author.id) in user and message.author.voice):
        channel = message.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        with open('./speech.mp3','wb') as audio_file:
            res = tts.synthesize(message.content, accept='audio/mp3',voice= 'es-ES_EnriqueVoice' ).get_result()
            audio_file.write(res.content)
        source = FFmpegPCMAudio('speech.mp3')
        voice.play(source)

@client.command()
async def novoid(ctx):
    el_hombre = ctx.author.id
    await ctx.channel.send('Digite o ID da pessoa que quer usar o bot:')
    usuario_id = await client.wait_for('message')
    if el_hombre == usuario_id.author.id:
        user.append(int(usuario_id.content))
        await ctx.channel.send("ID inserido com sucesso!")

@client.command()
async def usuarios(ctx):
    for i in range (len(user)):
        await ctx.channel.send(f"<@{user[i]}>")

client.run(os.getenv('TOKEN'))