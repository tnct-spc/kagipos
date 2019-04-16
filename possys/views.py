from django.shortcuts import render, redirect
from .form import SignupForm
from django.contrib.auth import login

# Create your views here.

def Signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
        return render(request, 'possys/signup.html', {'form': form, })