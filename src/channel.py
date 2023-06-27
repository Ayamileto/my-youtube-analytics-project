import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not isinstance(channel_id, str):
            raise ValueError('channel_id должно быть строкой')
        self.channel_id = channel_id
        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.custom_url = self.channel_data['items'][0]['snippet']['customUrl']
        self.url = f"https://www.youtube.com/{self.custom_url}"
        print(self.url)
        self.subscriber_count = int(self.channel_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel_data['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel_data['items'][0]['statistics']['viewCount'])

    @property
    def channel_data(self):
        """ Получаем список из данных по API-запросу """
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.channel_data
        print(json.dumps(channel, indent=2, ensure_ascii=False))

