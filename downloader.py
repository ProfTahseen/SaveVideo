import pytube
from redvid import Downloader

def checkLenght(url):

    if pytube.YouTube(url).length > 60:
        return False
    else:
        return True

def downloadYoutube(url):

    pytube.YouTube(url).streams.get_by_itag(18).download(filename="savevideo")

def downloadReddit(url):

    reddit = Downloader()
    reddit.max_s = 7.5 * (1 << 20)
    reddit.auto_max = True
    reddit.log = False
    reddit.url = url

    if reddit.duration < 60:
        reddit.download()
    else:
        return False