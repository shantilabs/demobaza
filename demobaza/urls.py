from django.conf import settings
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import os
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    web_root = os.path.join(settings.BASE_DIR, 'web')
    urlpatterns += static('favicon.ico', document_root=web_root)
    urlpatterns += static('robots.txt', document_root=web_root)
    urlpatterns += static('humans.txt', document_root=web_root)
    urlpatterns += static(settings.STATIC_URL)
