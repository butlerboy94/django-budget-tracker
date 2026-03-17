"""
ASGI config for budget_tracker project.

This file is used when the project is served with an ASGI-compatible server.
ASGI is the newer web server standard that supports features like async work
and WebSockets.
"""

import os

from django.core.asgi import get_asgi_application

# Point Django to the settings file for this project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# `application` is the ASGI callable the server looks for when starting up.
application = get_asgi_application()
