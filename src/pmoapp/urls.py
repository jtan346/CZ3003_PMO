from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from views import *

from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'plan_ID',PlanViewSet)
router2 = routers.SimpleRouter()
router2.register(r'eval_planID',EvalPlanViewSet)

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
    url(r'^graphUpdates/(?P<slug>[\w-]+)/$', graphUpdates.as_view()),
    url(r'^api/plan/', include(router.urls)),
    # http://127.0.0.1:8000/api/plan/plan_ID/ the link to call the api from CMO side
    url(r'^api/eval/', include(router2.urls)),
    # http://127.0.0.1:8000/api/eval/eval_planID/ the link to call the api from CMO side
]
