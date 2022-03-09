TOKEN = "ENTER TOKEN HERE"

import discord, os, pytube, webserver
from redvid import Downloader
from discord.ext import commands

reddit = Downloader()
prefixes = ['sv ', 'Sv ']
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")
	
def checkReddit(url, lengthReddit):
	reddit.url = url
	reddit.min = True
	reddit.log = False
	reddit.check()
	if reddit.duration > lengthReddit:
		return False
	else:
		return True

def checkYoutube(url, lengthYoutube):
	if pytube.YouTube(url).length > lengthYoutube:
		return False
	else:
		return True

def downloadYoutube(url):
	pytube.YouTube(url).streams.get_by_itag(18).download(filename="savevideo.mp4")

def renameReddit(name):
	dir = []
	for file in os.listdir():
		if file.endswith('.mp4'):
			dir.append(file)
	os.rename(dir[0], name)
            
def downloadReddit(url):
	reddit.max_s = 7.5 * (1 << 20)
	reddit.auto_max = True
	reddit.log = False
	reddit.url = url
	reddit.download()

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
	print('Bot is online.')

@bot.command(aliases=['Video'])
@commands.cooldown(1, 15, commands.BucketType.default)
async def video(ctx, url):
	if "youtu" in url:
		try:
			async with ctx.typing():
				if checkYoutube(url, 60):
					downloadYoutube(url)
					await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
					os.remove("savevideo.mp4")
					await ctx.message.delete()
				else:
					await ctx.send("Your video is longer than 60 seconds!\n(The reason behind this is the Discord upload limit.)", delete_after=5.0)
					await ctx.message.delete(delay=5)
		except:
			await ctx.send("Something went wrong while getting the video.\nTo notify the developers: https://discord.gg/vNmAgsB3uV")
			os.remove("savevideo.mp4")
			print(f"Something went wrong while getting the video. (YouTube)\n{url}")
	elif "/comments/" in url:
		try:
			async with ctx.typing():
				if checkReddit(url, 60):
					downloadReddit(url)
					renameReddit("savevideo.mp4")
					await ctx.send(content=f"Reddit video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
					os.remove("savevideo.mp4")
					await ctx.message.delete()
				else:
					await ctx.send("Your video is longer than 60 seconds!\n(The reason behind this is the Discord upload limit.)", delete_after=5.0)
					await ctx.message.delete(delay=5)
		except:
			await ctx.send("Something went wrong while getting the video.\nTo notify the developers: https://discord.gg/vNmAgsB3uV")
			os.remove("savevideo.mp4")
			print(f"Something went wrong while getting the video. (Reddit)\n{url}")
	else:
		await ctx.send("That platform is not supported.", delete_after=5.0)
		await ctx.message.delete(delay=5)

@bot.command(aliases=['Help'])
async def help(ctx):
	embed = discord.Embed(
		title="SaveVideo Support",
		description="Maximum video length is 60 seconds.\nSupports YouTube and Reddit.",
		colour=discord.Color.blurple())
	embed.add_field(name='**sv help**', value="Displays this message.", inline=False)
	embed.add_field(name='**sv stats**', value="Shows the bot's statistics.", inline=False)
	embed.add_field(name='**sv video <URL>**', value="Downloads the video from the given URL.", inline=False)
	embed.add_field(name='[Source Code](https://github.com/Tahsinalp267/SaveVideo)', value='')
	embed.set_thumbnail(url="https://i.hizliresim.com/bbv58bh.png")
	await ctx.send(embed=embed)

@bot.command(aliases=['Stats'])
async def stats(ctx):
	await ctx.send(f"Bot latency: `{round(bot.latency * 1000)}ms`\nTotal servers: `{len(bot.guilds)}`\nTotal users: `{sum(guild.member_count for guild in bot.guilds)}`")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You have to provide an URL to download from.", delete_after=5.0)
		await ctx.message.delete(delay=5)
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("Couldn't find that command you're looking for.", delete_after=5.0)
		await ctx.message.delete(delay=5)
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"Command is on interserveral cooldown. Try again in {error.retry_after:0.1f} seconds.", delete_after=5.0)
		await ctx.message.delete(delay=5)

if __name__ == "__main__":
    bot.run(TOKEN)
