from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Bill, Transaction

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Required. Choose a username for your account."
        self.fields["email"].help_text = "Required. Used for your account profile."
        self.fields["password1"].help_text = "Use at least 8 characters and avoid common passwords."
        self.fields["password2"].help_text = "Enter the same password again for verification."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "type", "category", "amount", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["name", "amount", "due_date", "paid", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
