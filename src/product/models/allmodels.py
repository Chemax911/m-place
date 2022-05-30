from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .basemodel import BaseModel


class Brand(BaseModel):

    class Meta:
        ordering = ['name']
        verbose_name = _('Бренды')
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
    logo = models.FileField(
        _('Логотип'), 
        upload_to='brand_upload', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('brand', (), {'slug': self.slug})


class ProducingCountry(BaseModel):

    class Meta:
        ordering = ['name']
        verbose_name = _('Страны-производители')
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
            'Слаг — это часть URL-адреса, которая идентифицирует страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(ProducingCountry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('producing_country', (), {'slug': self.slug})


class Store(BaseModel):

    class Meta:
        ordering = ['name']
        verbose_name = _('Магазины')
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
            'Слаг — это часть URL-адреса, которая идентифицирует страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    url_link = models.URLField(
        _('URL-ссылка'), 
        help_text=_(
            'Url адрес сайта'
        ),
        max_length=255, 
        null=True, 
        blank=True
    )
    logo = models.FileField(
        _('Логотип'), 
        upload_to='store_upload', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('store', (), {'slug': self.slug})
