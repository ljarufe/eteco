# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from valorizacion.models import ParteDiario


class Marca(models.Model):
    """
    Marca de una maquinaria
    """
    nombre = models.CharField(max_length=250, verbose_name=u"nombre")

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        ordering = ("nombre",)


class TipoMaquina(models.Model):
    """
    Tipo de máquina
    """
    nombre = models.CharField(max_length=250, verbose_name=u"nombre")

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = u"Tipo de máquina"
        verbose_name_plural = u"Tipos de máquina"
        ordering = ("nombre",)


class Maquina(models.Model):
    """
    Máquina
    """
    centro_costos = models.IntegerField(verbose_name=u"centro de costos",
                                        unique=True)
    maquina = models.ForeignKey(TipoMaquina, verbose_name=u"tipo de máquina")
    marca = models.ForeignKey(Marca)
    modelo = models.CharField(max_length=250, blank=True, null=True)
    serie = models.CharField(max_length=250, verbose_name=u"número de serie",
                             null=True, blank=True)
    anio = models.CharField(max_length=4, null=True, blank=True,
                            verbose_name=u"año")
    placa = models.CharField(max_length=10, null=True, blank=True)
    motor = models.CharField(max_length=100, null=True, blank=True)
    horometro = models.FloatField(default=0)
    horas_alerta = models.IntegerField(default=50,
                                       verbose_name=u"Horas de alerta",
        help_text=u"La alerta se encenderá con estas horas de anticipación")
    ubicacion = models.CharField(max_length=100, verbose_name=u"ubicación",
                                 null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.centro_costos

    def get_ubicacion(self):
        """
        Calcula la ubicación en base a los partes diarios si estuviera en una
        obra,
        """
        if self.ubicacion:
            return u"%s" % self.ubicacion
        else:
            try:
                return ParteDiario.objects.filter(
                    maquina=self, fecha=datetime.now()
                ).latest().obra
            except ParteDiario.DoesNotExist:
                return u"Taller"
    get_ubicacion.short_description = 'Ubicación'

    def get_estado(self):
        """
        Devuelve el estado en el que está la máquina
        - Verde: Se ha realizado el mantenimiento
        - Amarillo: El mantenimiento está a "horas alerta" cerca
        - Rojo: No se realizó el mantenimiento en el tiempo adecuado
        """
        from mantenimiento.models import PeriodoServicio, MantenimientoPreventivo
        periodos = PeriodoServicio.objects.all()
        for periodo in periodos:
            try:
                mantenimiento = MantenimientoPreventivo.objects.filter(maquina=self, periodo_servicio=periodo).latest()
#                if round((self.horometro + self.horas_alerta)/periodo.horas - mantenimiento.horometro/periodo.horas) < 2: Mantenimientos perfectos
                if self.horometro < mantenimiento.horometro + periodo.horas - self.horas_alerta:
                    periodo.estado = u"verde"
                elif self.horometro < mantenimiento.horometro + periodo.horas:
                    periodo.estado = u"amarillo"
                else:
                    periodo.estado = u"rojo"
                periodo.mantenimiento = mantenimiento
            except MantenimientoPreventivo.DoesNotExist:
                if self.horometro + self.horas_alerta < periodo.horas:
                    periodo.estado = u"verde"
                elif periodo.horas - self.horometro % periodo.horas <= self.horas_alerta:
                    periodo.estado = u"amarillo"
                else:
                    periodo.estado = u"rojo"

        return periodos

    def increase(self, add):
        """
        Incrementa el horómetro
        """
        self.horometro += add
        self.save()

    class Meta:
        verbose_name = u"Máquina"
        verbose_name_plural = u"Máquinas"
        ordering = ["centro_costos"]


class Operador(models.Model):
    """
    Operador
    """
    nombres = models.CharField(max_length=200, verbose_name=u"nombre")

    def __unicode__(self):
        return u"%s" % self.nombres

    class Meta:
        verbose_name_plural = u"Operadores"