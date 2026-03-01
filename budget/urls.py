from django.urls import path 
from . import views


# Define URL patterns for the budget app
urlpatterns = [
    path('', views.home, name='home'), # This will route the root URL of the budget app to the home view
    path("transactions/add/", views.add_transaction, name="add_transaction"), # This will route the URL for adding a transaction to the add_transaction view
    path("bills/add/", views.add_bill, name="add_bill"), # This will route the URL for adding a bill to the add_bill view
    path("bills/<int:bill_id>/toggle/", views.toggle_bill_paid, name="toggle_bill_paid"), # This will route the URL for toggling the paid status of a bill to the toggle_bill_paid view, with the bill_id as a parameter
]