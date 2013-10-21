# -*- coding: utf-8 -*-

from django.contrib import admin
from maquinarias.models import *


class MaquinaAdmin(admin.ModelAdmin):
    """
    Admin para una máquina
    """
    list_display = ("centro_costos", "maquina", "marca", "modelo",
                    "get_ubicacion", "placa", "motor", "horometro",
                    "horas_alerta",)
    list_editable = ("horometro", "horas_alerta",)
    list_filter = ("maquina", "marca",)


admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Marca)
admin.site.register(TipoMaquina)
admin.site.register(Operador)