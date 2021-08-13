import os, pytube
from redvid import Downloader

reddit = Downloader()
	
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
    
    #ydl_opts = {
    #    'format': 'worst',  
    #    'outtmpl': 'savevideo.mp4'
    #}
    
    #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #    length = ydl.extract_info(url, download=False).get("duration")
    #    if length > lengthYoutube:
    #        return False
    #    else:
    #        return True
    
    if pytube.YouTube(url).length > lengthYoutube:
        return False
    
    else:
        return True

def downloadYoutube(url):
    
    #ydl_opts = {
    #    'format': 'worst',  
    #    'outtmpl': 'savevideo.mp4'
    #}
    
    #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download([url])
    
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
