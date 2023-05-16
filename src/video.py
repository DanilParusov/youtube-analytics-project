from googleapiclient.discovery import build
import json
import os

api_key: str = os.getenv('API_KEY_YT')
youtube = build('youtube', 'v3', developerKey=api_key)

class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',id=video_id).execute()

        self.title = video_response["items"][0]["snippet"]["title"]
        self.viewCount = video_response["items"][0]["statistics"]["viewCount"]
        self.likeCount = video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

