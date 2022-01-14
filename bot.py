import discord # <-- discord.py is imported here
import pytz
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("Token")

bot = discord.Client() #intents=discord.Intents.all(), command_prefix='!'

global prefix
prefix = "!"

@bot.event
async def on_ready():
    print(f'BotId: {bot.user.id} - Name: {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith(prefix + "join"):
        channel = message.author.voice.channel
        voice = discord.utils.get(message.guild.voice_channels, name=channel.name)
        voice_client = discord.utils.get(bot.voice_clients, guild = channel.guild)

        if voice_client == None:
            voice_client = await voice.connect()
        else: 
            await channel.connect()

    if message.content.lower().startswith(prefix + "leave"):
        channel = message.author.voice.channel
        voice = discord.utils.get(message.guild.voice_channels, name=channel.name)
        voice_client = discord.utils.get(bot.voice_clients, guild = channel.guild)
        if voice_client != None:
            await voice_client.disconnect()

@bot.event
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@bot.event
async def poll(ctx, *, message):
    message = await ctx.send(message)
    await message.add_reaction(u"\U0001F44D")
    await message.add_reaction(":tumbsdown: ")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    if payload.channel_id == 689431715038756899:
        if payload.message_id == 931650248558936094:
            if payload.emoji.name == '🦷':
                guild: discord.Guild = bot.get_guild(831633094699253831)

                role: discord.Role = guild.get_role(572490054975488010)
                await payload.member.add_roles(role, reason="Zuweisung")

                channel: discord.TextChannel = guild.get_channel(689431715038756899)
                message = await channel.send('Du hast den Zahn gezogen.')
                await message.add_reaction('🦷')

@bot.event#(name='test')
async def test(ctx, *args):
    await ctx.send(f'Eingabe: {" ".join(args)}')

@bot.event#(name='userinfo')
async def userinfo(ctx, member: discord.Member):
    de = pytz.timezone('Europe/Berlin')
    embed = discord.Embed(title=f'> Userinfo für {member.display_name}',
                          description='', color=0x4cd137, timestamp=pytz.datetime.now().astimezone(tz=de))

    embed.add_field(name='Name', value=f'```{member.name}#{member.discriminator}```', inline=True)
    embed.add_field(name='Bot', value=f'```{("Ja" if member.bot else "Nein")}```', inline=True)
    embed.add_field(name='Nickname', value=f'```{(member.nick if member.nick else "Nicht gesetzt")}```', inline=True)
    embed.add_field(name='Server beigetreten', value=f'```{member.joined_at}```', inline=True)
    embed.add_field(name='Discord beigetreten', value=f'```{member.created_at}```', inline=True)
    embed.add_field(name='Rollen', value=f'```{len(member.roles)}```', inline=True)
    embed.add_field(name='Höchste Rolle', value=f'```{member.top_role.name}```', inline=True)
    embed.add_field(name='Farbe', value=f'```{member.color}```', inline=True)
    embed.add_field(name='Booster', value=f'```{("Ja" if member.premium_since else "Nein")}```', inline=True)
    embed.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

bot.run(token)