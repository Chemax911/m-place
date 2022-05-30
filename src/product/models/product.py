# from django.db import models
# from django.urls import reverse
# # from polymorphic.managers import PolymorphicManager
# from django.contrib.contenttypes.models import ContentType
# from django.utils.text import slugify
# from django.utils.translation import ugettext_lazy as _
#
# from .basemodel import BaseModel
# from .category import SubCategory
# from .producttype import ProductType
# from .allmodels import Brand, ProducingCountry, Store
#
#
# class Product(BaseModel):
#     ''' Продукт '''
#
#     class Meta:
#         verbose_name = _('Товары')
#         verbose_name_plural = verbose_name
#
#     name = models.CharField(_('Название'), max_length=250)
#     slug = models.SlugField(
#         _('Слаг'),
#         max_length=255,
#         help_text=_(
#             'Слаг — это часть URL-адреса, которая идентифицирует страницу с помощью удобочитаемых ключевых слов.'
#         )
#     )
#     vendor_code = models.CharField(_('Код магазина'), max_length=50, null=True, blank=True)
#     product_id = models.IntegerField(_('Идентификатор'), null=True, blank=True)
#     sync_id = models.IntegerField(_('ID синхронизации'), null=True, blank=True, editable=False)
#     product_type = models.ForeignKey(
#         ProductType,
#         verbose_name=_('Тип продукта'),
#         related_name='product_type_id',
#         on_delete=models.CASCADE,
#         default=''
#     )
#     subcategory = models.ForeignKey(
#         SubCategory,
#         verbose_name=_('Подкатегория'),
#         related_name='subcategory_id',
#         on_delete=models.CASCADE,
#         default=''
#     )
#     brand = models.ForeignKey(
#         Brand,
#         verbose_name=_('Бренд'),
#         related_name='brand_id',
#         on_delete=models.CASCADE,
#         default=''
#     )
#     producing_country = models.ForeignKey(
#         ProducingCountry,
#         verbose_name=_('Страна производитель'),
#         related_name='producing_country_id',
#         on_delete=models.CASCADE,
#         default=''
#     )
#     store = models.ForeignKey(
#         Store,
#         verbose_name=_('Магазин'),
#         related_name='store_id',
#         on_delete=models.CASCADE,
#         default=''
#     )
#     image = models.URLField(_('Изображение'), max_length=255, null=True, blank=True)
#     description = models.TextField(_('Описание'), null=True, blank=True)
#     price = models.DecimalField(
#         _('Цена'),
#         max_digits=6,
#         decimal_places=0,
#         null=True,
#         blank=True
#     )
#     markdown_price = models.DecimalField(
#         _('Цена уценки'),
#         max_digits=6,
#         decimal_places=0,
#         null=True,
#         blank=True
#     )
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.slug = slugify(self.name)
#         super(Product, self).save(*args, **kwargs)
#
#     def get_absolute_url(self):
#         ''' Возвращает абсолютный URL. '''
#         return 'product', {'slug': self.slug}
#
#     def get_content_type(self):
#         return ContentType.objects.get_for_model(self)
