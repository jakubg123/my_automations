import settings
import discord
from discord.ext import commands, tasks
import datetime
import asyncio

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    reminders = []

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        check_reminders.start()
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

    @tasks.loop(seconds=60)
    async def check_reminders():
        current_time = datetime.datetime.now().time()
        for reminder in reminders[:]:
            if reminder['time'] <= current_time:
                channel = bot.get_channel(reminder["channel_id"])
                await channel.send(reminder["message"])
                reminders.remove(reminder)

    @bot.command()
    async def health_reminder(ctx):
        health_messages = ["Sit straight!", "Drink some water!", "Take a short break!"]
        for message in health_messages:
            await ctx.send(message)
            await asyncio.sleep(60)

    @bot.command()
    async def list_reminders(ctx):
        if not reminders:
            await ctx.send("No active reminders.")
            return

        reminder_list = "\n".join([f"Time: {r['time']}, Message: {r['message']}" for r in reminders])
        await ctx.send(f"Active reminders:\n{reminder_list}")

    @bot.command()
    async def servertime(ctx):
        """Get the current server time."""
        current_time = datetime.datetime.now()
        await ctx.send(f"Server's current time: {current_time.strftime('%H:%M:%S')}")


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
