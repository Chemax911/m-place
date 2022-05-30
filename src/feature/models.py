from django.db import models
from django.utils.translation import ugettext_lazy as _

from product.models import BaseModel, ProductType


class GroupsFeature(BaseModel):

    class Meta:
        verbose_name = _('Группы Особенностей')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'),
        max_length=255
    )
    product_type = models.ForeignKey(
        ProductType,
        verbose_name=_('Тип продукта'),
        on_delete=models.CASCADE,
        related_name='group_features',
        null=True
    )

    def __str__(self):
        return self.name


class FeatureKey(BaseModel):

    class Meta:
        verbose_name = _('Особенности')
        verbose_name_plural = verbose_name

    KIND = [
        ('choice', _('Choice')),
        ('range', _('Range')),
        ('bool', _('Bool')),
    ]

    group = models.ForeignKey(
        GroupsFeature,
        verbose_name=_('Группа Особенности'),
        on_delete=models.CASCADE,
        related_name='group_features',
        null=True
    )
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    slug = models.SlugField(
        _('Слаг'),
        max_length=255,
        unique=True,
        allow_unicode=True,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    kind = models.IntegerField(
        _('Вид'),
        choices=KIND
    )

    def __str__(self):
        return self.name


# class FeatureValue(BaseModel):
#
#     class Meta:
#         verbose_name = _('Значения')
#         verbose_name_plural = verbose_name
#
#     product = models.ForeignKey(
#         Product,
#         verbose_name=_('Продукт'),
#         on_delete=models.CASCADE,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     features = models.ForeignKey(
#         FeatureKey,
#         verbose_name=_('Особенность'),
#         on_delete=models.CASCADE,
#         db_index=True
#         )
#     value = models.CharField(
#         _('Значение'),
#         max_length=255
#     )
#
#     def __str__(self):
#         return self.value
