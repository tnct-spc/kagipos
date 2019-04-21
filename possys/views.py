from django.shortcuts import render
from .models import Product, Transaction
from django.contrib.auth.decorators import login_required

# Create your views here.


def products_list(request):
    products = Product.objects.all()

    return render(request, 'possys/products_list.html', {'products': products, })


@login_required
def history(request):
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'possys/history.html', {'transactions': transactions, })
