import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
import asyncio

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

class CheckIn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.morning_checkin.start()
        self.evening_checkin.start()
        self.night_checkin.start()

    # -- Utility for log writing --
    def log_entry(self, section, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n--\n[{section.upper()}] {now}\n{content}\n"
        with open("checkin_log.txt", "a") as f:
            f.write(entry)

    # -- Check-in Command --
    @commands.command(name="checkin")
    async def checkin(self, ctx, time_of_day="morning"):
        def check(m): return m.author == ctx.author and m.channel == ctx.channel
        prompts = {
            "morning": [
                "🌤️ How are you feeling *physically* this morning?",
                "🧠 And mentally?",
                "How about emotionally?",
                "💬 What’s one thing you want vs need today?",
                "🎯 What are 1–3 intentions or tasks you’d like to aim for?"
            ],
            "evening": [
                "🌆 Did you go outside today?",
                "💧 How was your water and food intake?",
                "🧘 One moment that felt good or grounding today?"
            ],
            "night": [
                "🌙 Did you feel up to your tasks today?",
                "📉 Any unmet needs or feelings that came up?",
                "📅 What should tomorrow look like — or how can you do better for yourself?"
            ]
        }

        responses = []
        if time_of_day not in prompts:
            await ctx.send("Please use '/checkin morning', '/checkin evening', or '/checkin night'.")
            return
        
        await ctx.send(f"**{time_of_day.capitalize()} Check-In**")
        for q in prompts[time_of_day]:
            await ctx.send(q)
            try:
                msg = await self.bot.wait_for("message", timeout=120.0, check=check)
                responses.append(f"{q}\n-> {msg.content}")
            except asyncio.TimeoutError:
                responses.append(f"{q}\n-> Skipped (timeout)")

        log = "\n".join(responses)
        self.log_entry(time_of_day, log)
        await ctx.send("✅ Logged your check-in!")
    
    # -- Scheduled Morning Ping --
    @tasks.loop(minutes=1.0)
    async def morning_checkin(self):
        now = datetime.now().strftime("%H:%M")
        if now == "10.00":
            channel = self.bot.get_channel(CHANNEL_ID)
            await channel.send("☀️ Good morning! Time for your `/checkin morning`")
    
    @tasks.loop(minutes=1.0)
    async def evening_checkin(self):
        now = datetime.now().strftime("%H:%M")
        if now == "17:00":
            channel = self.bot.get_channel(CHANNEL_ID)
            await channel.send("🌆 Evening check-in reminder! Try `/checkin evening`")

    @tasks.loop(minutes=1.0)
    async def night_checkin(self):
        now = datetime.now().strftime("%H:%M")
        if now == "22:30":
            channel = self.bot.get_channel(CHANNEL_ID)
            await channel.send("🌙 Wind down time. Reflect with `/checkin night`")
    
    @morning_checkin.before_loop
    @evening_checkin.before_loop
    @night_checkin.before_loop
    async def before_tasks(self):
        await self.bot.wait_until_ready()
    
async def setup(bot):
    await bot.add_cog(CheckIn(bot))