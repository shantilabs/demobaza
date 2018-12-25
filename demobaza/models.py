from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify  # slugify() из джанги не знает кириллицы


class User(AbstractUser):
    musicians = models.ManyToManyField(
        'demobaza.Musician',
        related_name='users',
        verbose_name='музыканты',
        blank=True,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Musician(models.Model):
    enabled = models.BooleanField('включён', default=True)
    verified = models.DateTimeField('проверен администрацией', null=True)
    created = models.DateTimeField('создан', auto_now_add=True)
    name = models.CharField('название', max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    short_text = models.TextField('короткий текст', blank=True)
    long_text = models.TextField('длинный текст', blank=True)
    genres = models.ManyToManyField(
        'demobaza.Genre',
        blank=True,
        verbose_name='жанры',
    )

    class Meta:
        verbose_name = 'музыкант'
        verbose_name_plural = 'музыканты'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField('название', max_length=20, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
