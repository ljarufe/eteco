# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Marca'
        db.create_table('maquinarias_marca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('maquinarias', ['Marca'])

        # Adding model 'TipoMaquina'
        db.create_table('maquinarias_tipomaquina', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('maquinarias', ['TipoMaquina'])

        # Adding model 'Maquina'
        db.create_table('maquinarias_maquina', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centro_costos', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('maquina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.TipoMaquina'])),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maquinarias.Marca'])),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('serie', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('anio', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('placa', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('motor', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('horometro', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('horas_alerta', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('ubicacion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('maquinarias', ['Maquina'])

        # Adding model 'Operador'
        db.create_table('maquinarias_operador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('maquinarias', ['Operador'])

    def backwards(self, orm):
        # Deleting model 'Marca'
        db.delete_table('maquinarias_marca')

        # Deleting model 'TipoMaquina'
        db.delete_table('maquinarias_tipomaquina')

        # Deleting model 'Maquina'
        db.delete_table('maquinarias_maquina')

        # Deleting model 'Operador'
        db.delete_table('maquinarias_operador')

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
        }
    }

    complete_apps = ['maquinarias']