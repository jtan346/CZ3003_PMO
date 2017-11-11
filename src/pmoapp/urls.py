from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from pmoapp.views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'plan_ID',PlanViewSet)
router2 = routers.SimpleRouter()
router2.register(r'eval_planID',EvalPlanViewSet)
router3 = routers.SimpleRouter()
router3.register(r'PlanID',TestViewSet)
router4 = routers.SimpleRouter()
router4.register(r'planID',CMOViewSet)

urlpatterns = [ #pylint: disable=invalid-name
    #url(r'^$', login, name='login'),
    url(r'^$', auth_views.login, {'template_name': 'pmoapp/login.html'}, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'pmoapp/login.html'}, name='login'),
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
    #url(r'^test', test, name='test'),
    url(r'^test/(?P<plan_id>[0-9]{8})$', test, name='test'),
    url(r'^crisisUpdates/(?P<slug>[\w-]+)/$', crisisUpdates.as_view()), #slug=crisisID
    url(r'^graphUpdates/(?P<slug>[\w-]+)/$', graphUpdates.as_view()),
    url(r'^commentUpdates/(?P<slug>[\w-]+)/$', commentUpdates.as_view()),
    url(r'^api/plan/', include(router.urls)),
    # http://127.0.0.1:8000/api/plan/plan_ID/ the link to call the api from CMO side
    url(r'^api/eval/', include(router2.urls)),
    # http://127.0.0.1:8000/api/eval/eval_planID/ the link to call the api from CMO side
    url(r'^api/test/', include(router3.urls)),
    # http://127.0.0.1:8000/api/test/PlanID/ the link to test the api from CMO side
    url(r'^api/cmo/', include(router4.urls)),
    # http://127.0.0.1:8000/api/cmo/planID/ the link to test the api from CMO side
    url(r'^saveComments/',saveComment),
    url(r'^updateNotiCount/',updateNotiCount),
    url(r'^sendReport/',sendReport),
    url(r'^getComments/(?P<userType>[\w-]+)/(?P<plan_id>[\w-]+)/$', getComments),

    #url(r'^admin/', admin.site.urls),

]

#pseudo startup-class
startupInits()

