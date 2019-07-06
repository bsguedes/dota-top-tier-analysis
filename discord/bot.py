import discord
from discord.utils import find


client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Stats & Data"))


@client.event
async def on_guild_join(guild):
    general = find(lambda x: 'geral' in x.name,  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Oi pessoal, tudo bom? Tenho uma pergunta pra vocês:')
        await general.send('Who is the best Pangolier player in PnK?')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == 'chuvisco':
        await message.channel.send('Of course, the best ancient player!')
    else:
        await message.channel.send('Bela tentativa.')

token = ''
with open('secrets/discord_token') as f:
    for line in f.readlines():
        token = line
client.run(token)
