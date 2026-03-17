"""
URL configuration for budget_tracker project.

This file is the main traffic controller for the whole project. It decides
which app should handle each URL.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin site for managing data as an administrator.
    path('admin/', admin.site.urls),

    # Django's built-in authentication URLs provide login and logout views.
    path('accounts/', include('django.contrib.auth.urls')),

    # Send all remaining URLs to the budget app.
    path('', include('budget.urls')),
]
