from django.shortcuts import render
from .models import Product, Transaction, Category
from users.models import get_user_from_idm
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from kagipos.errors import CustomError


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IsPossysHousing(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='possys').exists()


def add_transaction(price, user, product=None):
    transaction = Transaction(
        price=price,
        user=user,
        product=product
    )
    try:
        transaction.save()
    except CustomError as e:
        return Response(str(e), status=418)
    return Response('True,wallet=' + str(user.wallet))


@login_required
@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_with_product(request, idm, product_id):
    product = Product.objects.filter(pk=product_id).first()
    if product is None:
        return Response('Product is not found', status=418)
    return add_transaction(-product.price, get_user_from_idm(idm), product)


@login_required
@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_without_product(request, idm, price):
    return add_transaction(price, get_user_from_idm(idm))


def products_list(request):
    categories = Category.objects.all()
    products_dictionary_of_each_category = {}
    for category in categories:
        tmp_list = Product.objects.filter(categories=category)
        products_dictionary_of_each_category[category] = tmp_list
    return render(request, 'possys/products_list.html', {
        'products_dictionary_of_each_category': products_dictionary_of_each_category,
    })


@login_required
def history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'possys/history.html', {'transactions': transactions, })
