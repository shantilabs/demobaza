# Generated by Django 2.1.4 on 2018-12-25 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0006_auto_20181225_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('short_text', models.TextField(blank=True, verbose_name='короткий текст')),
                ('long_text', models.TextField(blank=True, verbose_name='длинный текст')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='demobaza.City', verbose_name='город')),
            ],
            options={
                'verbose_name': 'событие',
                'verbose_name_plural': 'события',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demobaza.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('archive', models.BooleanField(default=False, verbose_name='архив')),
                ('verified', models.DateTimeField(null=True, verbose_name='проверен администрацией')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='название')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('short_text', models.TextField(blank=True, verbose_name='короткий текст')),
                ('long_text', models.TextField(blank=True, verbose_name='длинный текст')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='demobaza.City', verbose_name='город')),
                ('genres', models.ManyToManyField(blank=True, related_name='projects', to='demobaza.Genre', verbose_name='жанры')),
            ],
            options={
                'verbose_name': 'музыкант',
                'verbose_name_plural': 'музыканты',
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='festival',
            name='city',
        ),
        migrations.AlterModelOptions(
            name='musician',
            options={},
        ),
        migrations.RemoveField(
            model_name='musician',
            name='archive',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='city',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='long_text',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='name',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='short_text',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='user',
            name='musicians',
        ),
        migrations.AddField(
            model_name='musician',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='musician',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Festival',
        ),
        migrations.AddField(
            model_name='organizer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='musician',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='demobaza.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='users', through='demobaza.Organizer', to='demobaza.Event', verbose_name='музыканты'),
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='users', through='demobaza.Musician', to='demobaza.Project', verbose_name='музыканты'),
        ),
    ]
