# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib import admin
from common.utils import direct_response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from valorizacion.models import *


class ClienteAdmin(admin.ModelAdmin):
    """
    Admin para un cliente
    """
    list_display = ("nombre", "numero", "procedencia")


class ObraAdmin(admin.ModelAdmin):
    """
    Admin para una obra
    """
    list_display = ("nombre", "cliente")


class ParteDiarioAdmin(admin.ModelAdmin):
    """
    Admin para un parte diario
    """
    list_display = ("maquina", "fecha", "numero", "obra", "operador",
                    "horometro_inicio", "horometro_final", "horas_trabajadas",
                    "calentamiento")
    list_filter = ("maquina", "fecha",)
    list_editable = ("calentamiento",)
    exclude = ("calentamiento",)

    def save_model(self, request, obj, form, change):
        """
        Ajusta el horómetro a la máquina según las horas trabajadas
        """
        if change:
            old = ParteDiario.objects.get(id=obj.id)
            anterior = old.horas_trabajadas + old.calentamiento
        else:
            anterior = 0
            try:
                horometro_anterior = ParteDiario.objects.filter(maquina=obj.maquina, fecha__lte=obj.fecha).latest().horometro_final
                calentamiento = obj.horometro_inicio - horometro_anterior
            except ParteDiario.DoesNotExist:
                calentamiento = 0
            if calentamiento > 0:
                obj.calentamiento = calentamiento
            else:
                obj.calentamiento = 0
        super(self.__class__, self).save_model(request, obj, form, change)
        obj.maquina.increase(obj.horas_trabajadas+obj.calentamiento-anterior)


class ValorizacionAdmin(admin.ModelAdmin):
    """
    Admin para la valorización
    """
    fields = ("valorizaciones", "costo_hora")
    filter_horizontal = ("valorizaciones",)

    def save_model(self, request, obj, form, change):
        """
        Saca los partes que están dentro de las fechas de cada valorización
        """
        super(self.__class__, self).save_model(request, obj, form, change)
        obj = Valorizacion.objects.get(id=obj.id)
        if change:
            obj.partes.clear()
        for valorizacion in obj.valorizaciones.all():
            partes = ParteDiario.objects.filter(fecha__gte=valorizacion.fecha_inicio,
                                                fecha__lte=valorizacion.fecha_fin,
                                                maquina=valorizacion.maquina)
            obj.partes.add(*partes)

    def get_urls(self):
        """
        URLs para modificar la lista de partes diarios
        """
        urls = super(self.__class__, self).get_urls()
        my_urls = patterns('',
            url(r'^partes_diarios/(?P<id>\d+)?$',
               self.admin_site.admin_view(self.partes_diarios),
               name='admin_partes_diarios'),
        )

        return my_urls + urls

    @csrf_exempt
    def partes_diarios(self, request, id=None):
        """
        Formulario para quitar partes de una valorización
        """
        obj = get_object_or_404(Valorizacion, id=id)
        messages = []
        if request.method == "POST":
            for i in range(1, obj.partes.all().count() + 1):
                if "parte_%s" % i in request.POST:
                    obj.partes.remove(ParteDiario.objects.get(
                        id=request.POST["parte_%s" % i])
                    )
            messages = [u"Se grabaron sus cambios correctamente"]

        return direct_response(request, 'admin/valorizacion/valorizacion/partes_diarios.html',
                               {"obj": obj,
                                "messages": messages})


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(ParteDiario, ParteDiarioAdmin)
admin.site.register(Valorizacion, ValorizacionAdmin)
admin.site.register(ValorizacionSimple)