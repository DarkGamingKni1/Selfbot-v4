import discord, json
from discord.ext import commands

save_file = "database/auto_responses.json"

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_responses = {}
        self.load()

    def load(self):
        try:
            with open(save_file, "r") as file:
                self.auto_responses = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.auto_responses = {}

    def save(self):
        with open(save_file, "w") as file:
            json.dump(self.auto_responses, file, indent=4)

    @commands.command(name="setar")
    async def set_auto_response(self, ctx, trigger_word: str, *, reply_msg: str):
        self.auto_responses[trigger_word.lower()] = reply_msg
        self.save()
        embed = discord.Embed(
            title="Auto-Response Set",
            description=f"Trigger Word: `{trigger_word}`\nResponse: `{reply_msg}`",
            color=discord.Color.green()
        )
        await self.bot.send_embed(ctx, embed)

    @commands.command(name="removear")
    async def remove_auto_response(self, ctx, trigger_word: str):
        if trigger_word.lower() in self.auto_responses:
            del self.auto_responses[trigger_word.lower()]
            self.save()
            embed = discord.Embed(
                title="Auto-Response Removed",
                description=f"Trigger: `{trigger_word}`",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="Not Found",
                description=f"No auto-response found for `{trigger_word}`.",
                color=discord.Color.orange()
            )
        await self.bot.send_embed(ctx, embed)

    @commands.command(name="showar")
    async def show_auto_responses(self, ctx):
        if self.auto_responses:
            lines = "\n".join([f"`{k}` → `{v}`" for k, v in self.auto_responses.items()])
            embed = discord.Embed(title="Auto-Responses", description=lines, color=discord.Color.blue())
        else:
            embed = discord.Embed(title="Auto-Responses", description="No auto-responses set.", color=discord.Color.greyple())
        await self.bot.send_embed(ctx, embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            for trigger, response in self.auto_responses.items():
                if trigger in message.content.lower():
                    if message.author.id == self.bot.user.id or self.bot.user.mentioned_in(message):
                        embed = discord.Embed(description=response, color=discord.Color.blurple())
                        ctx = await self.bot.get_context(message)
                        await self.bot.send_embed(ctx, embed)
                        break

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))