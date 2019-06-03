from django.urls import path
from . import views as users_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('signup/', users_views.SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(template_name="possys/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_reset/',
         PasswordResetView.as_view(template_name="possys/password_reset.html"),
         name="password_reset"),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name="possys/password_reset_done.html"),
         name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="possys/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name="possys/password_reset_complete.html"),
         name="password_reset_complete"),
    path('add_card/<uuid>/', users_views.CardCreateView.as_view(template_name='possys/add_card.html'), name='add_card'),
    path('charge_wallet/', users_views.ChargeWalletView.as_view(), name="charge_wallet"),
    path('api/add_idm/<idm>/', users_views.add_idm),
]
