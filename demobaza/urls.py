import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = []

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.views.static import serve
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += [
        re_path('^(?P<path>[^/]+)$', serve, kwargs={
            'document_root': os.path.join(settings.BASE_DIR, 'web'),
            'show_indexes': True,
        }),
    ]

urlpatterns += [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('musicians/<str:slug>/', views.musician)
    url('', include('social_django.urls', namespace='social'))
]
