"""pmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
# from rest_framework import routers
#
#
# router = routers.SimpleRouter()
# router.register(r'plan_ID',PlanViewSet)
# router2 = routers.SimpleRouter()
# router2.register(r'eval_planID',EvalPlanViewSet)

urlpatterns = [ # pylint: disable=invalid-name
    url(r'^admin/', admin.site.urls),
    url(r'^/', include('pmoapp.urls')),
    url(r'^', include('pmoapp.urls')),
]

#     url(r'^api/plan/', include(router.urls)),
#     # http://127.0.0.1:8000/api/plan/plan_ID/ the link to call the api from CMO side
#     url(r'^api/eval/', include(router2.urls)),
#     # http://127.0.0.1:8000/api/eval/eval_planID/ the link to call the api from CMO side
#]
