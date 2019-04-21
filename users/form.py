from django.contrib.auth.forms import UserCreationForm
from users.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('number', 'username', 'last_name', 'first_name', 'email', 'password1', 'password2')