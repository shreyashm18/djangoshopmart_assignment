from django import forms
from .models import Products, Category, Tags, Cartitems, Cart

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'

class CartItemForm(forms.ModelForm):
    class Meta:
        model=Cartitems
        fields='__all__'