from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Bill, Transaction

# Ask Django for the active User model instead of importing it directly.
# This is the recommended approach because it works even if the project later
# switches to a custom user model.
User = get_user_model()


class RegisterForm(UserCreationForm):
    # Add an email field to Django's default user registration form.
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        # This tells Django which model the form saves to and which fields
        # should appear on the registration page.
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        # Call the parent class first so the default fields are created.
        super().__init__(*args, **kwargs)

        # Replace Django's longer default help text with shorter explanations
        # that are easier for a beginner user to understand.
        self.fields["username"].help_text = "Required. Choose a username for your account."
        self.fields["email"].help_text = "Required. Used for your account profile."
        self.fields["password1"].help_text = "Use at least 8 characters and avoid common passwords."
        self.fields["password2"].help_text = "Enter the same password again for verification."

    def save(self, commit=True):
        # Save the new user, but manually copy the email field because
        # UserCreationForm does not handle that for us by default.
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TransactionForm(forms.ModelForm):
    # A ModelForm automatically builds form fields from the Transaction model.
    class Meta:
        model = Transaction
        fields = ["date", "type", "category", "amount", "note"]
        widgets = {
            # Use the browser's date picker for easier date entry.
            "date": forms.DateInput(attrs={"type": "date"}),

            # Keep the note field compact on the page.
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class BillForm(forms.ModelForm):
    # A ModelForm for creating and updating Bill records.
    class Meta:
        model = Bill
        fields = ["name", "amount", "due_date", "paid", "notes"]
        widgets = {
            # Use the browser's date picker for due dates.
            "due_date": forms.DateInput(attrs={"type": "date"}),

            # Keep the notes box from taking up too much space.
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
