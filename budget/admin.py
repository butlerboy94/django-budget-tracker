from django.contrib import admin
from .models import Transaction, Bill

# Register Transaction and Bill models with the Django admin site
# so they are accessible and manageable from the /admin/ panel.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Columns shown in the transaction list view in the admin panel
    list_display = ("id","user", "date", "type", "category", "amount")
    # Sidebar filters for narrowing down transactions by type, category, or date
    list_filter = ("type", "category", "date")
    # Fields that the admin search bar will query against
    search_fields = ("user__username", "category", "note")

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    # Columns shown in the bill list view in the admin panel
    list_display = ("id", "user", "name", "amount", "due_date", "paid")
    # Sidebar filters for narrowing down bills by paid status or due date
    list_filter = ("paid", "due_date")
    # Fields that the admin search bar will query against
    search_fields = ("user__username", "name", "notes")