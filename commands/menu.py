import discord
from discord.ext import commands
from discord.ui import View, Button

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="menu")
    async def menu(self, ctx):
        embed = discord.Embed(
            title="What would you like to check in with?",
            description="Pick one of the following or type a command anytime!"
        )
        
        embed.add_field(name="🧠 /checkin", value="Morning/Evening/Night energy & mood tracking", inline=False)
        embed.add_field(name="🌇 /eod", value="End of day reflection", inline=False)
        embed.add_field(name="📅 /weeklywrap", value="End of week wrap-up & planning", inline=False)
        embed.add_field(name="🧘 /regulate", value="Lifestyle rhythm check (sleep, food, body)", inline=False)
        embed.add_field(name="🧊 /recover", value="Post-stress or sleeplessness or fog or hangover recovery protocol", inline=False)

        view = View()

        buttons = [
            ("🧠 Check-In", discord.ButtonStyle.primary, "checkin"),
            ("🌇 EOD", discord.ButtonStyle.secondary, "eod"),
            ("📅 Weekly Wrap", discord.ButtonStyle.success, "weeklywrap"),
            ("🧘 Regulate", discord.ButtonStyle.primary, "regulate"),
            ("🧊 Recover", discord.ButtonStyle.danger, "recover"),
        ]

        for label, style, cmd in buttons:
            button = Button(label=label, style=style, custom_id=cmd)
            async def button_callback(interaction, cmd=cmd):
                await interaction.response.send_message(f"Use '/{cmd}' to begin.", ephemeral=True)
            button.callback = button_callback
            view.add_item(button)
        
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Menu(bot))