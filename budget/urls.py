from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("transactions/add/", views.add_transaction, name="add_transaction"),
    path("bills/add/", views.add_bill, name="add_bill"),
    path("bills/<int:bill_id>/toggle/", views.toggle_bill_paid, name="toggle_bill_paid"),
]
