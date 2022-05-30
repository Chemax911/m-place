from django.db import models
from django.urls import reverse
# from polymorphic.managers import PolymorphicManager
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# from feature.models import FeatureKey


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
        _('Порядок в списке подкатегорий'), 
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

        return ('category', (), {'slug': self.slug})


class SubCategory(BaseModel):

    class Meta:
        ordering = ['name']
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
    cat_id = models.IntegerField(
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
    parent = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),  
        related_name='parent_id', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('subcategory', (), {'slug': self.slug})


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
    type_id = models.IntegerField(
        _('Идентификатор'), 
        null=True, 
        blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name=_('Подкатегория'), 
        related_name='sub_category_id', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    # features = models.ManyToManyField(FeatureKey, verbose_name=_('Feature Key'), blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(ProductType, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''
    
        return ('product_type', (), {'slug': self.slug})


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


class Product(BaseModel):
    ''' Продукт '''

    class Meta:
        verbose_name = _('Товары')
        verbose_name_plural = verbose_name

    name = models.CharField(_('Название'), max_length=250)
    slug = models.SlugField(
        _('Слаг'), 
        max_length=255, 
        help_text=_(
            'Слаг — это часть URL-адреса, которая идентифицирует страницу с помощью удобочитаемых ключевых слов.'
        )
    )
    vendor_code = models.CharField(_('Код магазина'), max_length=50, null=True, blank=True)
    product_id = models.IntegerField(_('Идентификатор'), null=True, blank=True)
    sync_id = models.IntegerField(_('ID синхронизации'), null=True, blank=True, editable=False)
    product_type = models.ForeignKey(
        ProductType,
        verbose_name=_('Тип продукта'),
        related_name='product_type_id', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name=_('Подкатегория'),
        related_name='subcategory_id', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    brand = models.ForeignKey(
        Brand, 
        verbose_name=_('Бренд'),
        related_name='brand_id',
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    producing_country = models.ForeignKey(
        ProducingCountry, 
        verbose_name=_('Страна производитель'),
        related_name='producing_country_id', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    store = models.ForeignKey(
        Store, 
        verbose_name=_('Магазин'),
        related_name='store_id', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    image = models.URLField(_('Изображение'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    price = models.DecimalField(
        _('Цена'), 
        max_digits=6, 
        decimal_places=0, 
        null=True, 
        blank=True
    )
    markdown_price = models.DecimalField(
        _('Цена уценки'), 
        max_digits=6, 
        decimal_places=0, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        ''' Возвращает абсолютный URL. '''

        return ('product', (), {'slug': self.slug, 'id': self.id})
    
    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
