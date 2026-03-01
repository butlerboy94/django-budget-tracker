from django.shortcuts import render, redirect #import HttpResponse
from django.http import HttpResponse #import HttpResponse to return a response to the user
from django.contrib.auth.decorators import login_required #import login_required to restrict access to authenticated users only
from .models import Transaction, Bill #import Transaction model to interact with the database
from django.db.models import Sum #import Sum to calculate the total income and expenses for the user
from django.contrib import messages #import messages to display success or error messages to the user
from .forms import TransactionForm, BillForm #import forms to handle user input for transactions and
from django.utils import timezone #import timezone to handle date and time for transactions and bills




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

    bills = Bill.objects.filter(user=user).order_by("paid", "due_date") # this will order the bills first by paid status (unpaid bills will come first) and then by due date within each group, so that unpaid bills are prioritized and sorted by their due dates.
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
        "bills": bills,
    }

    return render(request, "budget/dashboard.html", context)

# This view handles the addition of new transactions. It checks if the request method is POST, validates the form data, and saves the transaction to the database. If the form is valid, it redirects the user back to the home page with a success message. If the request method is GET, it simply renders an empty form for the user to fill out.
@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            messages.success(request, "Transaction added.")
            return redirect("home")
    else:
        form = TransactionForm()

    return render(request, "budget/transaction_form.html", {"form": form})


# This view handles the addition of new bills. Similar to the add_transaction view, it checks if the request method is POST, validates the form data, and saves the bill to the database. If the form is valid, it redirects the user back to the home page with a success message. If the request method is GET, it renders an empty form for the user to fill out.
@login_required
def add_bill(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill added.")
            return redirect("home")
    else:
        form = BillForm()

    return render(request, "budget/bill_form.html", {"form": form})


# This view toggles the paid status of a bill. It only accepts POST requests to prevent accidental changes via link clicks. It retrieves the bill based on the provided bill_id and checks if it belongs to the logged-in user. If the bill is found, it toggles the paid status and saves the change to the database. Finally, it redirects the user back to the home page with a success message indicating whether the bill is now marked as paid or unpaid.
@login_required
def toggle_bill_paid(request, bill_id):
    # POST-only toggle to avoid accidental changes via link clicks
    if request.method != "POST":
        return redirect("home")

    try:
        bill = Bill.objects.get(id=bill_id, user=request.user)
    except Bill.DoesNotExist:
        messages.error(request, "Bill not found.")
        return redirect("home")

    bill.paid = not bill.paid
    bill.save()
    messages.success(request, f"Bill marked as {'paid' if bill.paid else 'unpaid'}.")
    return redirect("home")