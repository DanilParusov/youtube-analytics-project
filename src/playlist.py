import datetime

import isodate
from googleapiclient.discovery import build
import os

api_key: str = os.getenv('API_KEY_YT')
youtube = build('youtube', 'v3', developerKey=api_key)
class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_response = youtube.playlists().list(part='snippet',id=self.playlist_id).execute()
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        playlist_response = youtube.playlistItems().list(part='contentDetails',playlistId=self.playlist_id,maxResults=50).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_response['items']]
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',id=','.join(video_ids)).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        playlist_response = youtube.playlistItems().list(part='contentDetails',playlistId=self.playlist_id,maxResults=50).execute()
        for video in playlist_response['items']:
            video_id = video['contentDetails']['videoId']
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',id=video_id).execute()
            best_video = max(video_response['items'], key=lambda x: int(x['statistics']['likeCount']))

        return f"https://youtu.be/{best_video['id']}"






