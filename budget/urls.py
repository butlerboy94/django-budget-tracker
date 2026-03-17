from django.urls import path

from . import views


# Central URL map for the budget app. Each route is named so templates and
# redirects can reference it cleanly without hard-coding full paths.
urlpatterns = [
    # Dashboard and account setup
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),

    # Transaction CRUD routes
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/add/", views.add_transaction, name="add_transaction"),
    path("transactions/<int:transaction_id>/edit/", views.edit_transaction, name="edit_transaction"),
    path("transactions/<int:transaction_id>/delete/", views.delete_transaction, name="delete_transaction"),

    # Bill routes currently support create plus quick paid/unpaid toggling
    path("bills/add/", views.add_bill, name="add_bill"),
    path("bills/<int:bill_id>/toggle/", views.toggle_bill_paid, name="toggle_bill_paid"),
]
