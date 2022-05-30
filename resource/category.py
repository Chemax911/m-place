from django.db import models
from django.urls import reverse
# from polymorphic.managers import PolymorphicManager
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .basemodel import BaseModel


class GroupCategory(BaseModel):

    class Meta:
        ordering = ['order']
        verbose_name = _('Группы Категорий')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    category_id = models.IntegerField(
        _('Идентификатор'),
        default=0,
        null=True, 
        blank=True
    )
    order = models.IntegerField(
        _('Порядок в списке'),
        default=0, 
        null=True, 
        blank=True
    )
    icon = models.FileField(
        _('Иконка'), 
        upload_to='category-icon_upload',
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('groupcategory', (), {'slug': self.slug})


class Category(BaseModel):

    class Meta:
        ordering = ['name']
        verbose_name = _('Категории')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    category_id = models.IntegerField(
        _('Идентификатор'),
        default=0,
        null=True, 
        blank=True
    )
    order = models.IntegerField(
        _('Порядок в списке категорий'),
        default=500, 
        null=True, 
        blank=True
    )
    group_category = models.ForeignKey(
        GroupCategory,
        verbose_name=_('Группа Категорий'), 
        related_name='group_cat_id', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('category', (), {'slug': self.slug})


class SubCategory(BaseModel):

    class Meta:
        ordering = ['parent_category']
        verbose_name = _('Подкатегории')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    category_id = models.IntegerField(
        _('Идентификатор'),
        default=0,
        null=True, 
        blank=True
    )
    order = models.IntegerField(
        _('Порядок в списке подкатегорий'), 
        default=500, 
        null=True, 
        blank=True
    )
    parent_category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),  
        related_name='cat_id', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('subcategory', (), {'slug': self.slug})
