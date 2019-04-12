from django.db import models
from django.utils import timezone

from users.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリー名', max_length=100, unique=True)


class Product(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=100, unique=True)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='カテゴリー', blank=True)
    price = models.PositiveIntegerField(verbose_name='値段')


class Transaction(models.Model):
    price = models.IntegerField(verbose_name='金額')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', verbose_name='ユーザー')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions', verbose_name='商品', blank=True)
    timestamp = models.DateTimeField(verbose_name='取引時刻', default=timezone.now)
