import os

from django.core.exceptions import ValidationError


def validate_mp3ext(value):
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Поддерживается только .mp3')


def validate_jpgext(value):
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Поддерживается только .jpg')
