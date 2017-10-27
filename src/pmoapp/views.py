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
#import requests
import json
from rest_framework import permissions, viewsets
import threading
from .serializer import PlanSerializer,EvalPlanSerializer
from django.contrib.auth.decorators import login_required

class PlanViewSet(viewsets.ModelViewSet):
    lookup_field = 'plan_ID'
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class EvalPlanViewSet(viewsets.ModelViewSet):
    lookup_field = 'eval_planID'
    queryset = EvalPlan.objects.all()
    serializer_class = EvalPlanSerializer

def getJsonValueByAttributes():
    response = requests.get('http://127.0.0.1:8000/api/plan/plan_ID/')
    response_dict = response.json()
    #for result1 in range(0,len(response_dict)):
    #    print(response_dict[result1])
    threading.Timer(60.0, getJsonValueByAttributes).start()
    #set timer to call the api can change to value of 60 current set to 1 min

def login(request):
    getJsonValueByAttributes()
    return render(request, 'pmoapp/login.html', {})

def otp(request):
    #request.session['first_name'] = 'Benjamin'
    # print(request.session['first_name'])
    #print(request.user.first_name)
    return render(request, 'pmoapp/authotp.html', {})

def home(request):
    template = loader.get_template('pmoapp/home.html')
    updateTime = datetime.now()


    #curUsername = request.user
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
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

    #until we have session..
    curUsername = request.user

    planItem = Plan.objects.filter(plan_ID=plan_id).get()
    crisisItem = planItem.plan_crisisID
    updateItem = CrisisUpdates.objects.filter(updates_crisisID__crisis_ID=crisisItem.crisis_ID).latest('updates_datetime')

    curAccount = Account.objects.filter(username=curUsername).get() #in session or something
    curUserType = curAccount.user_type
    curUser = curAccount.name
    allAccounts = Account.objects.all()

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

    #test to see if there is a comment by this minister yet
    allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
    myComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)

    submittedUsers = []
    for c in allComments:
        submittedUsers.append(c.eval_userID.user_type)

    context = {
        'planItem': planItem,
        'allAccounts': allAccounts,
        'submittedUsers': submittedUsers,
        'crisisItem': crisisItem,
        'planID': planItem.plan_ID,
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curAccount.name),
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
        #'jsonCrisis1': JsonResponse(serializers.serialize(graphUpdateList)),
        'jsonComments': serializers.serialize('json', allComments),
        'allComments': allComments,
        'myComments': myComments,
        'updateItem': updateItem,
        'accountType': curUserType,
        'curUser': curUser,
        'curAccount': curAccount,
        'toDisplay': toDisplay,
        'planID': json.dumps(planItem.plan_ID)
    }
    return HttpResponse(template.render(context, request))

def saveComment(request):
    print(request)
    if request.POST:
        getPlanID = request.POST['planID']
        getAccType = request.POST['accType']
        getCommentTxt = request.POST['commentTxt']
        getHasComment = request.POST['hasComment']

        curAccount = Account.objects.filter(user_type=getAccType).get()
        curPlan = Plan.objects.filter(plan_ID=getPlanID).get()
        eval_entry = EvalPlan(eval_planID=curPlan, eval_userID=curAccount, eval_text=getCommentTxt, eval_hasComment=getHasComment)
        testDuplicate = EvalPlan.objects.filter(eval_planID__plan_ID=getPlanID, eval_userID__user_type=getAccType)

        if not testDuplicate:
            #print("testDuplicate is empty!") #save here
            eval_entry.save()
        else:
            #print("there is something here: " + testDuplicate[0].eval_text) #replace here
            testDuplicate[0].delete()
            eval_entry.save()
            #testNew = EvalPlan.objects.filter(eval_planID__plan_ID=getPlanID, eval_userID__user_type=getAccType).get()
            #print("New Text Saved: "+testNew.eval_text)
    return HttpResponse('')

def getComments(request, userType, plan_id):
    print(userType, plan_id)
    allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
    allUsers = Account.objects.all()

    diff = []
    for user in allUsers:
        found = False
        for comment in allComments:
            if(user.user_type==comment.eval_userID.user_type):
                found = True
                break
        if not found:
            diff.append(user.user_type)

    print(diff)

    context = {
        'noReviewYet': diff
    }
    return HttpResponse(json.dumps(context))

class commentUpdates(ListView):
    template_name = 'pmoapp/commentUpdates.html'
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