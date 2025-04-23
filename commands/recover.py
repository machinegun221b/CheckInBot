import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class Recover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def log_recover(self, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n---\n[Recover] {now}\n{content}\n"
        with open("recover.txt", "a") as f:
            f.write(entry)
    
    @commands.command(name="recover")
    async def recover(self, ctx):
        suggestions = [
            "💤 Ensure you're getting sufficient sleep.",
            "🥗 Eat balanced meals at regular intervals.",
            "🚶 Engage in light physical activity, like a short walk.",
            "🧘 Practice relaxation techniques, such as deep breathing or meditation.",
            "📵 Take breaks from screens to rest your eyes and mind.",
            "💧 Stay hydrated throughout the day.",
            "📓 Reflect on your day and jot down any thoughts or feelings."
        ]

        await ctx.send("🧊 **Recovery Suggestions**")
        for suggestion in suggestions:
            await ctx.send(suggestion)

        self.log_recovery("Provided recovery suggestions to user.")
        await ctx.send("✅ Recovery suggestions have been provided. Take care!")

async def setup(bot):
    await bot.add_cog(Recover(bot))