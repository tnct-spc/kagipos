from django.shortcuts import render, redirect
from .form import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Product, Transaction
from users.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def ProductsList(request):
    prodcts = Product.objects.all()

    return render(request, 'possys/produtsList.html', {'products': prodcts, })

@login_required
def History(request):
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'possys/history.html', {'transactions': transactions, })


@login_required
def ChargeWallet(request):
    user = request.user
    if request.method == 'POST':
        price = request.POST['price']
        if price != "":
            price = int(price)
            user.wallet += price
            user.save()
        return redirect("/possys/chargeWallet")

    return render(request, 'possys/chargeWallet.html', {'user': user, })


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("/possys/") #とりあえずトップに飛ばす
    else:
        form = SignupForm()

    return render(request, 'possys/signup.html', {'form': form, })