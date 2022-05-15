import discord, os, pytube
from discord.ext import commands
from datetime import datetime, timezone, timedelta

bot = commands.Bot(command_prefix=['sv ', 'Sv '], case_insensitive=True)
bot.remove_command("help")
TOKEN = os.environ['TOKEN']

def checkYoutube(url, lengthYoutube):
	if pytube.YouTube(url).length > lengthYoutube:
		return False
	else:
		return True

def downloadYoutube(url):
	pytube.YouTube(url).streams.get_by_itag(18).download(filename="savevideo.mp4")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
	print(f"\nBot online.\n{datetime.now(timezone(timedelta(hours=+3))).time()}")	

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.default)
async def video(ctx, url):
	async with ctx.typing():
		if "youtu" in url:
			try:
				if checkYoutube(url, 60):
					downloadYoutube(url)
					await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
					await ctx.message.delete()
					os.remove("savevideo.mp4")
					print(f"\nYoutube video sent by {ctx.message.author.mention}\n{url}\n{datetime.now(timezone(timedelta(hours=+3))).time()}")
				else:
					await ctx.send("Your video is longer than 60 seconds.\n(Reason behind is the upload limit.)\nhttps://github.com/discord/discord-api-docs/issues/2037", delete_after=5.0)
					await ctx.message.delete(delay=5)
					print(f"\nYour video is longer than 60 seconds.\n{url}\n{datetime.now(timezone(timedelta(hours=+3))).time()}")
			except:
				await ctx.send("Something went wrong while getting the video.\nTo notify the developers: https://discord.gg/vNmAgsB3uV")
				print(f"\nSomething went wrong while getting the video.\n{url}\n{datetime.now(timezone(timedelta(hours=+3))).time()}")
				os.remove("savevideo.mp4")
		else:
			await ctx.send("That platform is not supported yet. ", delete_after=5.0)
			await ctx.message.delete(delay=5)
			print(f"\nThat platform is not supported yet.\n{url}\n{datetime.now(timezone(timedelta(hours=+3))).time()}")	
		
@bot.command()
async def help(ctx):
	embed = discord.Embed(
		title="SaveVideo Support",
		description="Maximum video length is 60 seconds.\nOnly supports YouTube for now.",
		colour=discord.Color.blurple())
	embed.add_field(name='**sv help**', value="Displays this help message.", inline=False)
	embed.add_field(name='**sv stats**', value="Shows the bot's statistics.", inline=False)
	embed.add_field(name='**sv video <URL>**', value="Downloads the video from the given URL.", inline=False)
	embed.add_field(name='Links', value='[Source Code](https://github.com/Tahsinalp267/SaveVideo)')
	embed.set_thumbnail(url="https://i.hizliresim.com/bbv58bh.png")
	await ctx.send(embed=embed)
	print(f"\nhelp\n{datetime.now(timezone(timedelta(hours=+3))).time()}")

@bot.command()
async def stats(ctx):
	await ctx.send(f"Bot latency: `{round(bot.latency * 1000)}ms`\nTotal servers: `{len(bot.guilds)}`\nTotal users: `{sum(guild.member_count for guild in bot.guilds)}`")
	print(f"\nstats\n{datetime.now(timezone(timedelta(hours=+3))).time()}")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You have to provide an URL to download videos from.", delete_after=5.0)
		await ctx.message.delete(delay=5)
		print(f"\nMissingRequiredArgument\n{datetime.now(timezone(timedelta(hours=+3))).time()}")
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("Couldn't find that command you're looking for.", delete_after=5.0)
		await ctx.message.delete(delay=5)
		print(f"\nCommandNotFound\n{datetime.now(timezone(timedelta(hours=+3))).time()}")
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"Command is on interserveral cooldown. Try again in {error.retry_after:0.1f} seconds.", delete_after=5.0)
		await ctx.message.delete(delay=5)
		print(f"\nCommandOnCooldown\n{datetime.now(timezone(timedelta(hours=+3))).time()}")

bot.run(TOKEN)
