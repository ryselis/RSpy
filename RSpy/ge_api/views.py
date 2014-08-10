from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from ge_api.models import Item


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def superheat(request):
    nature_rune = Item.get(name='Nature rune')
    fire_rune = Item.get(name='Fire rune')
    highalch_cost = nature_rune.price_info.exact + 4 * fire_rune.price_info.exact
    processed_items = [{
        'item': item,
        'highalch_profit': - item.price_info.exact - highalch_cost
    } for item in Item.all()]
    processed_items = sorted(processed_items, key=lambda x: -x['highalch_profit'])[:100]
    return render_to_response('ge/superheat.html', {
        'items': processed_items
    }, RequestContext(request))