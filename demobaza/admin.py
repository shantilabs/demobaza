from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from . import models

admin.site.site_header = 'Демобаза'


class TrackAdmin(admin.TabularInline):
    max_num = settings.DEMOBAZA_MAX_TRACKS
    model = models.Track


class MovieAdmin(admin.TabularInline):
    max_num = settings.DEMOBAZA_MAX_MOVIES
    model = models.Movie


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'genres',
    )
    inlines = (
        TrackAdmin,
        MovieAdmin,
    )


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    pass
