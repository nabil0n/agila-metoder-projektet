from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get('DISC_TOKEN')
# TOKEN = 'MTI3NTgwNTE5NjEwNjA3NjE5Mw.GyNwsO.rfiZCJQ0hZggyQZg0ycriikd23DL7DEadisKsk'
CHANNEL_ID = 1275809359045070970 #HEJJEJEJEJ
MAX_SESSION_TIME_MINUTES = 2

@dataclass
class Session:
    is_active: bool = False
    start_time = int = 0

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

session = Session()

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")# hej hej
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You have been studying for {MAX_SESSION_TIME_MINUTES} minutes.")


@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"Study session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Study session ended after {human_readable_duration}")
    

bot.run(TOKEN)