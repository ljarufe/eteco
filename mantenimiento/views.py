# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from common.utils import json_response, direct_response
from mantenimiento.forms import ReporteForm
from mantenimiento.models import PeriodoServicio
from maquinarias.models import Maquina


@login_required
def alerta_preventiva(request):
    """
    Muestra el cuadro de máquinas vs periodos preventivos
    """
    return direct_response(request, "mantenimiento/alerta_preventiva.html",
                           {"periodos": PeriodoServicio.objects.all(),
                            "maquinas": Maquina.objects.all()})


@login_required
def reportes(request):
    """
    Cuadro de diálogo para generar reportes
    """
    if request.method == "POST":
        form = ReporteForm(request.POST)
        if form.is_valid():
            template, data = form.save()
            return direct_response(request, template, data)
    else:
        form = ReporteForm()

    return direct_response(request, "mantenimiento/reportes.html",
                           {'form': form})


@login_required
def json_get_periodo(request):
    """
    Devuelve una lista con los ids de los servicios relacionados a un proyecto,
    se toman los servicios de los periodos múltiplos también
    """
    if request.method == "GET":
        if "id_periodo" in request.GET:
            horas = get_object_or_404(PeriodoServicio,
                                      id=request.GET["id_periodo"]).horas
            periodos_obj = PeriodoServicio.objects.all()
            servicios = []
            periodos = []
            for periodo in periodos_obj:
                if horas % periodo.horas == 0:
                    servicios.extend(
                        [servicio.id for servicio in periodo.servicios.all()])
                    periodos.append(periodo.id)

            return json_response({"servicios": servicios, "periodos": periodos})
        else:
            return json_response({})
    else:
        return json_response({})