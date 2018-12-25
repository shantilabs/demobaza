from urllib.parse import urlparse, parse_qs

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
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
    projects = models.ManyToManyField(
        'demobaza.Project',
        through='demobaza.Musician',
        related_name='users',
        verbose_name='музыканты',
        blank=True,
    )

    # для фестивалей та же логика, что и для проектов: пользователь может
    # быть организатором любого количества событий, от нуля.
    events = models.ManyToManyField(
        'demobaza.Event',
        through='demobaza.Organizer',
        related_name='users',
        verbose_name='музыканты',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Project(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    # Архивных не показываем в списках, но показываем по прямой ссылке.
    # должна быть плашка «архив». Треки у архивных не отображаются, только текст
    archive = models.BooleanField('архив', default=False)
    # Если не проверен, отображаем так же точно. А если проверен, можно
    # писать «проверен»
    verified = models.BooleanField('проверен администрацией', default=False)
    verified_at = models.DateTimeField(editable=False, null=True)
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
        if self.verified and not self.verified_at:
            self.verified_at = now()
        elif not self.verified and self.verified_at:
            self.verified_at = None
        super().save(*args, **kwargs)


# не более settings.DEMOBAZA_MAX_TRACKS треков на проект
class Track(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    sort_ordering = models.SmallIntegerField('порядок сортировки')
    project = models.ForeignKey('demobaza.Project', on_delete=models.PROTECT)
    title = models.CharField('название', max_length=100, unique=True)
    duration_sec = models.PositiveIntegerField('длина, сек.', editable=False)
    file = models.FileField('.mp3', upload_to='tracks')

    class Meta:
        verbose_name = 'трек'
        verbose_name_plural = 'треки'
        ordering = (
            'sort_ordering',
        )

    def __str__(self):
        return '{} - {}'.format(
            self.title,
            self.project.name,
        )

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        # FIXME: при загрузке файла заполнять поле duration_sec и название трека
        # название можно редактировать (допустим, в mp3 название не указано
        # или указано криво), а время редактировать нельзя
        super().save(*args, **kwargs)


# не более settings.DEMOBAZA_MAX_MOVIES треков на проект
class Movie(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    sort_ordering = models.SmallIntegerField('порядок сортировки')
    project = models.ForeignKey('demobaza.Project', on_delete=models.PROTECT)
    title = models.CharField('название', max_length=100, unique=True)
    youtube_url = models.URLField('адрес ролика на YouTube')
    youtube_id = models.CharField(max_length=40, editable=False)

    class Meta:
        verbose_name = 'трек'
        verbose_name_plural = 'треки'
        ordering = (
            'sort_ordering',
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


# пока не импортируем никакую общую базу, будем создавать базу городов
# по ходу дела, по потребонсти. Возможно, городов вообще много не будет.
class City(models.Model):
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
        verbose_name = 'событие'
        verbose_name_plural = 'события'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# явные задаём модели для связей

class Organizer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('demobaza.User', on_delete=models.PROTECT)
    event = models.ForeignKey('demobaza.Event', on_delete=models.PROTECT)


class Musician(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('demobaza.User', on_delete=models.PROTECT)
    project = models.ForeignKey('demobaza.Project', on_delete=models.PROTECT)
