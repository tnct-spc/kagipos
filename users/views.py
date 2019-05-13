from django.shortcuts import redirect
from .forms import SignupForm
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from possys.views import add_transaction
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Temporary, Card, User


@api_view(['GET'])
def add_idm(request, idm):
    temporary, created = Temporary.objects.get_or_create(idm=idm)
    return Response(temporary.uuid.hex)


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'possys/signup.html'
    success_url = '/possys/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['name']
    success_url = '/possys/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.idm = Temporary.objects.get(uuid=self.kwargs['uuid']).idm
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ChargeWalletView(TemplateView):
    template_name = 'possys/charge_wallet.html'

    def post(self, request):
        # 1000円チャージする
        price = 1000
        user = request.user
        add_transaction(price, user)
        return redirect('charge_wallet')
