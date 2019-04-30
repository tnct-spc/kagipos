from django.shortcuts import render, redirect
from .form import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Temporary


@api_view(['GET'])
def add_idm(request, idm):
    temporary, created = Temporary.objects.get_or_create(idm=idm)
    return Response(temporary.uuid.hex)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # とりあえずトップに飛ばす
            return redirect("/possys/")
    else:
        form = SignupForm()

    return render(request, 'possys/signup.html', {'form': form, })


@login_required
def charge_wallet(request):
    user = request.user
    if request.method == 'POST':
        price = request.POST['price']
        if price != "":
            price = int(price)
            user.wallet += price
            user.save()
        return redirect("/possys/accounts/charge_wallet")

    return render(request, 'possys/charge_wallet.html', {'user': user, })
