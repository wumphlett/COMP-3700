from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import PaymentForm


@login_required(login_url="login")
def index(request):
    return render(request, "index.html")


@login_required(login_url="login")
def customer(request):
    if request.method == "GET":
        transactions = (
            list(request.user.household.payment_set.all())
            + list(request.user.household.charge_set.all())
            + list(request.user.household.fee_set.all())
        )
        transactions.sort(key=lambda x: x.datetime)
        balance = (
            sum((fee.amount for fee in request.user.household.fee_set.all()))
            + sum(
                (
                    charge.units_consumed * charge.price_per_unit
                    for charge in request.user.household.charge_set.all()
                )
            )
            - sum((pay.amount for pay in request.user.household.payment_set.all()))
        )
        context = {
            "household": request.user.household,
            "customers": request.user.household.user_set.all(),
            "usage": request.user.household.charge_set.last(),
            "balance": f"{balance:.2f}",
            "transactions": [
                (transaction.__class__.__name__, transaction)
                for transaction in transactions
            ],
        }
        return render(request, "customer/customer.html", context=context)


@login_required(login_url="login")
def payment(request):
    if request.method == "GET":
        context = {
            "form": PaymentForm(
                request.GET or None,
                initial={"customer": request.user, "household": request.user.household},
            )
        }
        return render(request, "customer/payment.html", context=context)
    elif request.method == "POST":
        form = PaymentForm(
            request.POST or None,
            initial={"customer": request.user, "household": request.user.household},
        )
        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
        else:
            context = {"form": form}
            return render(request, "customer/payment.html", context=context)
