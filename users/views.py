from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from possys.views import add_transaction
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Temporary, Card


@api_view(['GET'])
def add_idm(request, idm):
    temporary = Temporary(
        idm=idm
    )
    temporary.save()
    return Response(temporary.uuid.hex)


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


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['name']
    success_url = '/possys/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.idm = Temporary.objects.get(uuid=self.kwargs['uuid']).idm
        return super().form_valid(form)


@login_required
def charge_wallet(request):
    if request.method == 'POST':
        # 1000円チャージする
        price = 1000
        user = request.user
        # 引数がidmからuserに変更されるので先に対応しておく
        add_transaction(price, user)
        return redirect('charge_wallet')
    return render(request, 'possys/charge_wallet.html', {})
