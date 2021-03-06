from django.shortcuts import render
from .models import Product, Transaction, Category
from users.models import get_user_from_idm
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from kagipos.errors import CustomError
from django.views.generic.list import ListView


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


@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_with_product(request, idm, product_id):
    product = Product.objects.filter(pk=product_id).first()
    if product is None:
        return Response('Product is not found', status=418)
    return add_transaction(-product.price, get_user_from_idm(idm), product)


@permission_classes(IsPossysHousing)
@api_view(['GET'])
def add_transaction_without_product(request, idm, price):
    return add_transaction(price, get_user_from_idm(idm))


class StoreView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'possys/store.html'
    result = None

    @method_decorator(login_required, name='dispatch')
    def post(self, request):
        user = request.user
        product_id = request.POST["product_id"]
        product = Product.objects.get(id=product_id)
        price = product.price

        result = add_transaction(price=-price, user=user, product=product)
        return render(request, 'possys/store.html', {
            'result': result,
            'categories': Category.objects.all(),
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.result
        return context


@method_decorator(login_required, name='dispatch')
class HistoryView(ListView):
    context_object_name = 'transactions'
    template_name = 'possys/history.html'

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-timestamp')
        return queryset
