# Generated by Django 2.1.4 on 2018-12-26 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0015_auto_20181226_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='userpic',
        ),
    ]