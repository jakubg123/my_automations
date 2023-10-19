import discord
from discord.ext import tasks, commands
import asyncio
import datetime
import settings
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

reminders = []
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')


@tasks.loop()
async def sit_straight_task(channels: list):
    for channel in channels:
        await channel.send("sit straight!")


@tasks.loop()
async def drink_water_task(channels: list):
    for channel in channels:
        await channel.send("drink some water!")


@tasks.loop()
async def do_pushups(channels: list):
    for channel in channels:
        await channel.send("push-ups!")


@tasks.loop(seconds=60)
async def check_reminders():
    current_time = datetime.datetime.now().time()
    for reminder in reminders[:]:
        if reminder['time'] <= current_time:
            channel = bot.get_channel(reminder["channel_id"])
            await channel.send(reminder["message"])
            reminders.remove(reminder)


def setup_reminder(task, channels, interval_minutes=None, interval_hours=None):
    task.start(channels)
    if interval_minutes:
        task.change_interval(minutes=interval_minutes)
    elif interval_hours:
        task.change_interval(hours=interval_hours)


@bot.command()
async def remind(ctx, time, *, message):
    try:
        reminder_time = datetime.datetime.strptime(time, '%H:%M').time()
        current_time = datetime.datetime.now().time()
        if reminder_time <= current_time:
            await ctx.send("Please provide a future time.")
            return
        reminders.append({
            "channel_id": ctx.channel.id,
            "time": reminder_time,
            "message": message
        })
        await ctx.send(f"Reminder set for {time}!")
    except ValueError:
        await ctx.send("Please use HH:MM format.")


@bot.command()
async def list_reminders(ctx):
    if not reminders:
        await ctx.send("No active reminders.")
        return
    reminder_list = "\n".join([f"Time: {r['time']}, Message: {r['message']}" for r in reminders])
    await ctx.send(f"Active reminders:\n{reminder_list}")


@bot.command()
async def servertime(ctx):
    current_time = datetime.datetime.now()
    await ctx.send(f"Server's current time: {current_time.strftime('%H:%M:%S')}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 100):
    await ctx.channel.purge(limit=amount + 1)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear_last_5(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)


@bot.command(name='listcommands')
async def list_commands(ctx):
    command_list = []
    for cmd in bot.commands:
        command_list.append(f"{cmd.name} - {cmd.help}")
    await ctx.send("\n".join(command_list))


def get_latest_tweets(username, count=5):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://twitter.com/{username}')
    driver_wait = WebDriverWait(driver, 30)
    confirm = driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Not now']"))).click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tweets = soup.find_all(attrs={"data-testid": "tweetText"})

    tweet_texts = [tweet.get_text() for tweet in tweets[:count]]
    driver.quit()

    return tweet_texts


@bot.command()
async def tweets(ctx, username: str):
    tweet_texts = get_latest_tweets(username)
    for tweet_text in tweet_texts:
        await ctx.send(tweet_text)
