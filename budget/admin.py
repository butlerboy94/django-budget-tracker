from django.contrib import admin
from .models import Transaction, Bill

# This file controls how models appear in Django's built-in admin panel.
# The admin site is helpful for quickly reviewing or editing data during
# development and demos.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # list_display controls which columns show in the transaction table.
    list_display = ("id", "user", "date", "type", "category", "amount")

    # list_filter adds filter boxes on the right side of the admin page.
    list_filter = ("type", "category", "date")

    # search_fields lets the admin search by username, category, or note text.
    search_fields = ("user__username", "category", "note")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    # Show the most useful bill fields in the admin table.
    list_display = ("id", "user", "name", "amount", "due_date", "paid")

    # Let the admin quickly filter bills by payment status or due date.
    list_filter = ("paid", "due_date")

    # Let the admin search bills by username, bill name, or notes.
    search_fields = ("user__username", "name", "notes")
