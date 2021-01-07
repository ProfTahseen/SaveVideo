import discord, time, os, downloader
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

prefixes = ['sv ', 'Sv ']
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")
load_dotenv('.env')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="sv help"))
    print('Bot is online.')

@bot.command(aliases=['Video'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def video(ctx, url):
    start = time.perf_counter()
    
    if "youtube.com" in url:
        if "/watch" in url:  
            if downloader.checkLenght(url):                    
                try:        
                    async with ctx.typing():                
                        downloader.downloadYoutube(url)                          
                        try:       
                            await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", 
                            file=discord.File(fp="savevideo.mp4"))
                            await ctx.message.delete()
                            
                            stop = time.perf_counter()
                            print(f"Sent the YouTube video! ({stop - start:0.1f} seconds.)")
                            os.remove("savevideo.mp4")                   
                        except:    
                            await ctx.send("Couldn't upload the video to Discord!")
                            os.remove("savevideo.mp4")
                            await ctx.message.delete()
                except:
                    await ctx.send("Couldn't download the video from YouTube!")
                    await ctx.message.delete()
            else:
                await ctx.send("Your video is longer than 60 seconds!")
        
        elif "/shorts" in url:
            if downloader.checkLenght(url):                           
                try:  
                    async with ctx.typing():
                        downloader.downloadYoutube(url)                     
                        try:              
                            await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", 
                            file=discord.File(fp="savevideo.mp4"))
                            await ctx.message.delete()
                            
                            stop = time.perf_counter()
                            print(f"Sent the YouTube video! ({stop - start:0.1f} seconds.)")
                            os.remove("savevideo.mp4")                        
                        except:   
                            await ctx.send("Couldn't upload the video to Discord!")
                            os.remove("savevideo.mp4")     
                            await ctx.message.delete()
                except:
                    await ctx.send("Couldn't download the video from YouTube!")
                    await ctx.message.delete()
            else:
                await ctx.send("Your video is longer than 60 seconds!") 
        else:
            await ctx.send("This type of link isn't supported!")
    
    elif "youtu.be" in url:
        if downloader.checkLenght(url):                            
            try:  
                async with ctx.typing():
                    downloader.downloadYoutube(url)              
                    try:              
                        await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", 
                        file=discord.File(fp="savevideo.mp4"))
                        await ctx.message.delete()

                        stop = time.perf_counter()
                        print(f"Sent the YouTube video! ({stop - start:0.1f} seconds.)")
                        os.remove("savevideo.mp4") 
                    except:   
                        await ctx.send("Couldn't upload the video to Discord!")
                        os.remove("savevideo.mp4")     
                        await ctx.message.delete()
            except:
                await ctx.send("Couldn't download the video from YouTube!")  
                await ctx.message.delete()
        else:
            await ctx.send("Your video is longer than 60 seconds!") 
    
    elif "reddit.com" in url:
        if "/comments/" in url:
                
            try:     
                async with ctx.typing():
                    downloader.downloadReddit(url)
                        
                    dir = []
                    for file in os.listdir():
                        if file.endswith('.mp4'):
                            dir.append(file)
                    os.rename(dir[0], "savevideo.mp4")
                        
                    try:
                        await ctx.send(content=f"Reddit video sent by {ctx.message.author.mention}", 
                        file=discord.File(fp="savevideo.mp4"))
                        await ctx.message.delete()

                        stop = time.perf_counter()
                        print(f"Sent a Reddit video! ({stop - start:0.1f} seconds.)")
                        os.remove("savevideo.mp4")
                        
                    except:
                        await ctx.send("Couldn't upload the video to Discord!")
                        os.remove("savevideo.mp4")
                        await ctx.message.delete()
            except:
                await ctx.send("Couldn't download the video from Reddit!")
                await ctx.message.delete()
        else:
            await ctx.send("This type of link isn't supported!")
    
    else:
        await ctx.send("This platform isn't supported!")
        
@bot.command(aliases=['Help'])
async def help(ctx):
    embed = discord.Embed(
        title="How to use the SaveVideo:",
        description="Maximum video length is 60 seconds.\nSupports YouTube and Reddit.",
        colour=discord.Color.blurple())
    embed.add_field(name='**sv help**', value="Displays this message.", inline=False)
    embed.add_field(name='**sv status/stats**', value="Shows the bot's status.", inline=False)
    embed.add_field(name='**sv video <URL>**', value="Downloads the video from the given URL.", inline=False)
    embed.add_field(name='**Links**', value='[Invite!](https://discord.com/api/oauth2/authorize?client_id=783728124021702689&permissions=191488&scope=bot) - [bots.gg](https://discord.bots.gg/bots/783728124021702689) - [top.gg](https://top.gg/bot/783728124021702689)')
    embed.set_thumbnail(url="https://i.hizliresim.com/orhNo4.png")
    await ctx.send(embed=embed)

@bot.command(aliases=['Status', 'stats', 'Stats'])
async def status(ctx):
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
    keep_alive()
    bot.run(os.getenv('TOKEN'))