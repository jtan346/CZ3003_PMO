from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [ #pylint: disable=invalid-name
    url(r'^$', login, name='login'),
    url(r'^authotp$', otp, name='otp'),
    url(r'^home$', home, name='home'),
    url(r'^report/(?P<crisis_id>[0-9]{8})$', report, name='report'),
    url(r'^newsfeed', newsfeed, name='newsfeed'),
    url(r'^history', history, name='history'),
    url(r'^testing', testinginsertdb)
]
