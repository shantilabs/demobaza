# Generated by Django 2.1.4 on 2018-12-25 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0003_auto_20181225_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'город',
                'verbose_name_plural': 'города',
                'ordering': ('name',),
            },
        ),
    ]
