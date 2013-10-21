# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from maquinarias.models import Maquina


class SistemaServicio(models.Model):
    """
    Sistema al que pertenece un servicio correctivo
    """
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = u"Sistema de servicio"
        verbose_name_plural = u"Sistemas de servicio"


class TipoServicioCorrectivo(models.Model):
    """
    Tipo de servicio para mantenimientos correctivos
    """
    nombre = models.CharField(max_length=200)
    sistema = models.ForeignKey(SistemaServicio)
    uso_correctivo = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s (%s)" % (self.nombre, self.sistema)

    def add_use(self):
        """
        Aumenta en 1 el uso por un mantenimiento
        """
        self.uso_correctivo += 1
        self.save()

    @staticmethod
    def by_sistema(servicios):
        """
        Devuelve un dicccionario ordenado por sistema
        """
        list = []
        for sistema in SistemaServicio.objects.all():
            list.append({"sistema": sistema.nombre,
                         "servicios": servicios.filter(sistema=sistema)})

        return list

    class Meta:
        verbose_name = u"Tipo de servicio correctivo"
        verbose_name_plural = u"Tipos de servicio correctivo"
        ordering = ("sistema", "id",)


class TipoServicioPreventivo(models.Model):
    """
    Tipo de servicio para mantenimientos correctivos
    """
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = u"Tipo de servicio preventivo"
        verbose_name_plural = u"Tipos de servicio preventivo"


class PeriodoServicio(models.Model):
    """
    Periodo de servicio, cada cuántas horas se realiza un conjunto de servicios
    """
    horas = models.IntegerField()
    servicios = models.ManyToManyField(TipoServicioPreventivo)

    def __unicode__(self):
        return u"%s" % self.horas

    def get_servicios(self):
        """
        Devuelve los detalles con mark_safe
        """
        return "<ul>%s</ul>" % u"".join([u"<li>%s</li>" % servicio for servicio in self.servicios.all()])
    get_servicios.short_description = u'Servicios'
    get_servicios.allow_tags = True

    class Meta:
        verbose_name = u"Periodo de servicio preventivo"
        verbose_name_plural = u"Periodos de servicio preventivo"


class Mecanico(models.Model):
    """
    Mecánico encargado de un mantenimiento
    """
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = u"Mecánico"
        verbose_name_plural = u"Mecánicos"


class Supervisor(models.Model):
    """
    Mecánico encargado de un mantenimiento
    """
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = u"Supervisor encargado"
        verbose_name_plural = u"Supervisores encargados"


class MantenimientoCorrectivo(models.Model):
    """
    Mantenimiento correctivo
    """
    maquina = models.ForeignKey(Maquina)
    servicios = models.ManyToManyField(TipoServicioCorrectivo)
    mecanico = models.ForeignKey(Mecanico, verbose_name=u"mecánico", blank=True,
                                 null=True)
    supervisor = models.ForeignKey(Supervisor,
                                   verbose_name=u"supervisor encargado",
                                   blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateField(default=datetime.now)
    costo = models.FloatField(null=True, blank=True, default=0)
    horometro = models.FloatField(null=True, blank=True,
                                  verbose_name=u"horómetro")

    def __unicode__(self):
        return u"%s: %s" % (self.maquina, self.fecha)

    def get_detalles(self):
        """
        Devuelve los detalles con mark_safe
        """
        return self.observaciones
    get_detalles.short_description = 'Observaciones'
    get_detalles.allow_tags = True

    class Meta:
        verbose_name_plural = u"Mantenimientos correctivos"


class MantenimientoPreventivo(models.Model):
    """
    Mantenimiento preventivo, el horómetro se guarda para compararlo contra los
    otros mantenimientos preventivos y mandar las alertas.
    """
    maquina = models.ForeignKey(Maquina)
    periodo_servicio = models.ManyToManyField(PeriodoServicio)
    servicios = models.ManyToManyField(TipoServicioPreventivo)
    mecanico = models.ForeignKey(Mecanico, verbose_name=u"mecánico", blank=True,
                                 null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateField(default=datetime.now)
    horometro = models.FloatField()
    costo = models.FloatField(null=True, blank=True, default=0)

    def __unicode__(self):
        return u"%s: %s" % (self.maquina, self.fecha)

    def get_periodos(self):
        """
        Devuelve una lista de los periodos de mantenimiento que se cubrieron
        """
        return "<ul>%s</ul>" % u"".join([u"<li>%s</li>" % periodo for periodo in self.periodo_servicio.all()])
    get_periodos.short_description = u'Periodos'
    get_periodos.allow_tags = True

    def get_absolute_url(self):
        """
        Devuelve la url al formulario del admin
        """
        return "/mantenimiento/mantenimientopreventivo/%s/" % self.id

    class Meta:
        verbose_name_plural = u"Mantenimientos preventivos"
        get_latest_by = "fecha"