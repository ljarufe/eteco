# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# TODO: Poner el favicon de eteco

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^mantenimiento/', include('mantenimiento.urls')),
    url(r'^valorizacion/', include('valorizacion.urls')),
    # Media y static
    (r'^media/(?P<path>.*)$','django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',
         {'document_root': settings.STATIC_ROOT,'show_indexes': True}),
)