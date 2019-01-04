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
    search_fields = (
        'name',
    )
    list_display = (
        'name',
        'city',
        'verified',
        'is_active',
    )
    list_filter = (
        'verified',
        'is_active',
        'city',
        'genres',
    )
    filter_horizontal = (
        'genres',
    )
    inlines = (
        TrackAdmin,
        MovieAdmin,
    )


class OrganizerAdmin(admin.TabularInline):
    model = models.Organizer
    raw_id_fields = (
        'event',
    )
    readonly_fields = (
        'created',
    )
    extra = 0


class MusicianAdmin(admin.TabularInline):
    model = models.Musician
    raw_id_fields = (
        'project',
    )
    readonly_fields = (
        'created',
    )
    extra = 0


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    inlines = BaseUserAdmin.inlines + [
        OrganizerAdmin,
        MusicianAdmin,
    ]


@admin.register(models.Track)
class TrackFileAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
    )
    list_display = (
        'title',
        'project',
        'duration_sec',

    )
    list_filter = (
        'project',

    )


admin.site.register(models.Genre)
admin.site.register(models.Event)
admin.site.register(models.Movie)
admin.site.register(models.City)
admin.site.register(models.Organizer)
admin.site.register(models.Avatar)
