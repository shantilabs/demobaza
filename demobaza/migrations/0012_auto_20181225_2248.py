# Generated by Django 2.1.4 on 2018-12-25 22:48

import demobaza.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0011_auto_20181225_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('name',), 'verbose_name': 'событие (фестиваль, концерт, квартирник)', 'verbose_name_plural': 'события (фестивали, концерты, квартирники)'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('sort_ordering', 'title'), 'verbose_name': 'видео', 'verbose_name_plural': 'видео'},
        ),
        migrations.AlterModelOptions(
            name='musician',
            options={'verbose_name': 'музыкант', 'verbose_name_plural': 'музыканты'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': 'организатор', 'verbose_name_plural': 'организаторы'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('name',), 'verbose_name': 'проект (группа, исполнитель)', 'verbose_name_plural': 'проекты (группы, исполнители)'},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ('sort_ordering', 'title'), 'verbose_name': 'трек', 'verbose_name_plural': 'треки'},
        ),
        migrations.RemoveField(
            model_name='project',
            name='archive',
        ),
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активен'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='добавлен'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demobaza.Project', verbose_name='проект'),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='добавлен'),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demobaza.Event', verbose_name='событие'),
        ),
        migrations.AlterField(
            model_name='track',
            name='duration_sec',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='длина, сек.'),
        ),
        migrations.AlterField(
            model_name='track',
            name='file',
            field=models.FileField(upload_to='tracks', validators=[demobaza.validators.validate_mp3ext], verbose_name='.mp3'),
        ),
        migrations.AlterField(
            model_name='track',
            name='project',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='demobaza.Project'),
        ),
        migrations.AlterField(
            model_name='track',
            name='sort_ordering',
            field=models.SmallIntegerField(default=1, verbose_name='порядок сортировки'),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='user',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='users', through='demobaza.Organizer', to='demobaza.Event', verbose_name='события'),
        ),
        migrations.AlterField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='users', through='demobaza.Musician', to='demobaza.Project', verbose_name='проекты'),
        ),
        migrations.AlterUniqueTogether(
            name='musician',
            unique_together={('user', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='organizer',
            unique_together={('user', 'event')},
        ),
    ]