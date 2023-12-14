from django import forms
from .models import Producto

class ProductoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    category = forms.CharField(label="Category", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    price = forms.FloatField(label="Price")
    image = forms.FileField(label="Image")

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and title.islower():
            raise forms.ValidationError("The title should commence with an initial capital letter.")

        return title
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError("The price cannot be negative.")

        return price


