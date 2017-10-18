"""All Django views for pmoapp.
"""
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic.list import ListView
from .models import *
from datetime import datetime
import json
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Max
#from django.test import Client
import operator

def login(request):
    return render(request, 'pmoapp/login.html', {})

def otp(request):
    return render(request, 'pmoapp/authotp.html', {})

def home(request):
    template = loader.get_template('pmoapp/home.html')
    updateTime = datetime.now()

    curAccount = Account.objects.filter(user_type='MDEF').get()  # in session or something
    accountType = curAccount.user_type
    curUser = curAccount.name

    crisisList = Crisis.objects.filter(crisis_status='Ongoing').order_by('-crisis_ID')
    planList = Plan.objects.filter(plan_crisisID__crisis_status='Ongoing')
    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = planList.filter(plan_crisisID__crisis_ID=crisis.crisis_ID)
        max = plansInCrisis[0]
        for plan in plansInCrisis:
            if(plan.plan_ID > max.plan_ID ): max = plan
        toDisplay.append(max)

    context = {
        'toDisplay': toDisplay,
        'updateTime':updateTime,
        'accountType': accountType,
        'curUser': curUser,
        # 'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curAccount.name)
    }
    return HttpResponse(template.render(context, request))

def history(request):
    template = loader.get_template('pmoapp/history.html')

    crisisOngoingList = Crisis.objects.filter(crisis_status='Ongoing').order_by('-crisis_ID')
    planOngoingList = Plan.objects.filter(plan_crisisID__crisis_status='Ongoing')

    planResolvedList = Plan.objects.exclude(plan_crisisID__crisis_status='Ongoing')
    toDisplay = []
    updateTime = datetime.now()

    crisisList = Crisis.objects.filter(crisis_status='Ongoing').order_by('-crisis_ID')
    planList = Plan.objects.filter(plan_crisisID__crisis_status='Ongoing')
    toDisplay2 = []
    for crisis in crisisList:
        plansInCrisis = planList.filter(plan_crisisID__crisis_ID=crisis.crisis_ID)
        max = plansInCrisis[0]
        for plan in plansInCrisis:
            if (plan.plan_ID > max.plan_ID): max = plan
        toDisplay2.append(max)

    curAccount = Account.objects.filter(user_type='MDEF').get()  # in session or something
    accountType = curAccount.user_type
    curUser = curAccount.name

    for plan in planResolvedList:
        toDisplay.append(plan)

    for crisis in crisisOngoingList:
        plansInCrisis = planOngoingList.filter(plan_crisisID__crisis_ID=crisis.crisis_ID)
        max = plansInCrisis[0]
        for plan in plansInCrisis:
            if (plan.plan_ID > max.plan_ID): max = plan
        for plan in plansInCrisis:
            if(plan != max): toDisplay.append(plan)

    context = {
        'toDisplay': toDisplay,
        'toDisplay2': toDisplay2,
        'updateTime': updateTime,
    }
    return HttpResponse(template.render(context, request))

def report(request, plan_id):
    template = loader.get_template('pmoapp/report.html')

    planItem = Plan.objects.filter(plan_ID=plan_id).get()
    crisisItem = planItem.plan_crisisID
    updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=crisisItem.crisis_ID).latest('updates_datetime')

    curAccount = Account.objects.filter(user_type='MDEF').get() #in session or something
    accountType = curAccount.user_type
    curUser = curAccount.name

    crisisList = Crisis.objects.filter(crisis_status='Ongoing').order_by('-crisis_ID')
    planList = Plan.objects.filter(plan_crisisID__crisis_status='Ongoing')
    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = planList.filter(plan_crisisID__crisis_ID=crisis.crisis_ID)
        max = plansInCrisis[0]
        for plan in plansInCrisis:
            if (plan.plan_ID > max.plan_ID): max = plan
        toDisplay.append(max)

    graphUpdateList = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=crisisItem.crisis_ID)

    context = {
        'planItem': planItem,
        'crisisItem': crisisItem,
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curAccount.name),
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
        # 'jsonCrisis1': JsonResponse(serializers.serialize(graphUpdateList)),
        'updateItem': updateItem,
        'accountType': accountType,
        'curUser': curUser,
        'toDisplay': toDisplay
    }
    return HttpResponse(template.render(context, request))

class crisisUpdates(ListView):
    template_name = 'pmoapp/crisisUpdates.html'
    findID=""
    def get_queryset(self):
        find_id = self.kwargs['slug']
        updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=find_id).latest('updates_datetime')
        return updateItem

class graphUpdates(ListView):
    template_name='pmoapp/graphUpdates.html'
    find_id=""
    def get_queryset(self):
        find_id = self.kwargs['slug']
        updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=find_id)
        return updateItem

    def get_context_data(self, **kwargs):
        find_id = self.kwargs['slug']
        updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=find_id)
        context = {
            'jsonCrisis1': serializers.serialize('json', updateItem)
        }
        return context


def newsfeed(request):
    template=loader.get_template('pmoapp/newsfeed.html')

    crisisList = Crisis.objects.filter(crisis_status='Ongoing').order_by('-crisis_ID')
    planList = Plan.objects.filter(plan_crisisID__crisis_status='Ongoing')
    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = planList.filter(plan_crisisID__crisis_ID=crisis.crisis_ID)
        max = plansInCrisis[0]
        for plan in plansInCrisis:
            if (plan.plan_ID > max.plan_ID): max = plan
        toDisplay.append(max)

    context = {
        "toDisplay": toDisplay
    }
    return HttpResponse(template.render(context, request))

#def testinginsertdb(Request):
    #newAccount = Account(username="benji", password="12345", emailAddress="benjamintanjb@gmail.com", user_type="PM")
    #newAccount.save()
    #return HttpResponse("IT SAVED " + str(newAccount.username))

def test(request, plan_id):
    template = loader.get_template('pmoapp/test.html')

    planItem = Plan.objects.filter(plan_ID=plan_id).get()
    crisisItem = planItem.plan_crisisID
    crisisItem2 = planItem.plan_crisisID.crisis_ID

    # d1 = planItem.plan_projResolutionTime
    # d2 = crisisItem.crisis_dateTime
    # FMT = '%H:%M:%S'
    # tdelta = datetime.strptime(d1, FMT) - datetime.strptime(d2, FMT)

    updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=crisisItem2).latest('updates_datetime')
    graphUpdateList = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=crisisItem.crisis_ID)

    # for item in planItem:
    #     planCrisisID = item.plan_crisisID

    context = {
        'planItem': planItem,
        'crisisItem': crisisItem,
        'crisisItem2': crisisItem2,
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
        'updateItem': updateItem,
        # 'tdelta': tdelta
    }
    return HttpResponse(template.render(context, request))