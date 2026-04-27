import json
from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BillForm, RegisterForm, TransactionForm
from .models import Bill, Transaction


def register(request):
    # This view handles account creation for new users.
    # If the user is already signed in, there is no reason to show the
    # registration form again, so redirect them back to the dashboard.
    if request.user.is_authenticated:
        return redirect("home")

    # Preserve Django's optional "next" parameter so users who were sent to
    # register from a protected page can continue where they intended to go.
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the new user account, log the user in immediately, and then
            # redirect to either the protected destination or the dashboard.
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect(next_url or "home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form, "next": next_url})


@login_required
def home(request):
    # This is the main dashboard page users see after logging in.
    # All dashboard data is filtered by the logged-in user to keep each
    # person's budget data private and isolated.
    user = request.user

    # Aggregate income and expense totals separately, then use them to build
    # the current account balance shown at the top of the dashboard.
    income_total = round(
        Transaction.objects
        .filter(user=user, type=Transaction.INCOME)
        .aggregate(total=Sum("amount"))["total"] or 0, 2
    )

    expense_total = round(
        Transaction.objects
        .filter(user=user, type=Transaction.EXPENSE)
        .aggregate(total=Sum("amount"))["total"] or 0, 2
    )

    paid_bills_total = round(
        Bill.objects
        .filter(user=user, paid=True)
        .aggregate(total=Sum("amount"))["total"] or 0, 2
    )

    expense_total = round(expense_total + paid_bills_total, 2)
    balance = round(income_total - expense_total, 2)

    # Show only recent activity on the dashboard to keep the page focused,
    # while still giving the user a link to the full transaction history.
    transactions = Transaction.objects.filter(user=user).order_by("-date", "-id")[:10]

    # Bills are ordered with unpaid items first so important items appear near
    # the top of the dashboard.
    bills = Bill.objects.filter(user=user).order_by("paid", "due_date")
    total_bills = bills.count()
    paid_bills = bills.filter(paid=True).count()
    unpaid_bills = bills.filter(paid=False).count()

    # Build the last 6 months as date objects (first day of each month) so we
    # can create labeled buckets for the bar chart regardless of whether the
    # user has any transactions in a given month.
    today = date.today()
    chart_months = []
    for i in range(5, -1, -1):
        month = today.month - i
        year = today.year
        while month <= 0:
            month += 12
            year -= 1
        chart_months.append(date(year, month, 1))

    chart_start = chart_months[0]

    # Group income transactions by month and store as a {YYYY-MM: total} dict
    # so they can be looked up by the label keys built above.
    income_by_month = {
        row["month"].strftime("%Y-%m"): float(row["total"])
        for row in (
            Transaction.objects
            .filter(user=user, type=Transaction.INCOME, date__gte=chart_start)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
        )
    }

    # Same grouping for expense transactions.
    expense_by_month = {
        row["month"].strftime("%Y-%m"): float(row["total"])
        for row in (
            Transaction.objects
            .filter(user=user, type=Transaction.EXPENSE, date__gte=chart_start)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
        )
    }

    # Convert the month buckets into parallel JSON arrays that Chart.js can
    # consume directly: labels (human-readable month names) and two data series.
    chart_labels = json.dumps([m.strftime("%b %Y") for m in chart_months])
    chart_income = json.dumps([income_by_month.get(m.strftime("%Y-%m"), 0) for m in chart_months])
    chart_expense = json.dumps([expense_by_month.get(m.strftime("%Y-%m"), 0) for m in chart_months])

    context = {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "total_bills": total_bills,
        "paid_bills": paid_bills,
        "unpaid_bills": unpaid_bills,
        "bills": bills,
        "transactions": transactions,
        # Chart data passed as JSON strings so the template can inject them
        # directly into the Chart.js configuration without extra serialization.
        "chart_labels": chart_labels,
        "chart_income": chart_income,
        "chart_expense": chart_expense,
    }
    return render(request, "budget/dashboard.html", context)


@login_required
def add_transaction(request):
    # This view displays the transaction form and saves a new transaction.
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            # The user field is intentionally assigned here instead of being
            # exposed in the form so one user cannot create data for another.
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added.")
            return redirect("home")
    else:
        form = TransactionForm()

    return render(
        request,
        "budget/transaction_form.html",
        {
            "form": form,
            "page_title": "Add Transaction",
            "heading": "Add Transaction",
            "submit_label": "Save Transaction",
        },
    )


@login_required
def transaction_list(request):
    # Show every transaction that belongs to the current user.
    # This management page shows the full transaction history for the current
    # user, unlike the dashboard which only displays recent activity.
    transactions = Transaction.objects.filter(user=request.user).order_by("-date", "-id")
    return render(request, "budget/transaction_list.html", {"transactions": transactions})


@login_required
def edit_transaction(request, transaction_id):
    # This view lets a user update one existing transaction.
    # get_object_or_404 with the current user check prevents users from editing
    # transactions that do not belong to them.
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            # Keep ownership attached to the current user even during updates.
            updated_transaction = form.save(commit=False)
            updated_transaction.user = request.user
            updated_transaction.save()
            messages.success(request, "Transaction updated.")
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "budget/transaction_form.html",
        {
            "form": form,
            "page_title": "Edit Transaction",
            "heading": "Edit Transaction",
            "submit_label": "Update Transaction",
        },
    )


@login_required
def delete_transaction(request, transaction_id):
    # This view shows a confirmation page and then deletes the transaction.
    # The same user filter is applied here so delete actions are limited to the
    # owner of the transaction.
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        # Use a confirmation page first so transactions are not deleted by an
        # accidental click from the list or dashboard.
        transaction.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("transaction_list")

    return render(
        request,
        "budget/transaction_confirm_delete.html",
        {"transaction": transaction},
    )


@login_required
def add_bill(request):
    # This view displays the bill form and saves a new bill.
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            # Bills follow the same ownership pattern as transactions so each
            # user's billing data stays separate.
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill added.")
            return redirect("home")
    else:
        form = BillForm()

    return render(
        request,
        "budget/bill_form.html",
        {
            "form": form,
            "page_title": "Add Bill",
            "heading": "Add Bill",
            "submit_label": "Save Bill",
        },
    )


@login_required
def bill_list(request):
    # Show every bill that belongs to the current user.
    # This management page shows every bill for the current user so payment
    # deadlines and statuses can be reviewed in one place.
    bills = Bill.objects.filter(user=request.user).order_by("paid", "due_date", "-id")
    return render(request, "budget/bill_list.html", {"bills": bills})


@login_required
def edit_bill(request, bill_id):
    # This view lets a user update one existing bill.
    # Restrict editing to bills owned by the logged-in user.
    bill = get_object_or_404(Bill, id=bill_id, user=request.user)

    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            updated_bill = form.save(commit=False)
            updated_bill.user = request.user
            updated_bill.save()
            messages.success(request, "Bill updated.")
            return redirect("bill_list")
    else:
        form = BillForm(instance=bill)

    return render(
        request,
        "budget/bill_form.html",
        {
            "form": form,
            "page_title": "Edit Bill",
            "heading": "Edit Bill",
            "submit_label": "Update Bill",
        },
    )


@login_required
def delete_bill(request, bill_id):
    # This view shows a confirmation page and then deletes the bill.
    # Restrict deletion to bills owned by the logged-in user.
    bill = get_object_or_404(Bill, id=bill_id, user=request.user)

    if request.method == "POST":
        bill.delete()
        messages.success(request, "Bill deleted.")
        return redirect("bill_list")

    return render(request, "budget/bill_confirm_delete.html", {"bill": bill})


@login_required
def toggle_bill_paid(request, bill_id):
    # This view flips a bill between paid and unpaid.
    # This status change should only happen through an explicit form POST.
    if request.method != "POST":
        return redirect("home")

    try:
        # Limit the lookup to the logged-in user to prevent unauthorized edits.
        bill = Bill.objects.get(id=bill_id, user=request.user)
    except Bill.DoesNotExist:
        messages.error(request, "Bill not found.")
        return redirect("home")

    # Flipping the boolean keeps the UI simple: one button can mark a bill as
    # paid or unpaid depending on its current state.
    bill.paid = not bill.paid
    bill.save()
    messages.success(request, f"Bill marked as {'paid' if bill.paid else 'unpaid'}.")
    return redirect("home")
