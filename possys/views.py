from django.shortcuts import render, redirect
from .form import SignupForm
from django.contrib.auth import login
from .models import Product

# Create your views here.

def ProductsList(request):
    prodcts = Product.objects.all()

    return render(request, 'possys/produtsList.html', {'products': prodcts, })

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