# -*- coding: utf-8 -*-
from urllib2 import urlopen
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from ge_api.models import Item


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        rs_api_items = Item.all()
        rune_wikia_url = 'http://runescape.wikia.com/wiki/%s'
        ItemAddition = orm.ItemAddition
        for item in rs_api_items:
            url = rune_wikia_url % item.name.replace(' ', '_')
            html = urlopen(url).read()
            index1 = html.find('High Alch')
            index2 = html[index1:].find('<td>')
            index3 = html[index1:][index2:].find('</td>')
            price = html[index1+index2:index1+index2+index3].replace('<td> ', '').replace('&#160;coins\n', '')
            price = price.replace('&#160;coin\n', '')
            try:
                split = price.replace(',', '').replace('gp', '').split(' ')
                price = '0'
                for p in split[::-1]:
                    try:
                        price = int(p)
                        break
                    except ValueError:
                        continue
                price = int(price)
                ItemAddition.objects.create(id=item.id,
                                            high_alch_price=price)
            except ValueError:
                import pdb; pdb.set_trace()
                print 'item not found: %s %s coins' % (item.name, price)
            else:
                print 'item done: %s' % item.name

    def backwards(self, orm):
        "Write your backwards methods here."
        ItemAddition = orm.ItemAddition
        ItemAddition.objects.all().delete()

    models = {
        u'ge_api.itemaddition': {
            'Meta': {'object_name': 'ItemAddition'},
            'high_alch_price': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['ge_api']
    symmetrical = True
