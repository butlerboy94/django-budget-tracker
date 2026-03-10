from django import forms
from .models import Transaction, Bill

# ModelForm for creating and submitting new transactions.
# The user field is intentionally excluded — it is assigned in the view
# using commit=False before saving, to enforce per-user data ownership.
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "type", "category", "amount", "note"]
        widgets = {
            # Renders a native browser date picker input
            "date": forms.DateInput(attrs={"type": "date"}),
            # Limits the note textarea to 3 rows to keep the form compact
            "note": forms.Textarea(attrs={"rows": 3}),
        }

# ModelForm for creating and submitting new bills.
# The user field is intentionally excluded — it is assigned in the view
# using commit=False before saving, to enforce per-user data ownership.
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["name", "amount", "due_date", "paid", "notes"]
        widgets = {
            # Renders a native browser date picker input
            "due_date": forms.DateInput(attrs={"type": "date"}),
            # Limits the notes textarea to 3 rows to keep the form compact
            "notes": forms.Textarea(attrs={"rows": 3}),
        }