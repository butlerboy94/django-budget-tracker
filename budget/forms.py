from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Bill, Transaction

# Ask Django for the active User model instead of importing it directly.
User = get_user_model()


class BootstrapFormMixin:
    """Automatically adds Bootstrap CSS classes to every widget in a form.

    Loops through all fields after the parent __init__ runs and sets the
    appropriate class based on the widget type:
      - Select / SelectMultiple  → form-select
      - CheckboxInput            → form-check-input
      - Everything else          → form-control
    This keeps Bootstrap styling in one place instead of repeating it on
    every widget definition across multiple form classes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault("class", "form-select")
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            else:
                widget.attrs.setdefault("class", "form-control")


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    # Add an email field to Django's default user registration form.
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        # BootstrapFormMixin.__init__ is called via super() through the MRO,
        # which adds Bootstrap classes after UserCreationForm builds its fields.
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


class TransactionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "type", "category", "amount", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class BillForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["name", "amount", "due_date", "paid", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
