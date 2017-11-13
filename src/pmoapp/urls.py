from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from pmoapp.views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers

urlpatterns = [ #pylint: disable=invalid-name
    url(r'^api/cmoapi/', CMOApi), #doublucheck
    url(r'^$', auth_views.login, {'template_name': 'pmoapp/LoginGUI/login.html'}, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'pmoapp/LoginGUI/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout2/$', logout, name='logout2'),
    url(r'^otplogout', otplogout, name='otplogout'),
    url(r'^authotp/$', otp, name='otp'),
    url(r'^otpAuthentication/$', otpAuthentication, name='otpAuthentication'),
    url(r'^resendOTP/$', resendOTP, name='resendOTP'),
    url(r'^home/$', home, name='home'),
    url(r'^crisis/(?P<crisis_id>[\w-]+)/$', crisis, name='report'),
    url(r'^report/(?P<plan_id>[\w-]+)/$', report, name='report'),
    url(r'^newsfeed', newsfeed, name='newsfeed'),
    url(r'^notificationBell', notificationBellUpdate.as_view(), name='notificationBell'),
    url(r'^history', history, name='history'),
    url(r'^crisisUpdates/(?P<slug>[\w-]+)/$', crisisUpdates.as_view()), #slug=crisisID
    url(r'^graphUpdates/(?P<slug>[\w-]+)/$', graphUpdates.as_view()),
    url(r'^commentUpdates/(?P<slug>[\w-]+)/$', commentUpdates.as_view()),
    url(r'^saveComments/',saveComment),
    url(r'^updateNotiCount/',updateNotiCount),
    url(r'^sendReport/',sendReport),
    url(r'^getComments/(?P<userType>[\w-]+)/(?P<plan_id>[\w-]+)/$', getComments),
]

#pseudo startup-class
startupInitializer()

