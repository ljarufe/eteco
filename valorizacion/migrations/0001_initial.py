# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cliente'
        db.create_table('valorizacion_cliente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('procedencia', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('valorizacion', ['Cliente'])

        # Adding model 'Obra'
        db.create_table('valorizacion_obra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['valorizacion.Cliente'])),
        ))
        db.send_create_signal('valorizacion', ['Obra'])

        # Adding model 'ParteDiario'
        db.create_table('valorizacion_partediario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('maquina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Maquina'])),
            ('operador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Operador'], null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('obra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['valorizacion.Obra'])),
            ('detalles', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('horometro_inicio', self.gf('django.db.models.fields.FloatField')()),
            ('horometro_final', self.gf('django.db.models.fields.FloatField')()),
            ('horas_trabajadas', self.gf('django.db.models.fields.FloatField')()),
            ('calentamiento', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('valorizacion', ['ParteDiario'])

        # Adding model 'ValorizacionSimple'
        db.create_table('valorizacion_valorizacionsimple', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('maquina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Maquina'])),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('valorizacion', ['ValorizacionSimple'])

        # Adding model 'Valorizacion'
        db.create_table('valorizacion_valorizacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('costo_hora', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('valorizacion', ['Valorizacion'])

        # Adding M2M table for field valorizaciones on 'Valorizacion'
        db.create_table('valorizacion_valorizacion_valorizaciones', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('valorizacion', models.ForeignKey(orm['valorizacion.valorizacion'], null=False)),
            ('valorizacionsimple', models.ForeignKey(orm['valorizacion.valorizacionsimple'], null=False))
        ))
        db.create_unique('valorizacion_valorizacion_valorizaciones', ['valorizacion_id', 'valorizacionsimple_id'])

        # Adding M2M table for field partes on 'Valorizacion'
        db.create_table('valorizacion_valorizacion_partes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('valorizacion', models.ForeignKey(orm['valorizacion.valorizacion'], null=False)),
            ('partediario', models.ForeignKey(orm['valorizacion.partediario'], null=False))
        ))
        db.create_unique('valorizacion_valorizacion_partes', ['valorizacion_id', 'partediario_id'])

    def backwards(self, orm):
        # Deleting model 'Cliente'
        db.delete_table('valorizacion_cliente')

        # Deleting model 'Obra'
        db.delete_table('valorizacion_obra')

        # Deleting model 'ParteDiario'
        db.delete_table('valorizacion_partediario')

        # Deleting model 'ValorizacionSimple'
        db.delete_table('valorizacion_valorizacionsimple')

        # Deleting model 'Valorizacion'
        db.delete_table('valorizacion_valorizacion')

        # Removing M2M table for field valorizaciones on 'Valorizacion'
        db.delete_table('valorizacion_valorizacion_valorizaciones')

        # Removing M2M table for field partes on 'Valorizacion'
        db.delete_table('valorizacion_valorizacion_partes')

    models = {
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
        'maquinarias.operador': {
            'Meta': {'object_name': 'Operador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'maquinarias.tipomaquina': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'TipoMaquina'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'valorizacion.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'procedencia': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'valorizacion.obra': {
            'Meta': {'object_name': 'Obra'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['valorizacion.Cliente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'valorizacion.partediario': {
            'Meta': {'ordering': "('horometro_final',)", 'object_name': 'ParteDiario'},
            'calentamiento': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'detalles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'horas_trabajadas': ('django.db.models.fields.FloatField', [], {}),
            'horometro_final': ('django.db.models.fields.FloatField', [], {}),
            'horometro_inicio': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maquina': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Maquina']"}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'obra': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['valorizacion.Obra']"}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Operador']", 'null': 'True', 'blank': 'True'})
        },
        'valorizacion.valorizacion': {
            'Meta': {'object_name': 'Valorizacion'},
            'costo_hora': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['valorizacion.ParteDiario']", 'null': 'True', 'blank': 'True'}),
            'valorizaciones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['valorizacion.ValorizacionSimple']", 'symmetrical': 'False'})
        },
        'valorizacion.valorizacionsimple': {
            'Meta': {'object_name': 'ValorizacionSimple'},
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maquina': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maquinarias.Maquina']"})
        }
    }

    complete_apps = ['valorizacion']