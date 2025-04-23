import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

# Load bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")

@bot.command()
async def checkin(ctx):
    def check(m): return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("👋 Hey! Let’s check in.\n\n1. **Your energy right now?** (e.g., Foggy, Clear, Wired)")
    energy = await bot.wait_for("message", check=check)

    await ctx.send("2. **Your emotional state?** (e.g., Anxious, Calm, Heavy)")
    emotion = await bot.wait_for("message", check=check)

    await ctx.send("3. **What are your top 1–3 intentions for the day?**")
    intentions = await bot.wait_for("message", check=check)

    # Timestamp + Log to local file
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"\n---\n{now}\nEnergy: {energy.content}\nEmotion: {emotion.content}\nTasks: {intentions.content}\n"

    with open("checkin_log.txt", "a") as f:
        f.write(log_entry)

    await ctx.send("✅ Logged your check-in privately. You’re doing great!")

bot.run(TOKEN)
