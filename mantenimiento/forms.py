#-*- coding: utf-8 -*-

from datetime import timedelta
from django import forms
from django.db.models import Sum
from common.widgets import CheckboxServicios
from mantenimiento.constants import CUADRO_CHOICES, TEMPLATE_REPORTES
from mantenimiento.models import MantenimientoCorrectivo, \
    MantenimientoPreventivo, PeriodoServicio, TipoServicioPreventivo, \
    TipoServicioCorrectivo
from maquinarias.models import Maquina


class PeriodoServicioForm(forms.ModelForm):
    """
    Formulario para un periodo de servicio
    """
    servicios = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=TipoServicioPreventivo.objects.all()
    )

    class Meta:
        model = PeriodoServicio


class MantenimientoCorrectivoForm(forms.ModelForm):
    """
    Formulario para el mantenimiento correctivo
    """

    class Meta:
        model = MantenimientoCorrectivo

    def __init__(self, *args, **kwargs):
        super(MantenimientoCorrectivoForm, self).__init__(*args, **kwargs)
        self.fields["servicios"].widget = CheckboxServicios(
            servicios=TipoServicioCorrectivo.by_sistema(TipoServicioCorrectivo.objects.all())
        )
        self.fields["servicios"].queryset = TipoServicioCorrectivo.objects.all()


class MantenimientoPreventivoForm(forms.ModelForm):
    """
    Formulario para el mantenimiento preventivo
    """
    servicios = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=TipoServicioPreventivo.objects.all()
    )
    periodo_servicio = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=PeriodoServicio.objects.all(),
    )

    class Meta:
        model = MantenimientoPreventivo


class ReporteForm(forms.Form):
    """
    Formulario para elegir maquina, fechas y tipo de reporte
    """
    maquina = forms.ModelChoiceField(queryset=Maquina.objects.all(),
                                     label=u"Máquina")
    fecha_inicio = forms.DateField(
        label=u"Fecha de inicio",
        help_text=u"La fecha debe estar en este formato: dd/mm/aaaa")
    fecha_fin = forms.DateField(
        label=u"Fecha de fin",
        help_text=u"La fecha debe estar en este formato: dd/mm/aaaa")
    tipo_cuadro = forms.ChoiceField(widget=forms.RadioSelect,
                                    label=u"Tipo de cuadro",
                                    choices=CUADRO_CHOICES)

    def save(self):
        """
        Devuelve el template según el cuadro seleccionado y los mantenimientos
        según la máquina y las fechas
        """
        maquina = self.cleaned_data["maquina"]
        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_fin = self.cleaned_data["fecha_fin"]
        tipo_cuadro = self.cleaned_data["tipo_cuadro"]
        template = TEMPLATE_REPORTES[tipo_cuadro]
        if tipo_cuadro == "C":
            preventivos = MantenimientoPreventivo.objects.filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin,
                maquina=maquina)
            correctivos = MantenimientoCorrectivo.objects.filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin,
                maquina=maquina)

            dias = (fecha_fin - fecha_inicio).days + 1
            data = []
            for fecha in (fecha_inicio + timedelta(n) for n in range(dias)):
                try:
                    obj = preventivos.get(fecha=fecha)
                    preventivo = obj.costo
                    preventivo_obs = obj.observaciones
                except MantenimientoPreventivo.DoesNotExist:
                    preventivo = 0
                    preventivo_obs = u""
                try:
                    obj = correctivos.get(fecha=fecha)
                    correctivo = obj.costo
                    correctivo_obs = obj.observaciones
                except MantenimientoCorrectivo.DoesNotExist:
                    correctivo = 0
                    correctivo_obs = u""
                data.append(
                    {"fecha": fecha,
                     "preventivo": preventivo,
                     "preventivo_obs": preventivo_obs,
                     "correctivo": correctivo,
                     "correctivo_obs": correctivo_obs,
                     "costo_total": preventivo + correctivo}
                )

            return (template,
                    {"fechas": data,
                     "sum_preventivo": sum(item["preventivo"] for item in data),
                     "sum_correctivo": sum(item["correctivo"] for item in data),
                     "sum_total": sum(item["costo_total"] for item in data),
                     "maquina": maquina,
                     "fecha_inicio": fecha_inicio,
                     "fecha_fin": fecha_fin})

        if tipo_cuadro == "B":
            preventivos = MantenimientoPreventivo.objects.filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin,
                maquina=maquina).aggregate(Sum('costo'))["costo__sum"]
            correctivos = MantenimientoCorrectivo.objects.filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin,
                maquina=maquina).aggregate(Sum('costo'))["costo__sum"]

            return (template,
                    {"sum_total": preventivos + correctivos,
                     "maquina": maquina,
                     "fecha_inicio": fecha_inicio,
                     "fecha_fin": fecha_fin})