import discord, time, os, pytube
from redvid import Downloader
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

prefixes = ['sv ', 'Sv ', 'SV']
bot = commands.Bot(command_prefix = prefixes)
bot.remove_command("help")
load_dotenv('.env')

def isVideoCompatibleYoutube(url):

    if pytube.YouTube(url).length > 60:
        return False
    else:
        return True

def downloadYoutube(url):

    youtube = pytube.YouTube(url)
    stream = youtube.streams.first()
    stream.download(filename="video")
    print("Downloaded the YouTube video.")

def downloadReddit(url):
        
    reddit = Downloader()
    reddit.auto_max = True
    reddit.log = False
    reddit.url = url
    reddit.max_s = 7.5 * (1 << 20)
    
    if reddit.duration < 60:
        reddit.download()
    else:
        return False
    print("Downloaded the Reddit video.")  

def destruct(filename):

    if os.path.exists("video.mp4"):
        os.remove(filename)
        print("Destructed the video.")
    else:
        print("The path you wanted does not exist!")

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
    print('Bot is online.')

@bot.command(aliases=['VIDEO', 'Video'])
@commands.cooldown(1, 10, commands.BucketType.guild)
async def video(ctx, url):
    start = time.perf_counter()

    if "youtube.com" in url:
        if "/watch" in url:
            if isVideoCompatibleYoutube(url):
                async with ctx.typing():

                    try:
                        downloadYoutube(url)
                        stop = time.perf_counter()
                        await ctx.send(content=f"Processed in {stop - start:0.1f} seconds. Sent by {ctx.message.author.mention}", file=discord.File(fp="video.mp4"))
                        await ctx.message.delete()
                            
                        print("Sent the YouTube video!")
                        destruct("video.mp4")
                    except:
                        await ctx.send("Couldn't download the video from YouTube! (Video too big)")
                        destruct("video.mp4")
            else:
                await ctx.send("Your video is longer than 60 seconds!")    
        else:
            await ctx.send("This type of link isn't supported!")

    elif "youtu.be" in url:
        if isVideoCompatibleYoutube(url):
            async with ctx.typing():
                                      
                try:
                    downloadYoutube(url)
                    stop = time.perf_counter()
                    await ctx.send(content=f"Processed in {stop - start:0.1f} seconds. Sent by {ctx.message.author.mention}", file=discord.File(fp="video.mp4"))
                    await ctx.message.delete()
                            
                    print("Sent the YouTube video!")
                    destruct("video.mp4")
                except:
                    await ctx.send("Couldn't download the video from YouTube! (Video too big)")
                    destruct("video.mp4")
        else:
            await ctx.send("Your video is longer than 60 seconds!")
    elif "reddit.com" in url:
        if "/comments/" in url:
            async with ctx.typing():
          
                try:
                    downloadReddit(url)
                    stop = time.perf_counter()

                except:
                    await ctx.send("Couldn't download the video from Reddit! (Video too big)")
                                
                dir = []
                for file in os.listdir():
                    if file.endswith('.mp4'):
                        dir.append(file)
                os.rename(dir[0], "video.mp4")
                                
               
                try:
                    await ctx.send(content=f"Processed in {stop - start:0.1f} seconds. Sent by {ctx.message.author.mention}", file=discord.File(fp="video.mp4"))
                    await ctx.message.delete()
                    
                    print("Sent the reddit video!")
                    destruct("video.mp4")
                                    
                except:       
                    await ctx.send("Couldn't send the video from Reddit! (Video too big.)")
                    destruct("video.mp4")
                 
        else:
            await ctx.send("This type of link isn't supported!")
    else:
        await ctx.send("This platform isn't supported!")

@bot.command(aliases=['HELP', 'Help'])
async def help(ctx):
    embed = discord.Embed(
        title="How to use the SaveVideo:",
        description="Maximum video length is 60 seconds.",
        colour= discord.Color.blurple())
    
    embed.add_field(name='**sv ping**', value="Views the bot latency.", inline=False)
    embed.add_field(name='**sv help**', value="Displays the help command.", inline=False)
    embed.add_field(name='**sv video <url>**', value="Downloads the video from the given link and sends it.", inline=False)
    embed.add_field(name='**Links**', value='[Invite me!](https://discord.com/api/oauth2/authorize?client_id=783728124021702689&permissions=191488&scope=bot) - [Vote me!](https://top.gg/bot/783728124021702689/vote)')
    embed.set_thumbnail(url="https://i.hizliresim.com/orhNo4.png")
    embed.set_footer(icon_url="https://i.redd.it/1i6tmwht8y261.png", text=f"Supports YouTube and Reddit | Online in {len(bot.guilds)} servers.")
    await ctx.send(embed=embed)

@bot.command(aliases=['PING', 'Ping'])
async def ping(ctx):
    await ctx.send(f"Bot latency is: `{round(bot.latency * 1000)}ms`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to give me an URL!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Couldn't find that command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on cooldown. Try again in {error.retry_after:0.1f} seconds.")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))