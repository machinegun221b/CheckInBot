import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

# load bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# load all command files
async def setup_hook():
	cmd_folder = "./commands"
	for filename in os.listdir(cmd_folder):
		if filename.endswith(".py") and filename != "__init__.py":
			await bot.load_extension(f"commands.{filename[:-3]}")

bot.setup_hook = setup_hook

#@bot.command()
#async def menu(ctx):
#	await ctx.send("**Where would you like to start?\n/checkin\n/eod\n/weeklywrap\n/regulate\n/recover**")

@bot.event
async def on_ready():
	print(f"{bot.user} is online and ready!")

bot.run(TOKEN)
