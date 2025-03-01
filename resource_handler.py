"""
It is the responsibility of the calling script to delete the resource after consumed (for now)
"""

# Basic deps
import requests
import os, time, json

from ensembledata.api import EDClient
import constants # make a constants.py file and define API keys
from textscraper import scrape_article
# YouTube resource getter
from pytubefix import YouTube
from pytubefix.cli import on_progress

# time for unique file names
dl_time = int(time.time()//10000)

# please use this API sparingly, as it is a paid API
# flag to enable actual API calls
USE_API = False

client = EDClient(constants.EDCLIENT_API_TOKEN)


def resourceHandler(url: str):
    # Router that the type of resource and calls the appropriate handler
    # for now, ensembledata API handles pretty much everything
    if "tiktok" in url:
        return tiktokHandler(url)
    elif "youtu" in url:
        return youtubeHandler(url)
    elif "insta" in url:
        return instagramHandler(url)
    else:
        scrape_article(url)


def tiktokHandler(url: str):
    # TikTok handler
    if not USE_API:
        print("API not enabled")
        resultData = json.load(open(os.path.join("logs","tiktok_data.json"))) # default to the testing

    else: resultData = client.tiktok.post_info(url=url).data

    # save result.data to logs/ using os path so that it supports windows paths
    with open(os.path.join("logs", f"tiktok_data_{dl_time}.json"), "w") as f:
        f.write(resultData)

    # download video to resource/ using os path so that it supports windows paths and requests
    video = requests.get(resultData.video.download_addr.url_list[0])
    with open(os.path.join("resource", f"tiktok_{dl_time}.mp4"), "wb") as f:
        f.write(video.content)

    return os.path.join("resource", f"tiktok_{dl_time}.mp4")


def youtubeHandler(url: str):
    yt = YouTube(url)
    ys = yt.streams.get_by_resolution("360p")
    if ys==None:
        ys = yt.streams.get_highest_resolution()
    assert ys != None, "No video streams found"
    ys.download(output_path="resource", filename=f"youtube_{dl_time}")
    captions = yt.captions['a.en'].save_captions(os.path.join("resource",f"youtube_cc_{dl_time}"))
    return os.path.join("resource", f"youtube_{dl_time}.mp4")


def instagramHandler(url: str):
    pass

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=FW2XOIxaNqg&t=19s"
    # test youtube
    print(youtubeHandler(url))
