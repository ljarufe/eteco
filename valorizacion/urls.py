# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('valorizacion.views',
    url(r'^valorizacion_impresion/(?P<id_valorizacion>\d+)/$',
       'valorizacion_impresion',
       name='valorizacion_impresion'),
#    url(r'^valorizacion_to_pdf/$',
#        'valorizacion_to_pdf',
#        name='valorizacion_to_pdf'),
    url(r'^json_get_horometro/$',
       'json_get_horometro',
       name='json_get_horometro'),
)