# Generated by Django 2.1.4 on 2018-12-25 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0008_auto_20181225_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('sort_ordering', models.SmallIntegerField(verbose_name='порядок сортировки')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='название')),
                ('youtube_url', models.URLField(verbose_name='адрес ролика на YouTube')),
                ('youtube_id', models.CharField(editable=False, max_length=40)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demobaza.Project')),
            ],
            options={
                'verbose_name': 'трек',
                'verbose_name_plural': 'треки',
                'ordering': ('sort_ordering',),
            },
        ),
    ]
