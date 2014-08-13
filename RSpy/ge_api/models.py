from django.db import models

# Create your models here.
import json
from urllib2 import urlopen
import datetime


class ItemNotFoundError(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class Item():
    ID_LIST_URL = 'http://api.rsapi.net/idlist.json'
    ITEM_LIST_URL = 'http://api.rsapi.net/ge/item/%(ids)s.json'

    TYPE_AMMO = 'Ammo'

    all_items = None
    last_update = datetime.datetime.now() - datetime.timedelta(hours=1)

    def __init__(self, datadict):
        self.id = datadict['id']
        self.icon = datadict['icon']
        self.icon_large = datadict['icon_large']
        self.type = datadict['type']
        self.name = datadict['name']
        self.description = datadict['description']
        self.members_item = datadict['membersitem'] == 'true'
        self.price_info = PriceInfo(datadict['prices'])

    @classmethod
    def all(cls):
        if not cls.all_items or cls.last_update + datetime.timedelta(hours=1) < datetime.datetime.now():
            cls.last_update = datetime.datetime.now()
            id_list_response = urlopen(cls.ID_LIST_URL).read()
            id_list_response_json = json.loads(id_list_response)
            id_list = [str(x['id']) for x in id_list_response_json]
            all_items = []
            id_list_length = len(id_list)
            ranges = id_list_length / 100
            for i in xrange(ranges):
                start, end = i * 100, (i + 1) * 100
                sliced_ids = id_list[start:end]
                joined_sliced_ids = ','.join(sliced_ids)
                item_list_url = cls.ITEM_LIST_URL % {
                    'ids': joined_sliced_ids
                }
                item_list_response = urlopen(item_list_url).read()
                item_json = json.loads(item_list_response)
                all_items.extend([cls(x) for x in item_json])
            cls.all_items = all_items
        return cls.all_items

    @classmethod
    def filter(cls, **kwargs):
        def filter_func(x):
            filter_passed = True
            for kwarg in kwargs:
                if hasattr(x, kwarg) and getattr(x, kwarg) != kwargs[kwarg]:
                    filter_passed = False
            return filter_passed

        all_items = cls.all()
        return filter(filter_func, all_items)

    @classmethod
    def get(cls, **kwargs):
        filtered_items = cls.filter(**kwargs)
        if len(filtered_items) == 0:
            raise ItemNotFoundError('Item was not found: %s' % kwargs)
        if len(filtered_items) > 1:
            raise MultipleObjectsReturned('Multiple items returned: %s' % filtered_items)
        return filtered_items[0]


class PriceInfo():
    def __init__(self, datadict):
        self.current = PriceHistory(datadict['current'])
        self.today = PriceHistory(datadict['today'])
        self.days30 = PriceHistory(datadict['days30'])
        self.days90 = PriceHistory(datadict['days90'])
        self.exact = int(datadict['exact'])


class PriceHistory():
    TREND_NEUTRAL = 'neutral'
    TREND_POSITIVE = 'positive'
    TREND_NEGATIVE = 'negative'

    def __init__(self, datadict):
        self.trend = datadict['trend']
        # if 'change' in datadict:
        #     self.change = float(datadict['change'].replace('%', '').replace(',', '.')) / 100
        # else:
        #     self.change = None


class ItemAddition(models.Model):
    item_id = models.CharField('ID', max_length=16)
    high_alch_price = models.IntegerField('High alch price')