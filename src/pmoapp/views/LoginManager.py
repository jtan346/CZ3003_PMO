from django.shortcuts import render
from django.http import HttpResponse
from pmoapp.models import *
from pmoapp.serializer import *
from pmoapp.views import *
from random import randint
from django.conf import settings
from django.core.mail import send_mail

def login(request):
    return render(request, 'pmoapp/LoginGUI/login.html', {})

def logout(request):
    return render(request, 'pmoapp/LoginGUI/logout.html', {})

def otplogout(request):
    return render(request, 'pmoapp/LoginGUI/otplogout.html', {})

def otp(request):
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    #Sessionstuff
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    loggedin = request.session['Loggedin'] = False
    curnumNotifications = Notifications.objects.count()
    request.session['NumNotifications'] = curnumNotifications
    email_text = str(request.user) + ": " +str(OTP)
    send_mail(subject, email_text, from_email, to_email, fail_silently=False)
    print(str(OTP))
    return render(request, 'pmoapp/LoginGUI/authotp.html', {})

def resendOTP(request):
    del request.session['OTP']
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    email_text = str(request.user) + ": " + str(OTP)
    send_mail(subject, email_text, from_email, to_email, fail_silently=False)
    return render(request, 'pmoapp/LoginGUI/authotp.html', {})

def otpAuthentication(request):
    if request.POST:
        otp = request.POST['otp']
        if (otp == str(request.session['OTP'])):
            del request.session['OTP']
            request.session['Loggedin'] = True
            return HttpResponse('')
    return HttpResponse('', status=401)

def login_check(session):
    if 'Loggedin' in session:
        if session['Loggedin'] == True:
            #print("User logged in")
            return True
        else:
            #print("User not logged in")
            return False
    else:
        #print("Session not found")
        return False