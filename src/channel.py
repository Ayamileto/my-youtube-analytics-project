import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб - канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        if not isinstance(channel_id, str):
            raise ValueError('channel_id должно быть строкой')
        self.__channel_id = channel_id
        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.custom_url = self.channel_data['items'][0]['snippet']['customUrl']
        self.url = f"https://www.youtube.com/{self.custom_url}"
        self.subscriber_count = int(self.channel_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel_data['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel_data['items'][0]['statistics']['viewCount'])


    def __str__(self):
        """
        Возвращает строку в формате `<название_канала> (<ссылка_на_канал>)`
        """
        return f"{self.title} ({self.url})"


    def __add__(self, other):
        """ Возвращает результат от суммы подписчиков двух каналов """
        add_ = self.subscriber_count + other.subscriber_count
        return add_


    def __sub__(self, other):
        """ Возвращает результат вычитания подписчиков двух каналов """
        sub_ = self.subscriber_count - other.subscriber_count
        return sub_


    def __gt__(self, other):
        """
        Возвращает True или False если условие сравнения
        подписчиков двух каналов верны или нет соответственно
        """
        gt_ = self.subscriber_count > other.subscriber_count
        return gt_


    def __ge__(self, other):
        """
        Возвращает True или False если условие сравнения
        подписчиков двух каналов верны или нет соответственно
        """
        ge_ = self.subscriber_count > other.subscriber_count
        return ge_


    def __lt__(self, other):
        """
        Возвращает True или False если условие сравнения
        подписчиков двух каналов верны или нет соответственно
        """
        lt_ = self.subscriber_count < other.subscriber_count
        return lt_


    def __le__(self, other):
        """
        Возвращает True или False если условие сравнения
        подписчиков двух каналов верны или нет соответственно
        """
        le_ = self.subscriber_count < other.subscriber_count
        return le_


    def __eq__(self, other):
        """
        Возвращает True или False если число
        подписчиков двух каналов равны или нет соответственно
        """
        if self.subscriber_count == other.subscriber_count:
            return True
        return False

    @property
    def channel_id(self):
        """Возвращает и защищает от изменений id канала."""
        return self.__channel_id


    @property
    def channel_data(self):
        """ Получаем список из данных по API - запросу """
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.channel_data
        print(json.dumps(channel, indent=2, ensure_ascii=False))


    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API """
        channel = cls.channel_data
        return channel


    def to_json(self, filename):
        """ Сохраняет в файл значения атрибутов экземпляра `Channel` в формате:
        'channel_id':  id канала,
        'title': название канала,
        'description': описание канала,
        'url': ссылка на канал,
        'subscriber_count': количество подписчиков,
        'video_count': количество видео,
        'view_count': общее количество просмотров
        """
        info_channel_data = filename
        searching_data = {
            'channel_id':  self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
         }
        with open(info_channel_data, "w") as file:
            # Записываем данные в файл JSON
            json.dump(searching_data, file, indent=2, ensure_ascii=False)

