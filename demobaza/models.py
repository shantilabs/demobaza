import os.path
from urllib.parse import urlparse, parse_qs

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from pytils.translit import slugify  # slugify() из джанги не знает кириллицы

from .validators import validate_mp3ext


class User(AbstractUser):
    """
    Пользователь системы. Может быть:
    - админом
    - представителем фестиваля (Event)
    - представителем музыканта (Project)

    А так же в любом случае любой пользователь может быть слушателем, который
    просто ходит по сайту и слушает музыку.
    """
    projects = models.ManyToManyField(
        'demobaza.Project',
        through='demobaza.Musician',
        related_name='users',
        verbose_name='проекты',
        blank=True,
    )
    events = models.ManyToManyField(
        'demobaza.Event',
        through='demobaza.Organizer',
        related_name='users',
        verbose_name='события',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Project(models.Model):
    """
    Проект (имеющий название, информацию, треки)

    Один пользователь может управлять несколькими музыкальными проектами
    (например, играет с группой, играет сольно, продюссирует ещё кого-то).

    Плюс одним проектом могут управлять несколько пользователей
    (например, все участники группы).

    Создать новый проект может любой пользователь.

    Если надо доверить управление проектом ещё кому-то, это должен явно
    сделать тот, у кого уже есть доступ.

    Все управляющие проектом равны. Если солист Вася доверил басисту Пете
    управлять страницей группы «Бетонные сырники», а басист Петя отключил
    солисту Васе управление (вот сволочь), то это их личные проблемы, пусть
    договариваются между собой сами.

    Если проектом управляет только один человек, он не может отказаться
    от управления.
    """
    created = models.DateTimeField('создан', auto_now_add=True)
    name = models.CharField('название', max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    short_text = models.TextField('короткий текст', blank=True)
    long_text = models.TextField('длинный текст', blank=True)
    city = models.ForeignKey(
        'demobaza.City',
        null=True,
        blank=True,
        verbose_name='город',
        on_delete=models.PROTECT,
        related_name='projects',
    )
    genres = models.ManyToManyField(
        'demobaza.Genre',
        blank=True,
        verbose_name='жанры',
        related_name='projects',
    )
    # Архивных не показываем в списках, но показываем по прямой ссылке.
    # должна быть плашка «архив». Треки у архивных не отображаются, только текст
    is_active = models.BooleanField('активен', default=True)
    # Если не проверен, отображаем так же точно. А если проверен, можно
    # писать «проверен»
    verified = models.BooleanField('проверен администрацией', default=False)
    verified_at = models.DateTimeField(editable=False, null=True)

    class Meta:
        verbose_name = 'проект (группа, исполнитель)'
        verbose_name_plural = 'проекты (группы, исполнители)'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        if self.verified and not self.verified_at:
            self.verified_at = now()
        elif not self.verified and self.verified_at:
            self.verified_at = None
        super().save(*args, **kwargs)


class Track(models.Model):
    """
    У каждого проекта не более settings.DEMOBAZA_MAX_TRACKS треков.
    """
    created = models.DateTimeField('создан', auto_now_add=True)
    sort_ordering = models.SmallIntegerField('порядок сортировки', default=1)
    project = models.ForeignKey(
        'demobaza.Project',
        on_delete=models.PROTECT,
        editable=False,
    )
    title = models.CharField(
        'название',
        max_length=100,
        unique=True,
        blank=True,
    )
    duration_sec = models.PositiveIntegerField(
        'длина, сек.',
        editable=False,
        default=0,
    )
    file = models.FileField(
        '.mp3',
        upload_to='tracks',
        validators=[validate_mp3ext],
    )

    class Meta:
        verbose_name = 'трек'
        verbose_name_plural = 'треки'
        ordering = (
            'sort_ordering',
            'title',
        )

    def __str__(self):
        return '{} - {}'.format(
            self.title,
            self.project.name,
        )

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        if not self.title:
            self.title = os.path.split(self.file.name)[-1]
        # FIXME: при загрузке файла заполнять поле duration_sec и название трека
        # название можно редактировать (допустим, в mp3 название не указано
        # или указано криво), а время редактировать нельзя
        super().save(*args, **kwargs)


class Movie(models.Model):
    """
    У каждого проекта не более settings.DEMOBAZA_MAX_MOVIES видео
    """
    created = models.DateTimeField('создан', auto_now_add=True)
    sort_ordering = models.SmallIntegerField('порядок сортировки')
    project = models.ForeignKey('demobaza.Project', on_delete=models.PROTECT)
    title = models.CharField('название', max_length=100, unique=True)
    youtube_url = models.URLField('адрес ролика на YouTube')
    youtube_id = models.CharField(max_length=40, editable=False)

    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
        ordering = (
            'sort_ordering',
            'title',
        )

    def __str__(self):
        return '{} - {}'.format(
            self.title,
            self.project.name,
        )

    def clean(self):
        try:
            o = urlparse(self.youtube_url)
        except ValueError as e:
            raise ValidationError('Некорректный адрес ролика')

        if o.netloc not in (
            'www.youtube.com',
            'm.youtube.com',
            'youtube.com',
        ):
            raise ValidationError('Некорректный адрес ролика')

        params = parse_qs(o.query)
        if 'v' not in params:
            raise ValidationError('Некорректный адрес ролика')

        self.youtube_id = params['v'][0]

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        self.clean()
        super().save(*args, **kwargs)


class Genre(models.Model):
    """
    Каждый управляющий проектом может создать новый жанр. Но лучше, конечно,
    использовать готовые.
    """
    created = models.DateTimeField('создан', auto_now_add=True)
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


class City(models.Model):
    """
    Пока не импортируем никакую общую базу, будем создавать базу городов
    по ходу дела, по потребонсти
    """
    created = models.DateTimeField('создан', auto_now_add=True)
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


class Event(models.Model):
    """
    События. Логика управления такая же, как и у проектов (Project), см. выше
    """
    name = models.CharField('название', max_length=50, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    short_text = models.TextField('короткий текст', blank=True)
    long_text = models.TextField('длинный текст', blank=True)
    city = models.ForeignKey(
        'demobaza.City',
        null=True,
        verbose_name='город',
        on_delete=models.PROTECT,
        related_name='events',
    )

    class Meta:
        verbose_name = 'событие (фестиваль, концерт, квартирник)'
        verbose_name_plural = 'события (фестивали, концерты, квартирники)'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# задаём явные модели для связей

class Organizer(models.Model):
    created = models.DateTimeField('добавлен', auto_now_add=True)
    user = models.ForeignKey('demobaza.User', on_delete=models.PROTECT)
    event = models.ForeignKey(
        'demobaza.Event',
        on_delete=models.PROTECT,
        verbose_name='событие',
    )

    class Meta:
        verbose_name = 'организатор'
        verbose_name_plural = 'организаторы'
        unique_together = (
            ('user', 'event'),
        )


class Musician(models.Model):
    created = models.DateTimeField('добавлен', auto_now_add=True)
    user = models.ForeignKey('demobaza.User', on_delete=models.PROTECT)
    project = models.ForeignKey(
        'demobaza.Project',
        on_delete=models.PROTECT,
        verbose_name='проект',
    )

    class Meta:
        verbose_name = 'музыкант'
        verbose_name_plural = 'музыканты'
        unique_together = (
            ('user', 'project'),
        )
