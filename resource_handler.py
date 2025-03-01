"""
It is the responsibility of the calling script to delete the resource after consumed (for now)
"""

# Basic deps
import requests
import os, time, json
from dotenv import load_dotenv

from ensembledata.api import EDClient
# import constants # make a constants.py file and define API keys
from textscraper import scrape_article

# YouTube resource getter
from pytubefix import YouTube
from pytubefix.cli import on_progress

# time for unique file names
dl_time = int(time.time()) - 1740840000

# please use this API sparingly, as it is a paid API
# flag to enable actual API calls
USE_API = False

load_dotenv()
EDCLIENT_API_TOKEN = os.getenv("EDCLIENT_API_TOKEN")
client = EDClient(EDCLIENT_API_TOKEN)


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
        resultData = json.load(open(os.path.join("logs","tiktok_data_7558.json"))) # default to the testing

    else:
        resultData = client.tiktok.post_info(url=url).data

        # save result.data to logs/ using os path so that it supports windows paths
        with open(os.path.join("logs", f"tiktok_data_{dl_time}.json"), "w") as f:
            json.dump(resultData[0], f)

        resultData=resultData[0]

    # download video to resource/ using os path so that it supports windows paths and requests
    video = requests.get(resultData['video']['download_addr']['url_list'][0])
    with open(os.path.join("resource", f"tiktok_{dl_time}.mp4"), "wb") as f:
        f.write(video.content)

    return os.path.join("resource", f"tiktok_{dl_time}.mp4")

def instagramHandler(url: str):
    # extract the shortcode from the url of this form https://www.instagram.com/reels/DFoV0rzP68Y/
    code = url.split("/")[-2]
    if not USE_API:
        print("API not enabled")
        resultData = json.load(open(os.path.join("logs","instagram_data.json")))['data']
    else: resultData = client.instagram.post_info_and_comments(code=code,num_comments=0).data

    # download the video
    video = requests.get(resultData['video_url'])
    with open(os.path.join("resource", f"instagram_{dl_time}.mp4"), "wb") as f:
        f.write(video.content)

    return os.path.join("resource", f"instagram_{dl_time}.mp4")

def youtubeHandler(url: str):
    yt = YouTube(url)
    ys = yt.streams.get_by_resolution("360p")
    if ys==None:
        ys = yt.streams.get_highest_resolution()
    assert ys != None, "No video streams found"
    ys.download(output_path="resource", filename=f"youtube_{dl_time}")
    captions = yt.captions['a.en'].save_captions(os.path.join("resource",f"youtube_cc_{dl_time}"))
    return os.path.join("resource", f"youtube_{dl_time}.mp4")



if __name__ == "__main__":
    url = "https://www.tiktok.com/@nianaguerrero/video/7465679997978610951?is_from_webapp=1&sender_device=pc"
    print(resourceHandler(url))
