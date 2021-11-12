#                     .-._              _,---.   ,--.--------.                 .=-.-.  .-._          ,--.-.,-.  
#                    /==/ \  .-._    .-`.' ,  \ /==/,  -   , -\    _.-.       /==/_ / /==/ \  .-._  /==/- |\  \ 
#                    |==|, \/ /, /  /==/_  _.-' \==\.-.  - ,-./  .-,.'|      |==|, |  |==|, \/ /, / |==|_ `/_ / 
#                    |==|-  \|  |  /==/-  '..-.  `--`\==\- \    |==|, |      |==|  |  |==|-  \|  |  |==| ,   /  
#                    |==| ,  | -|  |==|_ ,    /       \==\_ \   |==|- |      |==|- |  |==| ,  | -|  |==|-  .|   
#                    |==| -   _ |  |==|   .--'        |==|- |   |==|, |      |==| ,|  |==| -   _ |  |==| _ , \  
#                    |==|  /\ , |  |==|-  |           |==|, |   |==|- `-._   |==|- |  |==|  /\ , |  /==/  '\  | 
#                    /==/, | |- |  /==/   \           /==/ -/   /==/ - , ,/  /==/. /  /==/, | |- |  \==\ /\=\.' 
#                    `--`./  `--`  `--`---'           `--`--`   `--`-----'   `--`-`   `--`./  `--`   `--`       


import discord, json, os, os.path, time
from discord.ext import commands, tasks
from colorama import Fore, Back, Style
from discord import Member, Embed
from discord.ext.tasks import loop
from os import path

token = 'TOKEN HERE'
prefix = 'BOT PREFIX HERE'

os.system('mode con: cols=200 lines=40')

top = """             &&@@@@@@@@\033[35m&&&&&&&&&&&&&&&&&\033[39m@@@@@@@@&&         
             &&@@@@@@@&@@\033[35m&&&&&&&&&&&&&\033[39m@@&@@@@@@@&&     
             &&@@@@@@\033[35m&&&&&&\033[39m@@\033[35m&&&&&\033[39m@@\033[35m&&&&&&\033[39m@@@@@@&&     
             &&@@@@@@\033[35m&&&&&&&&&&\033[39m@\033[35m&&&&&&&&&&\033[39m@@@@@@&&     
             &&@@@@@@\033[35m&&&&&&&&&&\033[39m@\033[35m&&&&&&&&&&\033[39m@@@@@@&&     
             &&@@@@@@\033[35m&&&&&&&&&&\033[39m@\033[35m&&&&&&&&&\033[39m@@@@@@@&&""".split("\n")

bottom = """  _   _______ _____ _    _____ _   _ _   __
     | \ | |  ___|_   _| |  |_   _| \ | | | / /
     |  \| | |_    | | | |    | | |  \| | |/ / 
     | . ` |  _|   | | | |    | | | . ` |    \ 
     | |\  | |     | | | |____| |_| |\  | |\  \.
    	     \_| \_\_|     \_/ \_____\___/\_| \_\_| \_/""".split("\n")

print('\033[39m' + """                            &&&@&&&
                        &&&&@@@@@@@@@&&&&     
                    &&&@@@@@@@@@@@@@@@@@@@&&&     
                &&&@@@@@@@@@@@@@@@@@@@@@@@@@@@&&     
             &&@@@@@@@@@@@@\033[35m&&&&&&&&\033[39m@@@@@@@@@@@@@&&""")

for row in zip(top, bottom):
    print(row[0] + " " + row[1])

print("""             &&@@@@@@@@@@\033[35m&&&&&&\033[39m@\033[35m&&&&&\033[39m@@@@@@@@@@@&&     
              &&&@@@@@@@@@@@\033[35m&&&\033[39m@\033[35m&&&&\033[39m@@@@@@@@@&&&&     
		  &&&&@@@@@@@@@@@@@@@@@@@&&&&     
		      &&&&@@@@@@@@@@@&&&          
			    &&&@&&&""")


intents = discord.Intents(
	messages = True,
	reactions = True,
	members = True,
	guilds = True
)

bot = commands.Bot(command_prefix = prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('$verify'))
	print('Bot is online!')
	print(f'Serving {len(bot.guilds)} Servers')

@bot.event
async def on_guild_join(guild):
	embed = discord.Embed(colour = discord.Colour.purple())
	embed.set_author(name='Thank you for inviting NFTLink!')
	embed.add_field(name='Get Started', value='Type $help to get started!', inline = False)
	embed.set_footer(text=f"Made by Oh#9999 - uhh.eth")
	for channel in guild.channels:
		if channel.name == 'nftlink-config':
			await channel.send(embed=embed)
			return
	overwrites = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False)
	}
	channel = await guild.create_text_channel('nftlink-config',  overwrites=overwrites)
	await channel.send(embed=embed)

@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(extension + " loaded")

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	await ctx.send(extension + " unloaded")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def help(ctx, category=None):
	if category==None:
		channel = ctx.message.channel
		embed = discord.Embed(title = 'Help 🆘', colour = discord.Colour.purple())
		embed.add_field(name='Verification', value = '🔗$verify {NG Username} - Link your NiftyGateway profile to receive roles!', inline = False)
		embed.add_field(name='Crypto', value = '⛽$gas - Shows current ETH gas prices in GWEI\n💰$c {Crypto Ticker} - Shows price of any cryptocurrency!', inline = False)
		embed.add_field(name='Setup', value = "⚙$role - Guides you through creating a new role configuration\n⚙$reset - Resets the server's configuration", inline = False)
		await channel.send(embed=embed)

bot.run(token, bot=True)
