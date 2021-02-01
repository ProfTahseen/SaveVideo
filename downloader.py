import pytube, os
from redvid import Downloader
reddit = Downloader()

def checkReddit(url):

    if reddit.duration < 60:
        return False
    else:
        return True

def checkYoutube(url):

    if pytube.YouTube(url).length < 60:
        return False
    else:
        return True

def downloadYoutube(url):

    pytube.YouTube(url).streams.get_by_itag(18).download(filename="savevideo")

def downloadReddit(url):

    reddit.max_s = 7.5 * (1 << 20)
    reddit.auto_max = True
    reddit.log = False
    reddit.url = url
    reddit.download()

def renameReddit(name):

    dir = []
    for file in os.listdir():
        if file.endswith('.mp4'):
            dir.append(file)

    os.rename(dir[0], name)
