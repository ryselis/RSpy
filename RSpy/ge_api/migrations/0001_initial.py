# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemAddition'
        db.create_table(u'ge_api_itemaddition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('high_alch_price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ge_api', ['ItemAddition'])


    def backwards(self, orm):
        # Deleting model 'ItemAddition'
        db.delete_table(u'ge_api_itemaddition')


    models = {
        u'ge_api.itemaddition': {
            'Meta': {'object_name': 'ItemAddition'},
            'high_alch_price': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['ge_api']