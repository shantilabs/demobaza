# Generated by Django 2.1.4 on 2018-12-26 12:01

import demobaza.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demobaza', '0012_auto_20181225_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='userpic',
            field=models.FileField(default=False, upload_to='img/userpic', validators=[demobaza.validators.validate_jpgext], verbose_name='.jpg'),
        ),
    ]