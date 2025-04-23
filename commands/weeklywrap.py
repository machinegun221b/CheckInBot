import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class WeeklyWrap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def log_weekly(self, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n---\n[Weekly Wrap] {now}\n{content}\n"
        with open("weekly_log.txt", "a") as f:
            f.write(entry)
    
    @commands.command(name="weeklywrap")
    async def weeklywrap(self, ctx):
        def check(m): return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send("📅 **Weekly Reflection**")

        questions = [
            "🌟 What were your highlights this week?",
            "⚠️ What challenges did you face?",
            "🔁 What would you like to improve next week?",
            "📝 Any notes or plans for the upcoming week?"
        ]
        answers = []

        for q in questions:
            await ctx.send(q)
            try:
                msg = await self.bot.wait_for("message", timeout=180.0, check=check)
                answers.append(f"{q}\n-> {msg.content}")
            except asyncio.TimeoutError:
                answers.append(f"{q}\n-> Skipped")
        
        log = "\n".join(answers)
        self.log_weekly(log)

        await ctx.send("✅ Your weekly reflection has been logged. Great job!")

async def setup(bot):
    await bot.add_cog(WeeklyWrap(bot))