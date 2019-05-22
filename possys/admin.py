from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Product, Transaction
from .forms import ProductAdminForm, TransactionAdminForm


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price', 'get_categories')
    form = ProductAdminForm

    def get_categories(self, obj: Product):
        return ', '.join(obj.categories.all().values_list('name', flat=True)) if obj.categories.all().exists() else '-'
    get_categories.short_description = 'カテゴリー'


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('price', 'get_username', 'get_product_name', 'timestamp')
    form = TransactionAdminForm

    def get_username(self, obj: Transaction):
        return obj.user.username
    get_username.short_description = 'ユーザー名'

    def get_product_name(self, obj: Transaction):
        return obj.product.name if obj.product is not None else '-'
    get_product_name.short_description = '商品名'
