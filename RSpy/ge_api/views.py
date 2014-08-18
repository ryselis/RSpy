from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from ge_api.models import Item, ItemAddition
from ge_api.forms import HighAlchemyForm


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def highalch(request):
    item_types = request.POST.getlist('f2p_p2p_items', [HighAlchemyForm.F2P, HighAlchemyForm.P2P])
    nature_rune = Item.get(name='Nature rune')
    fire_rune = Item.get(name='Fire rune')
    highalch_cost = nature_rune.price_info.exact + 4 * fire_rune.price_info.exact
    item_additions = ItemAddition.objects.all()
    processed_items = []
    for item in Item.all():
        if (HighAlchemyForm.F2P in item_types and not item.members_item) or (HighAlchemyForm.P2P in item_types and item.members_item):
            addition = [x for x in item_additions if x.id == item.id]
            if len(addition) > 0:
                addition = addition[0]
                processed_items.append({
                    'item': item,
                    'highalch_profit': addition.high_alch_price - item.price_info.exact - highalch_cost
                })
    processed_items = [q for q in sorted(processed_items, key=lambda x: -x['highalch_profit']) if q['highalch_profit'] >= 0]
    form = HighAlchemyForm(initial={
        'f2p_p2p_items': item_types
    })
    return render_to_response('ge/superheat.html', {
        'items': processed_items,
        'form': form
    }, RequestContext(request))
