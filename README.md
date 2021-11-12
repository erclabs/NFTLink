# NFTLink
NFTLink - The original NFT ownership verification Discord bot

**(this code only supports ownership verification of NFTs on NiftyGateway)**
## Usage
  1. Install the latest version of Python from https://www.python.org/downloads/ and make sure to add Python to path in the installer
  2. Navigate to the NFTLink folder in your terminal / command prompt
  3. Type 'pip install -r requirements.txt'
  4. Create a Discord bot (https://discordpy.readthedocs.io/en/stable/discord.html)
  5. Give your bot PRESENCE INTENT and SERVER MEMBERS INTENT in the Bot tab of your application
  6. Copy your bot token and paste it in the token variable in bot.py
  7. Set your bot prefix in the prefix variable in bot.py
  8. Retrieve an Etherscan API key (https://info.etherscan.com/api-keys/) and paste it in the etherscanAPIKey variable in cogs\main.py. **Gas price command will not work without this**
  9. Run bot.py
  10. Create an OAuth2 invite URL with 'Administrator' permissions (https://discordpy.readthedocs.io/en/stable/discord.html). This URL will be used to invite the bot into servers.
