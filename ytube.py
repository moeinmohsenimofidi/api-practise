import os
import pandas as pd
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import re
import json
from pprint import pprint as pp
from datetime import timedelta

PLAYLIST_ID = "PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_"
find_view_playlistId = "PL8uoeex94UhHFRew8gzfFJHIpRFWyY4YW"
#CHANNEL_ID =["UCfM3zsQsOnfWNUppiycmBuw"]
API_KEY = "AIzaSyCVn30zAVbkG5GiJ7bV2nyeVU-agTnByaw"
api_service_name = "youtube"
api_version = "v3"

youtube = build(
    api_service_name, api_version, developerKey=API_KEY)


def get_channel_state(yotube, username):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        forUsername=username
    )
    response = request.execute()
    for item in response["items"]:

            title = item["snippet"]["title"]
            description = item["snippet"]["description"].split(".\n\n")[0]
            publishedAt = item["snippet"]["publishedAt"].split("T")[0]

    return print(title+"\n" + description + "\n" + publishedAt  + "\n")

def total_pl_duration(PLAYLIST_ID):

    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    second_pattern = re.compile(r'(\d+)S')

    total_seconds = 0

    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        video_ids = []
        for item in pl_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        video_request = youtube.videos().list(
                    part="contentDetails",
                    id=','.join(video_ids),
                    maxResults=50
        )

        video_response = video_request.execute()

        for item in video_response["items"]:
            duration = item["contentDetails"]["duration"]

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = second_pattern.search(duration)

            hours = int(hours.group(1) if hours else 0)
            minutes = int(minutes.group(1) if minutes else 0)
            seconds = int(seconds.group(1) if seconds else 0)

            video_second = int(timedelta(
                hours = hours,
                minutes = minutes,
                seconds = seconds
            ).total_seconds())
            total_seconds += video_second
        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken :
            break

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    print(f"Total playlist duration is {hours}:{minutes}:{seconds}" )

def find_popular_video_in_pl (PLAYLIST_ID):
    videos = list()
    nextPageToken = None
    pl_request = youtube.playlistItems().list(
        part="contentDetails ",
        playlistId=PLAYLIST_ID,
        maxResults=50,
        pageToken=nextPageToken
    )
    pl_response = pl_request.execute()

    video_ids = []
    for item in pl_response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    video_request = youtube.videos().list(
        part="statistics",
        id=','.join(video_ids),

    )

    video_response = video_request.execute()
    for item in video_response["items"]:
        vid_view = item["statistics"]["viewCount"]

        vid_id = item["id"]
        vid_link = f"https//youtube.be/{vid_id}"

        videos.append(
            {
            "views": int(vid_view),
            "url": vid_link
            }
        )


        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken:
            break
    videos.sort(key=lambda vid: vid["views"], reverse=True)

    output = {print(f' \n {video["url"]},Toal view is:{video["views"]}') for video in videos[:10]}
    return output



get_channel_state(youtube, "schafer5")
total_pl_duration(PLAYLIST_ID)
find_popular_video_in_pl(find_view_playlistId)