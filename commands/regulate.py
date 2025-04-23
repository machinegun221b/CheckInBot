import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class Regulate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def log_regulate(self, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n---\n[Regulate] {now}\n{content}\n"
        with open("regulate.txt", "a") as f:
            f.write(entry)
    
    @commands.command(name="regulate")
    async def regulate(self, ctx):
        def check(m): return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send("🧭 **Daily Regulation Check-In**")

        questions = [
            "🛏️ What time did you go to bed last night?",
            "⏰ What time did you wake up today?",
            "🍽️ Have you eaten regular meals today?",
            "💧 Are you staying hydrated?",
            "🏃 Have you engaged in any physical activity today?",
            "🧘 Have you taken any breaks or practiced relaxation?"
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
        self.log_regulate(log)

        await ctx.send("✅ Your daily regulation check-in has been logged. Keep up the good work!")
    
async def setup(bot):
    await bot.add_cog(Regulate(bot))