# -*- coding: utf-8 -*-

from django.contrib import admin
from mantenimiento.forms import MantenimientoCorrectivoForm, \
    MantenimientoPreventivoForm, PeriodoServicioForm
from mantenimiento.models import *
from valorizacion.models import ParteDiario


class TipoServicioCorrectivoAdmin(admin.ModelAdmin):
    """
    Admin para tipo de servicio
    """
    list_display = ("nombre", "sistema", "uso_correctivo",)
    readonly_fields = ["uso_correctivo",]
    list_filter = ("sistema",)


class TipoServicioPreventivoAdmin(admin.ModelAdmin):
    """
    Admin para tipo de servicio
    """
    list_display = ("nombre",)


class PeriodoServicioAdmin(admin.ModelAdmin):
    """
    Admin para un peridodo de servicio
    """
    form = PeriodoServicioForm
    list_display = ("horas", "get_servicios")


class MantenimientoCorrectivoAdmin(admin.ModelAdmin):
    """
    Admin para un mantenimiento correctivo
    """
    form = MantenimientoCorrectivoForm
    list_filter = ('maquina', 'fecha')
    list_display = ("maquina", "fecha", "mecanico", "supervisor", "costo",
                    "horometro", "get_detalles")

    def save_model(self, request, obj, form, change):
        """
        Se guarda el horómetro en el que se realizó el mantenimiento
        """
        if not change:
            for servicio in form.cleaned_data["servicios"]:
                servicio.add_use()
        super(self.__class__, self).save_model(request, obj, form, change)


class MantenimientoPreventivoAdmin(admin.ModelAdmin):
    """
    Admin para un mantenimiento preventivo
    """
    form = MantenimientoPreventivoForm
    list_filter = ('maquina', 'fecha')
    list_display = ("maquina", "fecha", "get_periodos", "mecanico", "horometro",
                    "observaciones")
    list_editable = ("horometro",)
    exclude = ("horometro",)

    def save_model(self, request, obj, form, change):
        """
        Se guarda el horómetro en el que se realizó el mantenimiento
        """
        if not change:
            try:
                parte = ParteDiario.objects.filter(maquina=obj.maquina, fecha=obj.fecha).latest()
                obj.horometro = parte.horometro_final
            except ParteDiario.DoesNotExist:
                obj.horometro = obj.maquina.horometro
        super(self.__class__, self).save_model(request, obj, form, change)


admin.site.register(SistemaServicio)
admin.site.register(TipoServicioCorrectivo, TipoServicioCorrectivoAdmin)
admin.site.register(TipoServicioPreventivo, TipoServicioPreventivoAdmin)
admin.site.register(PeriodoServicio, PeriodoServicioAdmin)
admin.site.register(Mecanico)
admin.site.register(Supervisor)
admin.site.register(MantenimientoCorrectivo, MantenimientoCorrectivoAdmin)
admin.site.register(MantenimientoPreventivo, MantenimientoPreventivoAdmin)