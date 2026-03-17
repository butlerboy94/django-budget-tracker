#!/usr/bin/env python
"""Entry point for running Django management commands from the terminal."""
import os
import sys


def main():
    """Set the Django settings module and pass command-line work to Django."""
    # This tells Django which settings file to use when commands like
    # `runserver`, `migrate`, or `createsuperuser` are executed.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
    try:
        # Import Django's command runner only after the settings module is set.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django cannot be imported, this error message gives a beginner a
        # helpful hint about common setup problems.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Pass whatever command the user typed to Django.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
