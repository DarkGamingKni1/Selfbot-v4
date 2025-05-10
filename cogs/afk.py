import discord
from discord.ext import commands

afk_reason = None
afk_users = {}

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def afk(self, ctx, *, reason):
        global afk_reason
        afk_reason = reason
        embed = discord.Embed(
            title="AFK Set",
            description=f"<a:sleep:1305994923559878867> AFK set with the reason: `{reason}`.",
            color=discord.Color.blue()
        )
        await self.bot.send_embed(ctx, embed)

    @commands.command()
    async def unafk(self, ctx):
        global afk_reason
        if afk_reason is not None:
            afk_reason = None
            embed = discord.Embed(
                title="AFK Removed",
                description="<a:check:1305994923559878867> You are no longer AFK.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Not AFK",
                description="You are not currently AFK.",
                color=discord.Color.orange()
            )
        await self.bot.send_embed(ctx, embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if not message.author.bot:
            if isinstance(message.channel, discord.DMChannel):
                if afk_reason is not None and message.author != self.bot.user:
                    embed = discord.Embed(
                        description=f"<a:sleep:1305994923559878867> <@{self.bot.user.id}> is AFK\n<:arrow_downright:1305994883202416742> Reason: `{afk_reason}`.",
                        color=discord.Color.blue()
                    )
                    await self.bot.send_embed(message, embed)
            else:
                if self.bot.user in message.mentions:
                    async for msg in message.channel.history(limit=5):
                        if msg.author == self.bot.user and msg.content.startswith(f"> <a:sleep:1305994923559878867> <@{self.bot.user.id}> is AFK"):
                            return 
                    if afk_reason is not None:
                        embed = discord.Embed(
                            description=f"<a:sleep:1305994923559878867> <@{self.bot.user.id}> is AFK\n<:arrow_downright:1305994883202416742> Reason: `{afk_reason}`.",
                            color=discord.Color.blue()
                        )
                        await self.bot.send_embed(message, embed)
                        

async def setup(bot):
    await bot.add_cog(AFK(bot))