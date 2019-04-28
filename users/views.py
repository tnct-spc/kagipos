from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View

# Create your views here.


class SignupView(View):
    form_class = SignupForm
    template_name = 'possys/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # とりあえずトップに飛ばす
            return redirect('/possys/')
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
