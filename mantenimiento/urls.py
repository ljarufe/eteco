# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('mantenimiento.views',
    url(r'^json_get_periodo/$',
        'json_get_periodo',
        name='json_get_periodo'),
    url(r'^alerta_preventiva/$',
        'alerta_preventiva',
        name='alerta_preventiva'),
    url(r'^reportes/$',
        'reportes',
        name='reportes'),
)