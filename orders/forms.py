from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_order', 'first_name', 'last_name',
                  'email', 'address', 'postal_code', 'city', 'card_paid']
