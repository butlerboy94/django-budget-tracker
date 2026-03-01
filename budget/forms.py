from django import forms
from .models import Transaction, Bill

# Transaction form for adding/editing transactions
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "type", "category", "amount", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }

# Bill form for adding/editing bills
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["name", "amount", "due_date", "paid", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }