from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.


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
        # 1000円チャージする
        user.wallet += 1000
        user.save()
        return redirect("/accounts/charge_wallet")

    return render(request, 'possys/charge_wallet.html', {'user': user, })
