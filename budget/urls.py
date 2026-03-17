from django.urls import path

from . import views


# This file connects URL paths to the view functions in views.py.
# Each name= value gives us a reusable label we can reference in templates,
# redirects, and tests.
urlpatterns = [
    # Dashboard and user registration
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),

    # Transaction pages
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/add/", views.add_transaction, name="add_transaction"),
    path("transactions/<int:transaction_id>/edit/", views.edit_transaction, name="edit_transaction"),
    path("transactions/<int:transaction_id>/delete/", views.delete_transaction, name="delete_transaction"),

    # Bill pages
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/add/", views.add_bill, name="add_bill"),
    path("bills/<int:bill_id>/edit/", views.edit_bill, name="edit_bill"),
    path("bills/<int:bill_id>/delete/", views.delete_bill, name="delete_bill"),
    path("bills/<int:bill_id>/toggle/", views.toggle_bill_paid, name="toggle_bill_paid"),
]
