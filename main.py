import discord, downloader, time, os
from discord.ext import commands
from keep_alive import keep_alive

prefixes = ['sv ', 'Sv ']
bot = commands.Bot(command_prefix = prefixes)
bot.remove_command("help")
TOKEN = "NzgzNzI4MTI0MDIxNzAyNjg5.X8e9sQ.HvDWWhr4eX0S1XaG6q-xwCQY"

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
    print('Bot is online.')

@bot.command()
async def video(ctx, url):
    start = time.perf_counter()

    if "www.youtube.com/" in url:
        if "watch?v=" in url:
            if downloader.isVideoShortYoutube(url):

                async with ctx.typing():
                    downloader.downloadYoutube(url)
                    stop = time.perf_counter()
                    await ctx.send(content=f"Processed in {stop - start:0.1f} seconds. Sent by {ctx.message.author.mention}", file=discord.File(fp='video.mp4'))
                    await ctx.message.delete()

                downloader.destruct("video.mp4")
                print("Sent the YouTube video!")

            else:
                await ctx.send("Your video is longer than a minute!")
        else:
            await ctx.send("This type of link is unsupported!")

    elif "www.reddit.com/r/" in url and "/comments/" in url:

        async with ctx.typing():
            
            try:
                downloader.downloadReddit(url)
            except:
                await ctx.send("There is no video in this post!")

            dir = []
            for file in os.listdir():
                if file.endswith('.mp4'):
                    dir.append(file)

            os.rename(dir[0], 'video.mp4')

            stop = time.perf_counter()
            await ctx.send(content=f"Processed in {stop - start:0.1f} seconds. Sent by {ctx.message.author.mention}", file=discord.File(fp='video.mp4'))
            await ctx.message.delete()
        downloader.destruct('video.mp4')
        print("Sent the Reddit video!")

    else:
        await ctx.send("This platform is unsupported!")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="How to use the SaveVideo:",
        description="Maximum YouTube video lenght is 60 seconds.\nFor Reddit, it's limited with 7.5 MBs.",
        colour= discord.Color.blurple())
    embed.add_field(name='**sv ping**', value="View the bot latency.", inline=False)
    embed.add_field(name='**sv help**', value="Display the help command.", inline=True)
    embed.add_field(name='**sv video <url>**', value="Downloads the video from the given link.", inline=True)
    embed.set_thumbnail(url="https://i.redd.it/6x3d4crl6y261.png")
    embed.set_footer(icon_url="https://i.redd.it/1i6tmwht8y261.png", text="Supported platforms: YouTube and Reddit")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Bot latency is: `{round(bot.latency * 1000)}ms`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to give me an URL!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Couldn't find that command.")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)