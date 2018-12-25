from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify  # slugify() из джанги не знает кириллицы


class User(AbstractUser):
    # Один пользователь может управлять несколькими музыкальными проектами
    # например, играет с группой, играет сольно. А может это просто зритель,
    # тогда у него ноль проектов.
    #
    # Также одним проектом могут управлять несколько пользователей. Создать
    # новый проект может любой пользователь. Если надо доверить управление
    # проектом ещё кому-то, это должен явно сделать тот, у кого уже есть доступ.
    # Ролей пока не делаем, то есть все управляющие равны. Если солист Вася
    # доверил басисту Пете управлять страницей группы «Бетонные сырники»,
    # а басист Петя отключил солисту Васе управление (вот сволочь), то это
    # их личные проблемы, пусть договариваются между собой сами
    #
    # Если проектом управляет только один человек, он не может отказаться
    # от управления.
    #
    # Если группу
    musicians = models.ManyToManyField(
        'demobaza.Musician',
        related_name='users',
        verbose_name='музыканты',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Musician(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    # Архивных не показываем в списках, но показываем по прямой ссылке.
    # должна быть плашка «архив». Треки у архивных не отображаются, только текст
    archive = models.BooleanField('архив', default=False)
    # Если не проверен, отображаем так же точно. А если проверен, можно
    # писать «проверен»
    verified = models.DateTimeField('проверен администрацией', null=True)
    name = models.CharField('название', max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    short_text = models.TextField('короткий текст', blank=True)
    long_text = models.TextField('длинный текст', blank=True)
    city = models.ForeignKey(
        'demobaza.City',
        null=True,
        verbose_name='город',
        on_delete=models.PROTECT,
        related_name='musicians',
    )
    genres = models.ManyToManyField(
        'demobaza.Genre',
        blank=True,
        verbose_name='жанры',
        related_name='musicians',
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


# пока не импортируем никакую общую базу, будем создавать базу городов
# по ходу дела, по потребонсти. Возможно, городов вообще много не будет.
class City(models.Model):
    name = models.CharField('название', max_length=50, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Festival(models.Model):
    name = models.CharField('название', max_length=50, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    short_text = models.TextField('короткий текст', blank=True)
    long_text = models.TextField('длинный текст', blank=True)
    city = models.ForeignKey(
        'demobaza.City',
        null=True,
        verbose_name='город',
        on_delete=models.PROTECT,
        related_name='festivals',
    )

    class Meta:
        verbose_name = 'фестиваль'
        verbose_name_plural = 'фестивали'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
