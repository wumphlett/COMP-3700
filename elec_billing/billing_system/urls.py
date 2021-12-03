from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index),
    path("customer", views.customer, name="customer_dashboard"),
    path("payment", views.payment, name="customer_payment"),
    path("accounts/", include("django.contrib.auth.urls")),
]
