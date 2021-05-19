# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

PATTERN = r".*list=(.*)"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def export(playlist_url):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    file = open('youtube/api_key.json')
    cred = json.load(file)
    api_key = cred['api-key']

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    # Get playlist url
    match = re.match(PATTERN, playlist_url)
    playlist_id = None
    if match:
        playlist_id = match[1]
    else:
        print('URL is not a playlist. Failed YouTube playlist PATTERN match.')
        exit()

    # Get playlist title info
    request = youtube.playlists().list(
        part='snippet',
        id=playlist_id
    )
    response = request.execute()
    print(response)
    playlist_name = response['items'][0]['snippet']['title']

    playlist = {"title": playlist_name, "url": playlist_url, "videos": []}
    nextPageToken = ''
    while nextPageToken is not None:
        try:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )

            response = request.execute()
            for video in response["items"]:
                playlist["videos"].append({"title": video["snippet"]["title"], "id": f"https://youtu.be/{video['snippet']['resourceId']['videoId']}"})
            
            if "nextPageToken" in response.keys():
                nextPageToken = response["nextPageToken"]
            else:
                nextPageToken = None
        except googleapiclient.errors.HttpError:
            print("Error: Given URL is not a valid playlist. Is the playlist private?")
            exit()
        except Exception as e:
            print(f"Error: Unknown Error - {e}")
            exit()


    for video in playlist["videos"]:
        print(video["title"])
        print(video["id"])
    
    outfile = open("output.json", "w")
    json.dump(playlist, outfile, indent=4)