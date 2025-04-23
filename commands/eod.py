import discord
from discord.ext import commands
from datetime import datetime
import os
import asyncio

class EndOfDay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_eod(self, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n---\n[EOD] {now}\n{content}\n"
        with open("eod_log.txt", "a") as f:
            f.write(entry)

    @commands.command(name="eod")
    async def eod(self, ctx):
        def check(m): return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send("🌇 **End of Day Check-In**")

        questions = [
            "✅ What worked well today?",
            "🌀 What didn’t work or felt off?",
            "🔁 How can you do better tomorrow?",
            "📝 Any to-dos or notes for tomorrow?"
        ]
        answers = []

        for q in questions:
            await ctx.send(q)
            try:
                msg = await self.bot.wait_for("message", timeout=120.0, check=check)
                answers.append(f"{q}\n-> {msg.content}")
            except asyncio.TimeoutError:
                answers.append(f"{q}\n -> Skipped")
        
        log = "\n".join(answers)
        self.log_eod(log)

        # closing suggestions
        await ctx.send("🧘 Great. Let’s close the day gently.")
        await ctx.send(
            "🛁 Try one of these: change lighting, play soft music, shower, wash face or feet.\n\n"
            "📺 Optional: watch a wind-down show, listen to a slow playlist, light a candle. Do skincare/soak feet if needed.\n\n"
            "🛏️ Get ready to sleep without screens for the last few mins. You did good today. 😴"
        )

        await ctx.send("✅ Logged your day. See you tomorrow! ✨")

async def setup(bot):
    await bot.add_cog(EndOfDay(bot))