import discord, os, downloader
from discord.ext import commands
from keepAlive import keepAlive
from dotenv import load_dotenv

prefixes = ['sv ', 'Sv ']
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")
load_dotenv('.env')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
    print('Bot is online.')

@bot.command(aliases=['Video'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def video(ctx, url):
    if "reddit.com" and "/comments/" in url:
        async with ctx.typing():

            try:
                downloader.downloadReddit(url)
                downloader.renameReddit("savevideo.mp4")

                await ctx.send(content=f"Reddit video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
                print("Sent a Reddit video!")
                
                await ctx.message.delete()
                os.remove("savevideo.mp4")

            except:
                await ctx.send("Something went wrong getting the video.")
                print("Something went wrong getting the video.(Reddit)")
                
                await ctx.message.delete()
                os.remove("savevideo.mp4")

    elif "youtu.be" or "/watch" or "/shorts" in url:
        if downloader.checkYoutube(url):
            async with ctx.typing():

                try:
                    downloader.downloadYoutube(url)

                    await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
                    print("Sent the YouTube video!")
                    
                    await ctx.message.delete()
                    os.remove("savevideo.mp4")

                except:
                    await ctx.send("Something went wrong getting the video.")
                    print("Something went wrong getting the video.(YouTube)")
                    
                    await ctx.message.delete()
                    os.remove("savevideo.mp4")
        else:
            await ctx.send("Your video is longer than 60 seconds!")
    else:
        await ctx.send("This type of link isn't supported!")

@bot.command(aliases=['Help'])
async def help(ctx):
    embed = discord.Embed(
        title="How to use the SaveVideo:",
        description="Maximum video length is 60 seconds.\nSupports YouTube and Reddit.",
        colour=discord.Color.blurple())
    embed.add_field(name='**sv help**', value="Displays this message.", inline=False)
    embed.add_field(name='**sv stats**', value="Shows the bot's statistics.", inline=False)
    embed.add_field(name='**sv video <URL>**', value="Downloads the video from the given URL.", inline=False)
    embed.add_field(name='**Links**', value='[Invite](https://discord.com/api/oauth2/authorize?client_id=783728124021702689&permissions=8&scope=bot) - [Feedback Server](https://discord.gg/pqVPHNCuDD)')
    embed.set_thumbnail(url="https://i.hizliresim.com/orhNo4.png")

    await ctx.send(embed=embed)

@bot.command(aliases=['Stats'])
async def stats(ctx):
    await ctx.send(f"Bot latency is: `{round(bot.latency * 1000)}ms`\nBot is in `{len(bot.guilds)}` servers.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to provide an URL.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Couldn't find that command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on cooldown. Try again in {error.retry_after:0.1f} seconds.")

if __name__ == "__main__":
    keepAlive()
    bot.run(os.getenv('TOKEN'))
