# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SistemaServicio'
        db.create_table('mantenimiento_sistemaservicio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('mantenimiento', ['SistemaServicio'])

        # Adding model 'TipoServicioCorrectivo'
        db.create_table('mantenimiento_tiposerviciocorrectivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sistema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mantenimiento.SistemaServicio'])),
            ('uso_correctivo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('mantenimiento', ['TipoServicioCorrectivo'])

        # Adding model 'TipoServicioPreventivo'
        db.create_table('mantenimiento_tiposerviciopreventivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('mantenimiento', ['TipoServicioPreventivo'])

        # Adding model 'PeriodoServicio'
        db.create_table('mantenimiento_periodoservicio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('horas', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('mantenimiento', ['PeriodoServicio'])

        # Adding M2M table for field servicios on 'PeriodoServicio'
        db.create_table('mantenimiento_periodoservicio_servicios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('periodoservicio', models.ForeignKey(orm['mantenimiento.periodoservicio'], null=False)),
            ('tiposerviciopreventivo', models.ForeignKey(orm['mantenimiento.tiposerviciopreventivo'], null=False))
        ))
        db.create_unique('mantenimiento_periodoservicio_servicios', ['periodoservicio_id', 'tiposerviciopreventivo_id'])

        # Adding model 'Mecanico'
        db.create_table('mantenimiento_mecanico', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('mantenimiento', ['Mecanico'])

        # Adding model 'Supervisor'
        db.create_table('mantenimiento_supervisor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('mantenimiento', ['Supervisor'])

        # Adding model 'MantenimientoCorrectivo'
        db.create_table('mantenimiento_mantenimientocorrectivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('maquina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Maquina'])),
            ('mecanico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mantenimiento.Mecanico'], null=True, blank=True)),
            ('supervisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mantenimiento.Supervisor'], null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('costo', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('horometro', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('mantenimiento', ['MantenimientoCorrectivo'])

        # Adding M2M table for field servicios on 'MantenimientoCorrectivo'
        db.create_table('mantenimiento_mantenimientocorrectivo_servicios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mantenimientocorrectivo', models.ForeignKey(orm['mantenimiento.mantenimientocorrectivo'], null=False)),
            ('tiposerviciocorrectivo', models.ForeignKey(orm['mantenimiento.tiposerviciocorrectivo'], null=False))
        ))
        db.create_unique('mantenimiento_mantenimientocorrectivo_servicios', ['mantenimientocorrectivo_id', 'tiposerviciocorrectivo_id'])

        # Adding model 'MantenimientoPreventivo'
        db.create_table('mantenimiento_mantenimientopreventivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('maquina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Maquina'])),
            ('mecanico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mantenimiento.Mecanico'], null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('horometro', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('mantenimiento', ['MantenimientoPreventivo'])

        # Adding M2M table for field periodo_servicio on 'MantenimientoPreventivo'
        db.create_table('mantenimiento_mantenimientopreventivo_periodo_servicio', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mantenimientopreventivo', models.ForeignKey(orm['mantenimiento.mantenimientopreventivo'], null=False)),
            ('periodoservicio', models.ForeignKey(orm['mantenimiento.periodoservicio'], null=False))
        ))
        db.create_unique('mantenimiento_mantenimientopreventivo_periodo_servicio', ['mantenimientopreventivo_id', 'periodoservicio_id'])

        # Adding M2M table for field servicios on 'MantenimientoPreventivo'
        db.create_table('mantenimiento_mantenimientopreventivo_servicios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mantenimientopreventivo', models.ForeignKey(orm['mantenimiento.mantenimientopreventivo'], null=False)),
            ('tiposerviciopreventivo', models.ForeignKey(orm['mantenimiento.tiposerviciopreventivo'], null=False))
        ))
        db.create_unique('mantenimiento_mantenimientopreventivo_servicios', ['mantenimientopreventivo_id', 'tiposerviciopreventivo_id'])

    def backwards(self, orm):
        # Deleting model 'SistemaServicio'
        db.delete_table('mantenimiento_sistemaservicio')

        # Deleting model 'TipoServicioCorrectivo'
        db.delete_table('mantenimiento_tiposerviciocorrectivo')

        # Deleting model 'TipoServicioPreventivo'
        db.delete_table('mantenimiento_tiposerviciopreventivo')

        # Deleting model 'PeriodoServicio'
        db.delete_table('mantenimiento_periodoservicio')

        # Removing M2M table for field servicios on 'PeriodoServicio'
        db.delete_table('mantenimiento_periodoservicio_servicios')

        # Deleting model 'Mecanico'
        db.delete_table('mantenimiento_mecanico')

        # Deleting model 'Supervisor'
        db.delete_table('mantenimiento_supervisor')

        # Deleting model 'MantenimientoCorrectivo'
        db.delete_table('mantenimiento_mantenimientocorrectivo')

        # Removing M2M table for field servicios on 'MantenimientoCorrectivo'
        db.delete_table('mantenimiento_mantenimientocorrectivo_servicios')

        # Deleting model 'MantenimientoPreventivo'
        db.delete_table('mantenimiento_mantenimientopreventivo')

        # Removing M2M table for field periodo_servicio on 'MantenimientoPreventivo'
        db.delete_table('mantenimiento_mantenimientopreventivo_periodo_servicio')

        # Removing M2M table for field servicios on 'MantenimientoPreventivo'
        db.delete_table('mantenimiento_mantenimientopreventivo_servicios')

    models = {
        'mantenimiento.mantenimientocorrectivo': {
            'Meta': {'object_name': 'MantenimientoCorrectivo'},
            'costo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'horometro': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maquina': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Maquina']"}),
            'mecanico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mantenimiento.Mecanico']", 'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'servicios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mantenimiento.TipoServicioCorrectivo']", 'symmetrical': 'False'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mantenimiento.Supervisor']", 'null': 'True', 'blank': 'True'})
        },
        'mantenimiento.mantenimientopreventivo': {
            'Meta': {'object_name': 'MantenimientoPreventivo'},
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'horometro': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maquina': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Maquina']"}),
            'mecanico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mantenimiento.Mecanico']", 'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'periodo_servicio': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mantenimiento.PeriodoServicio']", 'symmetrical': 'False'}),
            'servicios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mantenimiento.TipoServicioPreventivo']", 'symmetrical': 'False'})
        },
        'mantenimiento.mecanico': {
            'Meta': {'object_name': 'Mecanico'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'mantenimiento.periodoservicio': {
            'Meta': {'object_name': 'PeriodoServicio'},
            'horas': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'servicios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mantenimiento.TipoServicioPreventivo']", 'symmetrical': 'False'})
        },
        'mantenimiento.sistemaservicio': {
            'Meta': {'object_name': 'SistemaServicio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'mantenimiento.supervisor': {
            'Meta': {'object_name': 'Supervisor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'mantenimiento.tiposerviciocorrectivo': {
            'Meta': {'ordering': "('sistema', 'id')", 'object_name': 'TipoServicioCorrectivo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sistema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mantenimiento.SistemaServicio']"}),
            'uso_correctivo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'mantenimiento.tiposerviciopreventivo': {
            'Meta': {'object_name': 'TipoServicioPreventivo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'maquinarias.maquina': {
            'Meta': {'ordering': "['centro_costos']", 'object_name': 'Maquina'},
            'anio': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'centro_costos': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'horas_alerta': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'horometro': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maquina': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.TipoMaquina']"}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Marca']"}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'motor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'placa': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'serie': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'maquinarias.marca': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Marca'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'maquinarias.tipomaquina': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'TipoMaquina'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['mantenimiento']