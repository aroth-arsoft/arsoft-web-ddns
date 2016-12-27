from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from arsoft.web.utils import django_debug_urls

from . import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^whoami$', views.whoami, name='whoami'),
    url(r'^update$', views.update, name='update'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the admin:
    url(r'^debug/', include(django_debug_urls())),
]
