import discord
from discord.ext import commands
import asyncio
import json
import os

class AutoSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_tasks = {}
        self.file_path = 'database/autosenders.json'
        self.load_autosenders()

    def load_autosenders(self):
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, 'r') as f:
            data = json.load(f)

        for channel_id_str, info in data.items():
            channel_id = int(channel_id_str)
            cooldown = info["cooldown"]
            message = info["message"]

            channel = self.bot.get_channel(channel_id)
            if channel:
                task = self.bot.loop.create_task(self.autosend_loop(channel, cooldown, message))
                self.auto_tasks[channel_id] = {"task": task, "cooldown": cooldown, "message": message}

    def save_autosenders(self):
        data = {
            str(channel_id): {
                "cooldown": info["cooldown"],
                "message": info["message"]
            } for channel_id, info in self.auto_tasks.items()
        }

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    async def autosend_loop(self, channel, cooldown, message):
        try:
            while True:
                await channel.send(message)
                await asyncio.sleep(cooldown)
        except asyncio.CancelledError:
            pass

    @commands.command()
    async def startautosender(self, ctx, channel_id: int, cooldown: int, *, message: str):
        channel = self.bot.get_channel(channel_id)
        embed = discord.Embed(color=discord.Color.green())

        if not channel:
            embed.title = "Error"
            embed.description = "Invalid channel ID."
            await self.bot.send_embed(ctx, embed)
            return

        if channel_id in self.auto_tasks:
            embed.title = "Error"
            embed.description = "Auto sender is already running for that channel."
            await self.bot.send_embed(ctx, embed)
            return

        task = self.bot.loop.create_task(self.autosend_loop(channel, cooldown, message))
        self.auto_tasks[channel_id] = {"task": task, "cooldown": cooldown, "message": message}
        self.save_autosenders()

        embed.title = "Auto Sender Started"
        embed.description = f"Auto sender started in <#{channel_id}> every {cooldown} seconds."
        await self.bot.send_embed(ctx, embed)

    @commands.command()
    async def stopautosender(self, ctx, channel_id: int):
        embed = discord.Embed(color=discord.Color.red())
        task_info = self.auto_tasks.pop(channel_id, None)

        if task_info:
            task_info["task"].cancel()
            self.save_autosenders()
            embed.title = "Auto Sender Stopped"
            embed.description = f"Auto sender stopped for <#{channel_id}>."
        else:
            embed.title = "Error"
            embed.description = "No auto sender is running for that channel."

        await self.bot.send_embed(ctx, embed)

    def cog_unload(self):
        for info in self.auto_tasks.values():
            info["task"].cancel()
        self.save_autosenders()

async def setup(bot):
    await bot.add_cog(AutoSender(bot))