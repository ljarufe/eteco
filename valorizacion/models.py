# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver


class Cliente(models.Model):
    """
    Cliente
    """
    nombre = models.CharField(max_length=300)
    numero = models.CharField(max_length=20, verbose_name=u"teléfono",
                              blank=True, null=True)
    procedencia = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name=u"Contacto")

    def __unicode__(self):
        return u"%s" % self.nombre


class Obra(models.Model):
    """
    Obra donde se manda a la maquinaria
    """
    nombre = models.CharField(max_length=300)
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return u"%s" % self.nombre


class ParteDiario(models.Model):
    """
    Parte diario de uso de una máquina
    """
    numero = models.CharField(max_length=10, verbose_name=u"número de parte")
    maquina = models.ForeignKey("maquinarias.Maquina", verbose_name=u"máquina")
    operador = models.ForeignKey("maquinarias.Operador", blank=True, null=True)
    fecha = models.DateField(default=datetime.now)
    obra = models.ForeignKey(Obra)
    detalles = models.TextField(verbose_name=u"Trabajos realizados", blank=True,
                                null=True)
    horometro_inicio = models.FloatField(verbose_name=u"horómetro inicial")
    horometro_final = models.FloatField(verbose_name=u"horómetro final")
    horas_trabajadas = models.FloatField()
    calentamiento = models.FloatField(default=0)

    def __unicode__(self):
        return u"%s: %s (H: %s)" % (self.maquina, self.fecha, self.horometro_final)

    def get_detalles(self):
        """
        Devuelve los detalles con mark_safe
        """
        return self.detalles
    get_detalles.short_description = 'Trabajos realizados'
    get_detalles.allow_tags = True

    class Meta:
        verbose_name_plural = u"Partes diarios"
        get_latest_by = ("horometro_final",)
        ordering = ("horometro_final",)


@receiver(pre_delete, sender=ParteDiario, dispatch_uid="delete_partediario")
def pre_delete_partediario(sender, **kwargs):
    """
    Al borrar el parte diario el horómetro de la máquina implicada se descuenta
    """
    obj = kwargs["instance"]
    obj.maquina.increase(0-obj.horas_trabajadas-obj.calentamiento)


class ValorizacionSimple(models.Model):
    """
    Valorización del alquiler de una maquinaria
    """
    maquina = models.ForeignKey("maquinarias.Maquina", verbose_name=u"máquina")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return u"%s: %s - %s" % (self.maquina, self.fecha_inicio, self.fecha_fin)

    def get_partes(self):
        """
        Devuelve todas las partes para la valorización
        """
        if not self.partes:
            self.partes = ParteDiario.objects.filter(
                fecha__lte=self.fecha_fin,
                fecha__gte=self.fecha_inicio,
                maquina=self.maquina
            ).order_by("fecha", "horometro_inicio")

        return self.partes

    class Meta:
        verbose_name = u"Valorización simple"
        verbose_name_plural = u"Valorizaciones simples"


class Valorizacion(models.Model):
    """
    Conjunto de valorizaciones para distintas máquinas
    """
    valorizaciones = models.ManyToManyField(ValorizacionSimple)
    partes = models.ManyToManyField(ParteDiario, blank=True, null=True)
    costo_hora = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "".join(["%s, " % val for val in self.valorizaciones.all()])

    def get_partes(self):
        """
        Obtiene las partes de cada una de las valorizaciones implicadas
        """
        return self.partes.all().order_by("fecha", "horometro_inicio")

    class Meta:
        verbose_name = u"Valorización"
        verbose_name_plural = u"Valorizaciones"