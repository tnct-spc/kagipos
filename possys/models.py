import json
import requests
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from slack import SLACK_URL
from django.forms.models import ModelMultipleChoiceField, ModelChoiceField
from users.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリー名', max_length=100, unique=True)

    class Meta:
        verbose_name = _('カテゴリー')
        verbose_name_plural = _('カテゴリー')


class CategoriesChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj: Category):
        return obj.name


class Product(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=100, unique=True)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='カテゴリー', blank=True)
    price = models.PositiveIntegerField(verbose_name='値段')

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')


class ProductChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: Category):
        return obj.name


class Transaction(models.Model):
    price = models.IntegerField(verbose_name='金額')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', verbose_name='ユーザー')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions', verbose_name='商品', blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name='取引時刻', default=timezone.now)

    class Meta:
        verbose_name = _('取引')
        verbose_name_plural = _('取引')

    def save(self, *args, **kwargs):
        self.user.wallet += self.price
        self.user.save()
        super().save(*args, **kwargs)
        notify_to_slack(self)


def notify_to_slack(transaction: Transaction):
    requests.post(
        SLACK_URL,
        json.dumps({
            'text': '*{0}* `id:{1}` <@{2}>'.format(
                transaction.timestamp.strftime("[%Y/%m/%d (%H:%M)]"),
                str(transaction.user_id),
                transaction.user.username
            ),
            'attachments': [
                {
                    'color': '#4169e1' if transaction.price < 0 else '#32cd32',
                    'text': '{0} ￥{1}'.format(
                        transaction.product.name if transaction.product is not None else 'チャージ',
                        abs(transaction.price)
                    )
                }
            ]
        }),
        headers={'Content-Type': 'application/json'}
    )
