from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Payment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ("payment_method", "amount", "customer", "household")
