import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """ Класс для работы с видео из Youtube """

    def __init__(self, id_video):
        """
        Экземпляр инициализируется по ID видео из Youtube.
        Далее все данные подтягиваются по API.
        :id_video: - id видео
        :video_title: - название видео
        :url_video: - ссылка на видео
        :view_count: - количество просмотров
        :like_count: - количество лайков
        """
        self.id_video = id_video
        self.video_title = self.video_data['items'][0]['snippet']['title']
        self.url_video = f'https://youtu.be/{self.id_video}'
        self.view_count = self.video_data['items'][0]['statistics']['viewCount']
        self.like_count = self.video_data['items'][0]['statistics']['likeCount']


    @property
    def video_data(self):
        """ Получаем список из данных по API - запросу """
        video_data = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.id_video).execute()
        return video_data


    def __str__(self):
        """
        Возвращает строку в формате '<название видео>'
        """
        return f'{self.video_title}'


class PLVideo(Video):
    """
    Класс инициализирует экземпляр по id видео и id плейлиста.
    """
    def __init__(self, id_video, id_playlist):
        """
        Экземпляр инициализируется по ID видео из Youtube и ID плейлиста.
        Остальные данные подтягиваются по API.
        :id_video: - id видео
        :video_title: - название видео
        :url_video: - ссылка на видео
        :view_count: - количество просмотров
        :like_count: - количество лайков
        :id_playlist: - id плейлиста
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist


    def __str__(self):
        """
        Возвращает строку в формате '<название видео>'
        """
        return super().__str__()