from django.shortcuts import render
from .models import Product, Transaction, Category
from users.models import Card
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IsPossysHousing(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='possys').exists()


def add_transaction(price, idm, product=None):
    card = Card.objects.filter(idm=idm).first()
    if card is None:
        return Response('IDm is not found', status=418)

    transaction = Transaction(
        price=price,
        user=card.user,
        product=product
    )
    transaction.save()
    return Response('True,wallet=' + str(card.user.wallet))


@login_required
@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_with_product(request, price, idm, product_id):
    product = Product.objects.filter(pk=product_id).first()
    if product is None:
        return Response('Product is not found', status=418)
    return add_transaction(price, idm, product)


@login_required
@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_without_product(request, price, idm):
    return add_transaction(price, idm)


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
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'possys/history.html', {'transactions': transactions, })
