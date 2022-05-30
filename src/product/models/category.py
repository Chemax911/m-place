from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .basemodel import BaseModel


class Category(BaseModel):
    class Meta:
        ordering = ['id']
        verbose_name = _('Категории')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    order = models.IntegerField(
        _('Порядок в списке'),
        default=0,
        null=True,
        blank=True
    )
    icon = models.FileField(
        _('Иконка'), 
        upload_to='category/icon',
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.name

    def icon_tag(self):
        try:
            return mark_safe('<img src="%s" />' % self.icon.url)
        except:
            return 'None'
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''
        return 'category', (), {'slug': self.slug}


class SubCategory(BaseModel):

    class Meta:
        ordering = ['parent']
        verbose_name = _('Подкатегории')
        verbose_name_plural = verbose_name

    name = models.CharField(
        _('Название'), 
        max_length=250,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255,
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует '
            'страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    order = models.IntegerField(
        _('Порядок в списке категорий'),
        default=0,
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        related_name='children',
        on_delete=models.CASCADE,
        default=''
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''
        return 'subcategory', (), {'slug': self.slug}
