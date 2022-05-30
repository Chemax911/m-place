from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('Базовые модели')
        verbose_name_plural = verbose_name

    created_at = models.DateTimeField(
        _('Дата и время создания'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('Дата и время обновления'),
        auto_now=True,
    )
    active = models.BooleanField(
        _('Активный'),
        default=True,
        help_text=_('Является активным.'),
    )
    