from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class Household(models.Model):
    receiving_service = models.BooleanField(default=False)
    street_address = models.CharField(max_length=150, blank=False)
    city = models.CharField(max_length=150, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.street_address}, {self.city} {self.state}, {self.zip_code}"


class User(AbstractUser):
    username = None
    household = models.ForeignKey(Household, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(_("email address"), unique=True)
    is_employee = models.BooleanField(
        verbose_name="employee",
        help_text="Designates whether the user is an employee.",
        default=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(User):
    pass


class Employee(User):
    is_employee = True


class Admin(User):
    is_staff = True


class ContactMethod(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    method_type = models.CharField(max_length=150, blank=False)
    method_value = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return f"{self.method_type} {self.method_value}"


class PaymentMethod(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} Payment Method"


class BankAccount(PaymentMethod):
    account_number = models.PositiveIntegerField()
    routing_number = models.PositiveIntegerField()

    def __str__(self):
        return f"XXXXXX000 XXX-XXXX000"


class CreditCard(PaymentMethod):
    creditcard_name = models.CharField(max_length=150, blank=False)
    creditcard_number = models.PositiveIntegerField()
    cvv = models.PositiveSmallIntegerField()
    zip_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"XXXX-XXXX-XXXX-1234"


class Transaction(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["datetime"]
        abstract = True


class Fee(Transaction):
    title = "Fee"
    reason = models.CharField(max_length=150, blank=False)
    amount = models.FloatField()

    def __str__(self):
        return f"${self.amount} {self.reason}"


class Charge(Transaction):
    title = "Charge"
    units_consumed = models.FloatField()
    price_per_unit = models.FloatField()

    def __str__(self):
        return f"{self.units_consumed} kWh at ${self.price_per_unit} per kWh"


class Payment(Transaction):
    title = "Payment"
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.customer} ${self.amount}"
