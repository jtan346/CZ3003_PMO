#!/usr/bin/env python
"""Script to run Django server.

Some useful commands:
  python manage.py runserver
  python manage.py createsuperuser
  python manage.py makemigrations
  python manage.py showmigrations
  python manage.py migrate
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmo.dev_settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # pylint: disable=unused-import
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?")
        raise
    execute_from_command_line(sys.argv)
