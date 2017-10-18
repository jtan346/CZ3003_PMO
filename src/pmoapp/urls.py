from django.conf.urls import url, include
from django.contrib import admin
from views import *
from django.views.generic import TemplateView

urlpatterns = [ #pylint: disable=invalid-name
    url(r'^$', login, name='login'),
    url(r'^authotp$', otp, name='otp'),
    url(r'^home$', home, name='home'),
    url(r'^report/(?P<plan_id>[0-9]{8})$', report, name='report'),
    url(r'^newsfeed', newsfeed, name='newsfeed'),
    url(r'^history', history, name='history'),
    #url(r'^test', test, name='test'),
    url(r'^test/(?P<plan_id>[0-9]{8})$', test, name='test'),
    url(r'^crisisUpdates/(?P<slug>[\w-]+)/$', crisisUpdates.as_view()),
    url(r'^graphUpdates/(?P<slug>[\w-]+)/$', graphUpdates.as_view())
]
