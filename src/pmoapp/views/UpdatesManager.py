from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.generic.list import ListView
from pmoapp.models import *
from django.core import serializers
from pmoapp.serializer import *
from pmoapp.views import *

class commentUpdates(ListView):
    template_name = 'pmoapp/CrisisGUI/commentUpdates.html'
    find_id = ""

    def get_queryset(self):
        dataRec = self.kwargs['slug']
        data2 = dataRec.replace('-', ' ').split(' ')
        updateItem = Account.objects.filter(user_type=data2[0]).get()
        return updateItem
    def get_context_data(self, **kwargs):
        dataRec = self.kwargs['slug']
        data2 = dataRec.replace('-', ' ').split(' ')
        curUser = Account.objects.filter(user_type=data2[0]).get()
        curPlan = Plan.objects.filter(plan_ID=data2[1]).get()
        allComments = EvalPlan.objects.filter(eval_planID__plan_ID=data2[1])
        allAccounts = Account.objects.all()
        submittedUsers = []
        for c in allComments:
            submittedUsers.append(c.eval_userID.user_type)
        hasComments = []
        for c in allComments:
            if c.eval_hasComment:
                hasComments.append(c.eval_userID.user_type)
        context = {
            'currentPlan': curPlan,
            'currentUser': curUser,
            'allComments': allComments,
            'hasComments': hasComments,
            'allAccounts': allAccounts,
            'submittedUsers': submittedUsers,
        }
        return context

class crisisUpdates(ListView):
    template_name = 'pmoapp/CrisisGUI/crisisUpdates.html'
    findID=""
    def get_queryset(self):
        find_id = self.kwargs['slug']
        updateItem = []
        if(CrisisUpdates.objects.filter(updates_crisisID=find_id)):
            updateItem = CrisisUpdates.objects.filter(updates_crisisID=find_id).latest('updates_datetime')
        return updateItem
    def get_context_data(self, **kwargs):
        find_id = self.kwargs['slug']
        allUpdates = CrisisUpdates.objects.filter(updates_crisisID=find_id)
        updateItem = []
        if (CrisisUpdates.objects.filter(updates_crisisID=find_id)):
            updateItem = CrisisUpdates.objects.filter(updates_crisisID=find_id).latest('updates_datetime')
        context = {
            'allUpdates': allUpdates,
            'updateItem': updateItem
        }
        return context

class graphUpdates(ListView):
    template_name='pmoapp/CrisisGUI/graphUpdates.html'
    find_id=""
    def get_queryset(self):
        find_id = self.kwargs['slug']
        updateItem = CrisisUpdates.objects.filter(updates_crisisID=find_id)
        return updateItem
    def get_context_data(self, **kwargs):
        find_id = self.kwargs['slug']
        updateItem = CrisisUpdates.objects.filter(updates_crisisID=find_id)
        context = {
            'jsonCrisis1': serializers.serialize('json', updateItem)
        }
        return context

class notificationBellUpdate(ListView):
    template_name = 'pmoapp/HomeGUI/notificationBell.html'
    def get_queryset(self):
        lastfive = Notifications.objects.all().order_by('-id')[:5]
        lastfive1 = reversed(lastfive)
        return lastfive1

    def get_context_data(self, **kwargs):
       #if have notifications
        if(Notifications.objects.all()):
            curNotifications1 = Notifications.objects.all()
            curCount = curNotifications1.count()
            lastfive = Notifications.objects.all().order_by('-id')[:5]
            lastfive1 = reversed(lastfive)
        else:
            curCount = 0
            lastfive1 = []
            curNotifications1 = []

        sessionNotiCount = self.request.session['NumNotifications']
        leftNotiCount = curCount-sessionNotiCount

        context = {
            'sessionNotiCount': sessionNotiCount, #No. of User's Currently Read Notifications
            'outstandingCount': leftNotiCount,  #No. of new notifications shown on bell
            'curNotification': lastfive1,   #All current notifications
        }
        return context

def updateNotiCount(request):
    curNotifications = Notifications.objects.all()
    curNotiCount = curNotifications.count()
    request.session['NumNotifications'] = curNotiCount
    print(request.session['NumNotifications'])
    return HttpResponse('')