"""All Django views for pmoapp.
"""
from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'pmoapp/login.html', {})

def otp(request):
    return render(request, 'pmoapp/authotp.html', {})

def home(request):
    return render(request, 'pmoapp/home.html', {})

def report(request, crisis_id):
    #return HttpResponse('Crisis_ID: ' + str(crisis_id))
    context = {'crisis_id': crisis_id}
    return render(request, 'pmoapp/report.html', context)

def newsfeed(request):
    return render(request, 'pmoapp/newsfeed.html', {})

def history(request):
    return render(request, 'pmoapp/history.html', {})