from django.contrib import admin
from .models import Transaction, Bill

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id","user", "date", "type", "category", "amount")
    list_filter = ("type", "category", "date")
    search_fields = ("user__username", "category", "note")

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "amount", "due_date", "paid")
    list_filter = ("paid", "due_date")
    search_fields = ("user__username", "name", "notes")