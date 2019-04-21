from django.urls import path
from . import views as users_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', users_views.signup, name="signup"),
    path('login/', LoginView.as_view(template_name="possys/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('charge_wallet/', users_views.charge_wallet, name="chargeWallet"),
]
