# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MantenimientoPreventivo.costo'
        db.add_column('mantenimiento_mantenimientopreventivo', 'costo',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'MantenimientoPreventivo.costo'
        db.delete_column('mantenimiento_mantenimientopreventivo', 'costo')

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
            'costo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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