import pytube, os
from redvid import Downloader

def isVideoShortYoutube(url):

    videoLength = pytube.YouTube(url).length

    if videoLength > 60 :
        return False
    else:
        return True

def downloadReddit(url):

    reddit = Downloader()
    reddit.auto_max = True
    reddit.max_s = 7.5 * (1 << 20)
    reddit.url = url
    reddit.download()
    print("Downloaded the video from Reddit.")

def downloadYoutube(url):

    pytube.YouTube(url).streams.get_highest_resolution().download(filename = "video")
    print("Downloaded the video from YouTube.")

def destruct(filename):

    if os.path.exists(filename):
        os.remove(filename)
        print("Destructed the video.")