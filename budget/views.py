from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BillForm, RegisterForm, TransactionForm
from .models import Bill, Transaction


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect(next_url or "home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form, "next": next_url})


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
    transactions = Transaction.objects.filter(user=user).order_by("-date", "-id")[:10]
    bills = Bill.objects.filter(user=user).order_by("paid", "due_date")
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
        "transactions": transactions,
    }
    return render(request, "budget/dashboard.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
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
    transactions = Transaction.objects.filter(user=request.user).order_by("-date", "-id")
    return render(request, "budget/transaction_list.html", {"transactions": transactions})


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
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
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
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
def toggle_bill_paid(request, bill_id):
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
