import settings
import discord
from discord.ext import commands, tasks
import datetime
from tasks import *
import asyncio
logger = settings.logging.getLogger("bot")

def run():

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        my_channel = [bot.get_channel(int(settings.DISCORD_CHANNEL))]
        print(my_channel)
        setup_reminder(sit_straight_task, my_channel, interval_minutes=15)
        await asyncio.sleep(60)
        setup_reminder(drink_water_task, my_channel, interval_minutes=30, interval_hours=1)
        await asyncio.sleep(60)
        setup_reminder(do_pushups, my_channel, interval_hours=3)
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
