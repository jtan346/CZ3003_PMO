"""All Django views for myapp.
"""
from django.shortcuts import render


def hello(request):
    """Example to handle request from clients."""
    return render(request, 'index.html', {})
