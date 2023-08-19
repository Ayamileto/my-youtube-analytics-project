import datetime
import os

import isodate
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

    def __str__(self):
        """ Возвращает строку c общим количеством времени всего плейлиста """
        return f"{self.total_duration}"

    @property
    def playlist_id(self):
        """ Получение данных плейлиста от его id через API-запрос """
        playlist_data = youtube.playlists().list(
            part="snippet",
            id=self._playlist_id,
            maxResults=50
        ).execute()
        return playlist_data

    def get_video_ids(self):
        """
        Функция возвращает список всех ID из плейлиста
        """
        video_ids = []
        nextPageToken = None

        while True:
            playlist_items = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=self._playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            for item in playlist_items['items']:
                video_ids.append(item['contentDetails']['videoId'])

            nextPageToken = playlist_items.get('nextPageToken')

            if not nextPageToken:
                break
        return video_ids

    @property
    def video_response(self):
        """ Возвращают данные всех видео из плейлиста по их ID """
        video_response = youtube.videos().list(
            part='contentDetails, statistics',
            id=','.join(self.get_video_ids())
        ).execute()
        return video_response

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста
        """
        total_duration = datetime.timedelta(seconds=0)

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        best_video = None
        max_likes = -1

        for video in self.video_response['items']:
            if 'likeCount' in video['statistics']:
                likes = int(video['statistics']['likeCount'])
                if likes > max_likes:
                    max_likes = likes
                    best_video = video

        if best_video:
            video_id = best_video['id']
            video_url = f"https://youtu.be/{video_id}"
            return video_url
        else:
            return None