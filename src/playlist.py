import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList:
    """
    Класс для работы с плейлистами, инициализируется _id_ плейлиста
    """

    def __init__(self, playlist_id):
        """ Инициализация по id плейлиста"""
        self._playlist_id = playlist_id
        self.title = self.playlist_id['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    @property
    def playlist_id(self):
        """ Получение данных плейлиста от его id через API-запрос """
        playlist_data = youtube.playlists().list(
            part="snippet",
            id=self._playlist_id,
            maxResults=50
        ).execute()
        return playlist_data





