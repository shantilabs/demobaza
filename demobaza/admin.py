from django.contrib import admin
from . import models


admin.site.site_header = 'Демобаза'


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'genres',
    )
