from django.forms import forms, fields, widgets

class HighAlchemyForm(forms.Form):
    F2P = "f2p"
    P2P = "p2p"
    F2P_P2P_CHOICES = (
        (F2P, "Free-to-play items"),
        (P2P, "Members' items")
    )
    f2p_p2p_items = fields.MultipleChoiceField(label="Item type", choices=F2P_P2P_CHOICES, widget=widgets.CheckboxSelectMultiple())
