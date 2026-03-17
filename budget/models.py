from django.db import models
from django.conf import settings

# Models define the structure of the database tables for this app.
# Each class below becomes a table in SQLite.
class Transaction(models.Model):
    # These constants make the code easier to read and reduce spelling errors.
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    # choices makes Django show a dropdown in forms instead of a plain text box.
    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    # Link each transaction to the user who created it.
    # related_name="transactions" lets us access a user's transactions with
    # user.transactions.all()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    # Basic transaction details.
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    class Meta:
        # Show newest transactions first.
        ordering = ["-date", "-id"]

        # Database indexes help common queries run faster.
        indexes = [
            models.Index(fields=["user", "date"], name="idx_tx_user_date"),
            models.Index(fields=["user", "type", "date"], name="idx_tx_user_type_date"),
        ]

    def __str__(self) -> str:
        # This controls how the object appears in the admin panel and shell.
        return f"{self.user.username} | {self.type} | {self.category} | {self.amount} on {self.date}"


class Bill(models.Model):
    # Link each bill to the user who owns it.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bills"
    )

    # Basic bill details.
    name = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        # Show unpaid bills first, then sort by due date.
        ordering = ["paid", "due_date", "-id"]

        # Add indexes for the queries this app uses most often.
        indexes = [
            models.Index(fields=["user", "due_date"], name="idx_bill_user_duedate"),
            models.Index(fields=["user", "paid"], name="idx_bill_user_paid"),
        ]

    def __str__(self) -> str:
        # Build a readable label for the admin panel and Django shell.
        paid_text = "PAID" if self.paid else "UNPAID"
        return f"{self.user.username} | {self.name} | {paid_text} | due {self.due_date}"
