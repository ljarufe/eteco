# -*- coding: utf-8 -*-
import os

from django.shortcuts import get_object_or_404
from common.utils import json_response, direct_response
from maquinarias.models import Maquina
from valorizacion.models import ParteDiario, Valorizacion


def valorizacion_impresion(request, id_valorizacion):
    """
    Muestra una página para imprimir una valorización
    """
    obj = get_object_or_404(Valorizacion, id=id_valorizacion)
#    operadores = [parte.operador for parte in obj.partes.all().distinct("operador")]

    return direct_response(request,
                           'valorizacion/valorizacion.html',
                           {"obj": obj})


#@csrf_exempt
#def valorizacion_to_pdf(request):
#    """
#    Convierte la valorización en un pdf
#    """
#    result = open("valorizacion.pdf", 'wb')
#    if "html" in request.POST:
#        html = request.POST["html"]
#    else:
#        html = u""
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result)
#    result.close()
#
#    if not pdf.err:
#        return HttpResponse("PDF generado con éxito")
#    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def json_get_horometro(request):
    """
    Devuelve el último registro del horómetro final de un parte diario de una
    máquina, si no existiera parte diario el horómetro de la máquina en el
    sistema
    """
    if "id_maquina" in request.GET:
        id_maquina = request.GET["id_maquina"]
        if id_maquina:
            try:
                horometro = ParteDiario.objects.filter(maquina__id=id_maquina).order_by("-horometro_final")[:1][0].horometro_final
            except IndexError:
                horometro = get_object_or_404(Maquina, id=id_maquina).horometro

            return json_response({"horometro": horometro})

        else:
            return json_response({})
    else:
        return json_response({})
