from django.db import models
from django.conf import settings 
from django.utils import timezone

# Create your models here.

# this Transaction model represents a financial transaction made by a user. 
# It includes fields for the user (linked to Django's built-in User model), date, type (income or expense), category, amount, and an optional note. 
# The Meta class defines ordering and indexes for efficient querying. The __str__ method provides a readable string representation of the transaction.
class Transaction(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    # FK to Django's built-in User table
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions" # this block allows us to access transactions from the user model using user.transactions.all()
    )

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["user", "date"], name="idx_tx_user_date"),
            models.Index(fields=["user", "type", "date"], name="idx_tx_user_type_date"),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} | {self.type} | {self.category} | {self.amount} on {self.date}"


# The Bill model represents a bill that a user needs to pay. 
# It includes fields for the user, name of the bill, amount, due date, status (paid or unpaid), and optional notes.
class Bill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bills"
    )

    name = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)  # False = unpaid, True = paid
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["paid", "due_date", "-id"]
        indexes = [
            models.Index(fields=["user", "due_date"], name="idx_bill_user_duedate"),
            models.Index(fields=["user", "paid"], name="idx_bill_user_paid"),
        ]

    def __str__(self) -> str:
        paid_text = "PAID" if self.paid else "UNPAID"
        return f"{self.user.username} | {self.name} | {paid_text} | due {self.due_date}"