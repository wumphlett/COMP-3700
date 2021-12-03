from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import (
    Household,
    User,
    ContactMethod,
    BankAccount,
    CreditCard,
    Fee,
    Charge,
    Payment,
)


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("__str__", "receiving_service")
    list_display_links = ("__str__",)
    fields = ("receiving_service", "street_address", "city", "state", "zip_code")


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    list_display = ("__str__", "customer")
    list_display_links = ("__str__",)
    fields = ("customer", "method_type", "method_value")


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("__str__", "customer")
    list_display_links = ("__str__",)
    fields = ("customer", "account_number", "routing_number")


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("__str__", "customer")
    list_display_links = ("__str__",)
    fields = ("customer", "creditcard_name", "creditcard_number", "cvv", "zip_code")


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "household")
    list_display_links = ("__str__",)
    fields = ("amount", "reason", "household")


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "household")
    list_display_links = ("__str__",)
    fields = ("units_consumed", "price_per_unit", "household")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "household")
    list_display_links = ("__str__",)
    fields = ("customer", "payment_method", "amount", "household")


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "household",
        "is_staff",
        "is_employee",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_employee",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": (("first_name", "last_name"), "email", "password", "household")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_employee", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                    "household",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_employee",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("is_staff", "is_employee")
