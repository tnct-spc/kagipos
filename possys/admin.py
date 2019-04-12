from django.contrib import admin

from .models import Category, Product, Transaction


admin.site.register({Category, Product, Transaction})
