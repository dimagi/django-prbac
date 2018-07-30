
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
