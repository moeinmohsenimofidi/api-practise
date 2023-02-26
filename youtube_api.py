import os
import pandas as pd
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import json

CHANNEL_ID =["UCfM3zsQsOnfWNUppiycmBuw"]
API_KEY = "AIzaSyCVn30zAVbkG5GiJ7bV2nyeVU-agTnByaw"
playlist_id ="UUfM3zsQsOnfWNUppiycmBuw"
api_service_name = "youtube"
api_version = "v3"


# Get credentials and create an API client
youtube = build(
    api_service_name, api_version, developerKey=API_KEY)


def get_channel_state(youtube, channel_ids):

    all_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics ",
        id=",".join(CHANNEL_ID)
    )
    response = request.execute()

    for item in response["items"]:
        data = {"cahnnelName":item["snippet"]["title"],
                "subscribers": item["statistics"]["subscriberCount"],
                "views": item["statistics"]["viewCount"],
                "totalViews": item["statistics"]["videoCount"],
                "playlistId": item["contentDetails"]["relatedPlaylists"]["uploads"],
                }
        all_data.append(data)
    return (pd.DataFrame(all_data))

def get_video_ids(youtube,playlist_id):

    video_ids = list()

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50,

    )
    response = request.execute()
    for item in response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    next_page_token = response.get("nextPageToken")
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken= next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        next_page_token = response.get("nextPageToken")
    return video_ids


def get_video_details(youtube, video_ids):
    all_video_info = []
    for i in range(50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ids[i:i + 50],
            maxResults=50
        )
        response = request.execute()
        for video in response["items"]:
            state_to_keep = {
                "snippet": ["channelTitle", "title", "description", "tags", "publishedAt"],
                "statistics": ["viewCount", "likeCount", "favoriteCount", "commentCount"],
                "contentDetails": ["duration", "definition", "caption"]
            }
            video_info = {}
            video_info["video_id"] = video["id"]

            for k in state_to_keep.keys():
                for v in state_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info = None
            all_video_info.append(video_info)

    return all_video_info

#channel_state = get_channel_state(youtube, CHANNEL_ID)
#print(channel_state)
#print(json.dumps(response, indent = 2))
video_ids = get_video_ids(youtube, playlist_id)
print(video_ids)
#video_df = get_video_details(youtube,video_ids)
#print(json.dumps(video_df, indent=2)
