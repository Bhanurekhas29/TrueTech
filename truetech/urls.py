import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]

# django.conf.urls.static.static() is a no-op unless DEBUG=True, so media is
# served explicitly here to work in production too (no CDN/object storage yet).
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
