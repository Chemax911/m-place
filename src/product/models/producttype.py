from django.db import models
from django.urls import reverse
# from polymorphic.managers import PolymorphicManager
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .basemodel import BaseModel
from .category import SubCategory


class ProductType(BaseModel):
    ''' Тип продукта '''

    class Meta:
        ordering = ['name']
        verbose_name = _('Типы продуктов')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255, 
        unique=True, 
        allow_unicode=True,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name=_('Подкатегория'), 
        related_name='sub_category_id', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(ProductType, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''
        return ('product_type', (), {'slug': self.slug})
