from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from product.models import BaseModel


class User(AbstractUser):
    ''' Абстрактный пользователь '''

    class Meta:
        ordering = ['username']
        verbose_name = _('Пользователи')
        verbose_name_plural = verbose_name

    email = models.EmailField(
        _('Email address'), 
        unique=True
    )
    email_verify = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class City(BaseModel):
    ''' Город '''

    class Meta:
        ordering = ['name']
        verbose_name = _('Города')
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Profile(BaseModel):
    ''' Профиль '''

    class Meta:
        verbose_name = _('Профили')
        verbose_name_plural = verbose_name
    
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _('Мужчина')),
        (GENDER_FEMALE, _('Женщина'))
    ]

    user = models.OneToOneField(
        User, 
        related_name="profile", 
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="profiles/avatars/", 
        null=True, 
        blank=True
    )
    birthday = models.DateField(
        null=True, 
        blank=True
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, 
        null=True, 
        blank=True
    )
    phone = PhoneNumberField(
        null=True, 
        blank=True, 
        unique=True
    )
    city = models.ForeignKey(
        City, 
        related_name='city_id', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return ""

    def __str__(self):
        return self.user.username

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #
    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image
