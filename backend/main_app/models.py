# from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

CATEGORIES = (
    ('Спорт', 'Спорт'),
    ('Политика', 'Политика'),
    ('Наука', 'Наука'),
    ('Мир', 'Мир'),
    ('Культура', 'Культура'),
    ('Экономика', 'Экономика'),
    ('Интернет', 'Интернет'),
)


class Message(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    img = models.ImageField('Картинка', upload_to='messages', blank=True)
    short_description = models.TextField('Краткое описание', max_length=256)
    created_at = models.DateTimeField('Время публикации', default=datetime.now)
    content = models.JSONField('Содержание', null=True, blank=True)
    category = models.CharField("Категория", choices=CATEGORIES, max_length=64, blank=True)
    view_counter = models.IntegerField('Счетчик просмотров', null=True, default=0)
    is_pinned = models.BooleanField('Новость закреплена', default=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, title, img, short_description, created_at, content, category):
        message = cls(title=title, img=img, short_description=short_description, created_at=created_at, content=content,
                      category=category)
        return message
