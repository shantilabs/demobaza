# Generated by Django 2.1.4 on 2018-12-25 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0009_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='verified_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='проверен администрацией'),
        ),
    ]