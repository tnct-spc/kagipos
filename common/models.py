from django.db import models

from users.models import User


class Card(models.Model):
    is_guest = models.BooleanField(verbose_name='ゲスト', default=True)
    name = models.CharField(verbose_name='カード名', max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards', verbose_name='所持ユーザー')
    idm = models.BigIntegerField(verbose_name='FeliCa ID', unique=True)
