import asyncio, aiohttp, string, json, random, discord, requests, os.path, ssl
from types import MethodDescriptorType
from discord.ext import commands, tasks
from discord import Member, Embed
from aiohttp import request, ClientSession
from itertools import cycle
from os import path
from urllib.request import urlopen

ssl._create_default_https_context = ssl._create_unverified_context

etherscanAPIKey = 'ETHERSCAN API KEY HERE'

class MainClass(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Main is online')

    @commands.command(pass_context=True)    
    async def reset(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            os.remove(f'servers\server_{str(ctx.message.guild.id)}.json')
 
    @commands.command(name='role')
    async def role(self, ctx):
        if ctx.message.author.guild_permissions.manage_roles:
            configMessage = discord.Embed(title = 'Role Type', color = discord.Colour.purple())
            configMessage.add_field(name = '🔽 Any Nifty', value = 'Creating a role configuration for any Nifty will apply the role to anyone who owns a specific amount of Nifties.', inline=False)
            configMessage.add_field(name = '💚 Specific Nifty', value = 'Creating a role configuration for a specific Nifty will apply the role to anyone who owns a specific amount of a specific Nifty.', inline=False)
            configMessage.add_field(name = '🟠 Specific collection', value = 'Creating a role configuration for a specific Nifty will apply the role to anyone who owns a specific amount of Nifties from a specific collection.', inline=False)
            configMessage.add_field(name = '🔺 Any Nifty by specific artist', value = 'Creating a role configuration for a specific Nifty will apply the role to anyone who owns a specific amount of Nifties by a specific artist.', inline=False)
            configMessage.add_field(name = '🟪 Limited Nifties by specific artist', value = 'Creating a role configuration for a specific Nifty will apply the role to anyone who owns a specific amount of drawing/auction/silent auction Nifties by a specific artist.', inline=False)
            awaitingMessage = await ctx.send(embed=configMessage)
            await awaitingMessage.add_reaction('🔽')
            await asyncio.sleep(0.5)
            await awaitingMessage.add_reaction('💚')
            await asyncio.sleep(0.5)
            await awaitingMessage.add_reaction('🟠')
            await asyncio.sleep(0.5)
            await awaitingMessage.add_reaction('🔺')
            await asyncio.sleep(0.5)
            await awaitingMessage.add_reaction('🟪')
            await asyncio.sleep(0.5)
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check = lambda reaction, user: reaction.emoji in ["🔽", "💚", "🟠", "🔺", "🟪"],
                    timeout = 120
                )
                await awaitingMessage.delete()
                if user.id == ctx.message.author.id:
                    if reaction.emoji == "🔽":
                        roleMethod = 'notSpecific'
                        configMessage2 = discord.Embed(color = discord.Colour.purple())
                        configMessage2.add_field(name = 'Next Steps', value = 'Please respond with the number requirement of Nifties to acquire this role and the @Role seperated by a comma and space.\n(example: 1, @Collector)', inline=False)
                        awaitingMessage2 = await ctx.send(embed=configMessage2)
                        try:
                            msg = await self.bot.wait_for(
                                "message",
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                            if msg:
                                messageData = msg.content.split(', ')
                                numreq = messageData[0]
                                roleID = messageData[1]
                                roleID = roleID[3:-1]

                        except asyncio.TimeoutError:
                            await ctx.send('**Timed out. Please try running the command again.**')
                            return
                    elif reaction.emoji == '💚':
                        roleMethod = 'specificNifty'
                        configMessage2 = discord.Embed(color = discord.Colour.purple())
                        configMessage2.add_field(name = 'Next Steps', value = "Please respond with the artist's exact Nifty name (without the #xx/xx), the number requirement of Nifties to acquire this role, and the @Role seperated by a comma and space.\n(example: nessgraphics, *Bull Run, 5, @Collector*)", inline=False)
                        awaitingMessage2 = await ctx.send(embed=configMessage2)
                        try:
                            msg = await self.bot.wait_for(
                                "message",
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                            if msg:
                                messageData = msg.content.split(', ')
                                artistProfile = messageData[0]
                                niftyName = messageData[1]
                                numreq = messageData[2]
                                roleID = messageData[3]
                                roleID = roleID[3:-1]

                        except asyncio.TimeoutError:
                            await ctx.send('**Timed out. Please try running the command again.**')
                            return
                    elif reaction.emoji == '🟠':
                        roleMethod = 'specificCollection'
                        configMessage2 = discord.Embed(color = discord.Colour.purple())
                        configMessage2.add_field(name = 'Next Steps', value = 'Please respond with the collection contract address, the number requirement of Nifties to acquire this role, and the @Role seperated by a comma and space.\n(example: *0x000000, 5, @Collector*)', inline=False)
                        awaitingMessage2 = await ctx.send(embed=configMessage2)
                        try:
                            msg = await self.bot.wait_for(
                                "message",
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                            if msg:
                                messageData = msg.content.split(', ')
                                contractAddress = messageData[0]
                                numreq = messageData[1]
                                roleID = messageData[2]
                                roleID = roleID[3:-1]

                        except asyncio.TimeoutError:
                            await ctx.send('**Timed out. Please try running the command again.**')
                            return
                    elif reaction.emoji == '🔺':
                        roleMethod = 'byArtist'
                        configMessage2 = discord.Embed(color = discord.Colour.purple())
                        configMessage2.add_field(name = 'Next Steps', value = "Please respond with the artist's exact NiftyGateway username, the number requirement of Nifties to acquire this role, and the @Role seperated by a comma and space.\n(example: *toomuchlag, 5, @Collector*)", inline=False)
                        awaitingMessage2 = await ctx.send(embed=configMessage2)
                        try:
                            msg = await self.bot.wait_for(
                                "message",
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                            if msg:
                                messageData = msg.content.split(', ')
                                artistProfile = messageData[0]
                                numreq = messageData[1]
                                roleID = messageData[2]
                                roleID = roleID[3:-1]

                        except asyncio.TimeoutError:
                            await ctx.send('**Timed out. Please try running the command again.**')
                            return
                    elif reaction.emoji == '🟪':
                        roleMethod = 'limitedNiftiesByArtist'
                        configMessage2 = discord.Embed(color = discord.Colour.purple())
                        configMessage2.add_field(name = 'Next Steps', value = "Please respond with the artist's exact NiftyGateway username, the number requirement of Nifties to acquire this role, and the @Role seperated by a comma and space.\n(example: *lushsux, 5, @Collector*)", inline=False)
                        awaitingMessage2 = await ctx.send(embed=configMessage2)
                        try:
                            msg = await self.bot.wait_for(
                                "message",
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                            if msg:
                                messageData = msg.content.split(', ')
                                artistProfile = messageData[0]
                                numreq = messageData[1]
                                roleID = messageData[2]
                                roleID = roleID[3:-1]

                        except asyncio.TimeoutError:
                            await ctx.send('**Timed out. Please try running the command again.**')
                            return
            except asyncio.TimeoutError:
                await ctx.send('**Timed out. Please try running the command again.**')
                return
            roleAdded = discord.Embed(title='Role Added✅', color = discord.Colour.green())
            authorName = ctx.message.author.name + '#' + ctx.message.author.discriminator
            serverID = str(ctx.message.guild.id)
            file = f'servers/server_{serverID}.json'
            if path.exists(file):
                if roleMethod == 'notSpecific':
                    jsonData = {
                        "method": roleMethod,
                        "roleID": int(roleID),
                        "numreq": int(numreq)
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                elif roleMethod == 'byArtist':
                    jsonData = {
                        "method": roleMethod,
                        "roleID": int(roleID),
                        "artistProfile": artistProfile,
                        "numreq": int(numreq)
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty by specific artist', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Artist', value=artistProfile, inline=False)
                elif roleMethod == 'specificNifty':
                    jsonData = {
                        "method": roleMethod,
                        "artistProfile": artistProfile,
                        "roleID": int(roleID),
                        "niftyName": niftyName,
                        "numreq": int(numreq)
                    }
                    roleAdded.add_field(name='Role Type', value='Specific Nifty', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Nifty Name', value=niftyName, inline=False)
                elif roleMethod == 'specificCollection':
                    jsonData = {
                        "method": roleMethod,
                        "roleID": int(roleID),
                        "contractAddress": contractAddress,
                        "numreq": int(numreq)
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty from specific collection', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Contract Address', value=contractAddress, inline=False)
                elif roleMethod == 'limitedNiftiesByArtist':
                    jsonData = {
                        "method": roleMethod,
                        "roleID": int(roleID),
                        "artistProfile": artistProfile,
                        "numreq": int(numreq)
                    }
                    roleAdded.add_field(name='Role Type', value='Limited Nifties by specific artist', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Artist', value=artistProfile, inline=False)
                await ctx.send(embed=roleAdded)

                with open (file, 'r') as outfile:
                    file_data = json.load(outfile)
                    file_data['roles'].append(jsonData)

                with open (file, 'w') as outfile:
                    json.dump(file_data, outfile, indent = 4, ensure_ascii = False)

            else:
                roleAdded = discord.Embed(title='Role Added✅', color = discord.Colour.green())
                if roleMethod == 'notSpecific':
                    jsonData = {
                        "administrator": authorName,
                        "serverID": serverID,
                        "roles": [
                            {
                                "method": roleMethod,
                                "roleID": int(roleID),
                                "numreq": int(numreq)
                            }
                        ]
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                elif roleMethod == 'byArtist':
                    jsonData = {
                        "administrator": authorName,
                        "serverID": serverID,
                        "roles": [
                            {
                                "method": roleMethod,
                                "roleID": int(roleID),
                                "artistProfile": artistProfile,
                                "numreq": int(numreq)
                            }
                        ]
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty by specific artist', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Artist', value=artistProfile, inline=False)
                elif roleMethod == 'specificNifty':
                    jsonData = {
                        "administrator": authorName,
                        "serverID": serverID,
                        "roles": [
                            {
                                "method": roleMethod,
                                "artistProfile": artistProfile,
                                "roleID": int(roleID),
                                "niftyName": niftyName,
                                "numreq": int(numreq)
                            }
                        ]
                    }
                    roleAdded.add_field(name='Role Type', value='Specific Nifty', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Nifty Name', value=niftyName, inline=False)
                elif roleMethod == 'specificCollection':
                    jsonData = {
                        "administrator": authorName,
                        "serverID": serverID,
                        "roles": [
                            {
                                "method": roleMethod,
                                "roleID": int(roleID),
                                "contractAddress": contractAddress,
                                "numreq": int(numreq)
                            }
                        ]
                    }
                    roleAdded.add_field(name='Role Type', value='Any Nifty from specific collection', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Contract Address', value=contractAddress, inline=False)
                elif roleMethod == 'limitedNiftiesByArtist':
                    jsonData = {
                        "administrator": authorName,
                        "serverID": serverID,
                        "roles": [
                            {
                                "method": roleMethod,
                                "roleID": int(roleID),
                                "artistProfile": artistProfile,
                                "numreq": int(numreq)
                            }
                        ]
                    }
                    roleAdded.add_field(name='Role Type', value='Limited Nifties by specific artist', inline=False)
                    roleAdded.add_field(name='Role ID', value=roleID, inline=False)
                    roleAdded.add_field(name='Minimum number of Nifties fitting the criteria required', value=numreq, inline=False)
                    roleAdded.add_field(name='Artist', value=artistProfile, inline=False)
                await ctx.send(embed=roleAdded)
                with open(file, 'w') as outfile:
                    json.dump(jsonData, outfile, indent = 4, ensure_ascii = False)

    @commands.command(name='verify')
    async def verify(self, ctx, name):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            await asyncio.sleep(1)
            await ctx.message.delete()
            await ctx.send(f'Sent you a DM! <@{ctx.message.author.id}>')
            errorMessage = discord.Embed(title = 'Error! 🚨', color = discord.Colour.red(), timestamp=ctx.message.created_at)
            dm_channel = await ctx.author.create_dm()
            nameLower = name.lower()
            res = await session.get(f'https://api.niftygateway.com//user/profile-and-offchain-nifties-by-url/?profile_url={nameLower}')
            resOBJ = await res.json()
            if resOBJ['didSucceed'] == True:
                def id_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
                    return ''.join(random.choice(chars) for n in range(8))
                code = 'NFTLink' + id_generator(0)
                verifyMessage = discord.Embed(title = 'Verification Instructions', color = discord.Colour.purple(), timestamp=ctx.message.created_at)
                verifyMessage.add_field(name = 'Next Steps', value = 'Add the unique string below to your Nifty Gateway bio within 5 minutes to link your NiftyGateway account.', inline=False)
                verifyMessage.add_field(name = 'Unique String', value=code, inline=False)
                await dm_channel.send(embed=verifyMessage)
                timeleft = 60
                for i in range(60):
                    res = await session.get('https://api.niftygateway.com//user/profile-and-offchain-nifties-by-url/?profile_url=' + nameLower + '&page={"current":1,"size":1000}')
                    resOBJ = await res.json()
                    if code in resOBJ['userProfileAndNifties']['bio']:
                        verifiedMessage = discord.Embed(title = 'Verified! ✅', color = discord.Colour.green(), timestamp=ctx.message.created_at)
                        verifiedMessage.add_field(name = 'Applying Roles', value='Please allow up to 2 minutes to get your roles.', inline=False)
                        await dm_channel.send(embed=verifiedMessage)
                        file = "servers\server_" + str(ctx.message.guild.id) + ".json"
                        openfile = open(file, "r", encoding = "utf-8")
                        data = json.load(openfile)
                        for serverRole in data['roles']:
                            role = discord.utils.get(ctx.author.guild.roles, id=serverRole['roleID'])
                            if serverRole['method'] == 'notSpecific':
                                numNifties = 0
                                for nifty in resOBJ['userProfileAndNifties']['nifties']:
                                    numNifties += 1
                                if numNifties >= serverRole['numreq']:
                                    await ctx.author.add_roles(role)
                            if serverRole['method'] == 'byArtist':
                                numNifties = 0
                                for nifty in resOBJ['userProfileAndNifties']['nifties']:
                                    if nifty['creator_info']['profile_url'].lower() == serverRole['artistProfile'].lower():
                                        numNifties += 1
                                if numNifties >= serverRole['numreq']:
                                    await ctx.author.add_roles(role)
                            if serverRole['method'] == 'specificNifty':
                                numNifties = 0
                                for nifty in resOBJ['userProfileAndNifties']['nifties']:
                                    if '#' in nifty['name']:
                                        newName = nifty['name'].split(' #')
                                        if newName[0].lower() == serverRole['niftyName'].lower() and nifty['creator_info']['profile_url'].lower() == serverRole['artistProfile'].lower():
                                            numNifties += 1
                                    else:
                                        if nifty['name'].lower() == serverRole['niftyName'].lower() and nifty['creator_info']['profile_url'].lower() == serverRole['artistProfile'].lower():
                                            numNifties += 1
                                    if numNifties >= serverRole['numreq']:
                                        await ctx.author.add_roles(role)
                            if serverRole['method'] == 'specificCollection':
                                numNifties = 0
                                for nifty in resOBJ['userProfileAndNifties']['nifties']:
                                    if nifty['contractAddress'] == role['contractAddress']:
                                        numNifties += 1
                                    if numNifties >= serverRole['numreq']:
                                        await ctx.author.add_roles(role)
                            if serverRole['method'] == 'limitedNiftiesByArtist':
                                numNifties = 0
                                for nifty in resOBJ['userProfileAndNifties']['nifties']:
                                    if nifty['creator_info']['profile_url'].lower() == serverRole['artistProfile'].lower():
                                        if nifty['unmintedNiftyObjThatCreatedThis']['contractObj']['isAnAuctionNifty'] == True or nifty['unmintedNiftyObjThatCreatedThis']['contractObj']['isDrawing'] == True or nifty['unmintedNiftyObjThatCreatedThis']['contractObj']['isSilentAuction'] == True:
                                            numNifties += 1
                                        if numNifties >= serverRole['numreq']:
                                            await ctx.author.add_roles(role)
                        break
                                    
                    else:
                        await asyncio.sleep(5)
                        timeleft -= 1
                if timeleft == 0:
                    errorMessage.add_field(name = 'Error Message', value='Failed to verify in time. Please retry verification.')
                    errorMessage.set_thumbnail(url = ctx.author.avatar.url)
                    await dm_channel.send(embed=errorMessage)
            else:
                errorMessage.set_thumbnail(url = ctx.author.avatar.url)
                errorMessage.add_field(name = 'Error Message', value = 'Invalid Username❌', inline=False)
                errorMessage.add_field(name = 'Command Syntax', value= '$verify {NiftyGateway Username}', inline=False)
                await dm_channel.send(embed=errorMessage)

    @commands.command(name='gas', description = 'Gives the accurate average, fast & fastest gas prices')
    async def gas(self, ctx):
        url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={etherscanAPIKey}"
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.json()
                low = str(r['result']['SafeGasPrice'])
                fast = str(r['result']['FastGasPrice'])
                average = str(r['result']['ProposeGasPrice'])
                embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at, title= "ETH Gas Price")
                embed.add_field(name="Low", value=f"{low} GWEI")
                embed.add_field(name="Average", value=f"{average} GWEI")
                embed.add_field(name="Fast", value=f"{fast} GWEI")
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @commands.command(name='crypto', aliases=['c'], description= 'Gives the accurate price and 24h % change of a cryptocurrency real time.')
    async def crypto(self, ctx, ticker):
        url = f'https://data.messari.io/api/v1/assets/{ticker}/metrics'
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.json()
                ticker = ticker.upper()
                embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                            title=f"{ticker}")
                data = str([r][0]['data']['market_data']['price_usd'])
                data2 = str([r][0]['data']['market_data']['percent_change_usd_last_24_hours'])
                size = len(data)
                size2 = len(data2)
                moddata = data[:size - 11]
                moddata2 = data2[:size2 - 11]
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Price (USD)", value=f"**${moddata} per {ticker}**", inline=False)
                embed.add_field(name="24h % Change", value=f"**{moddata2}%**", inline=False)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MainClass(bot))
