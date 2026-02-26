from django.urls import path 
from . import views


# Define URL patterns for the budget app
urlpatterns = [
    path('', views.home, name='home'), # This will route the root URL of the budget app to the home view
]