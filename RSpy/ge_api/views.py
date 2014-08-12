from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from ge_api.models import Item, ItemAddition


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def highalch(request):
    nature_rune = Item.get(name='Nature rune')
    fire_rune = Item.get(name='Fire rune')
    highalch_cost = nature_rune.price_info.exact + 4 * fire_rune.price_info.exact
    item_additions = ItemAddition.objects.all()
    processed_items = []
    for item in Item.all():
        addition = filter(lambda x: x.id == item.id, item_additions)
        if len(addition) > 0:
            addition = addition[0]
            processed_items.append({
                'item': item,
                'highalch_profit': addition.high_alch_price - item.price_info.exact - highalch_cost
            })
    processed_items = sorted(processed_items, key=lambda x: -x['highalch_profit'])[:100]
    return render_to_response('ge/superheat.html', {
        'items': processed_items
    }, RequestContext(request))