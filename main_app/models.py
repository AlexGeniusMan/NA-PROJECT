from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from datetime import datetime


class Message(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    img = models.ImageField('Картинка', upload_to='messages', blank=True)
    short_description = models.TextField('Краткое описание', max_length=256)
    created_at = models.DateTimeField('Время публикации', default=datetime.now)
    content = models.JSONField('Содержание')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
