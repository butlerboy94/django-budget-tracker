from django.shortcuts import render #import HttpResponse
from django.http import HttpResponse #import HttpResponse to return a response to the user
from django.contrib.auth.decorators import login_required #import login_required to restrict access to authenticated users only
from .models import Transaction, Bill #import Transaction model to interact with the database
from django.db.models import Sum #import Sum to calculate the total income and expenses for the user


# Create your views here.
#this view is a simple home page that displays a welcome message and the number of transactions the logged-in user has. The @login_required decorator ensures that only authenticated users can access this view.
@login_required
def home(request):
    user = request.user

    income_total = (
        Transaction.objects
        .filter(user=user, type=Transaction.INCOME)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    expense_total = (
        Transaction.objects
        .filter(user=user, type=Transaction.EXPENSE)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    balance = income_total - expense_total

    bills = Bill.objects.filter(user=user)
    total_bills = bills.count()
    paid_bills = bills.filter(paid=True).count()
    unpaid_bills = bills.filter(paid=False).count()

    context = {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "total_bills": total_bills,
        "paid_bills": paid_bills,
        "unpaid_bills": unpaid_bills,
    }

    return render(request, "budget/dashboard.html", context)
