from django import forms
from .models import Product, Category, CategoriesChoiceField, ProductChoiceField


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'] = CategoriesChoiceField(queryset=Category.objects.all())


class TransactionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = ProductChoiceField(queryset=Product.objects.all())
