from django import forms
from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','quantity','image']


class OrderForm(forms.Form):
    PAYMENT_METHOD=[('cash_on_delivery' ,'Cash on Delivery'),
    ("online paymeny","online paymeny")
    ]
    name = forms.CharField(label='Name', max_length=100,required=True)
    address = forms.CharField(label='Address', widget=forms.Textarea,required=True)
    phone_number = forms.CharField(label='Phone Number', max_length=20,required=True)
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_METHOD,required=True)






