"""All Django views for pmoapp.
"""
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template import loader
from django.views.generic.list import ListView
from .models import *
from datetime import datetime
from django.core import serializers
import requests
import json
from rest_framework import permissions, viewsets
from .serializer import PlanSerializer,EvalPlanSerializer,TestSerializer ,CMOSerializer
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import warnings
# from django.contrib.auth.decorators import login_required
# import threading
# from django.core.serializers import serialize
# from django.core.serializers.json import DjangoJSONEncoder
# from django.db.models import Max
# #from django.test import Client
# import operator

class PlanViewSet(viewsets.ModelViewSet):
    lookup_field = 'plan_ID'
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class EvalPlanViewSet(viewsets.ModelViewSet):
    lookup_field = 'eval_planID'
    queryset = EvalPlan.objects.all()
    serializer_class = EvalPlanSerializer

class TestViewSet(viewsets.ModelViewSet):
    lookup_field = 'PlanID'
    queryset = testmyfuckingapi.objects.all()
    serializer_class = TestSerializer

class CMOViewSet(viewsets.ModelViewSet):
    lookup_field = 'planID'
    queryset = Notifications.objects.all()
    serializer_class = CMOSerializer

def startupInits():
    #initStorage()
    MyCMOApi()
    #initNotifications()

def initStorage():
    Plan.objects.all().delete()
    Crisis.objects.all().delete()
    SubCrisis.objects.all().delete()
    CrisisUpdates.objects.all().delete()
    print("Storage Reset and ready to receive CMO Data.")

def MyCMOApi():
    warnings.simplefilter("ignore", RuntimeWarning)
    #Delete all preextings?
    # Plan.objects.all().delete()
    # Crisis.objects.all().delete()
    # SubCrisis.objects.all().delete()
    CrisisUpdates.objects.all().delete()

    #response = requests.get('http://172.21.148.168/api/pmo/')
    #response_dict = response.json()

    # with urllib.request.urlopen('http://172.21.148.168/api/pmo/') as url:
    try:
        url = urllib.request.urlopen('http://172.21.148.168/api/pmo/', timeout=3)
        s = url.read()
        data = json.loads(s)

        #Crisis Model
        #Missing:
        # - crisis_description: Concat SubCrisis Description
        # - crisis_datetime: Earliest SubCrisis datetime
        # if(len(response_dict)>0):
        #     for i in range(0,len(response_dict)):
        if (len(data) > 0):
            for i in range(0, len(data)):
                # print(data[i]['id']) #OK
                # print(data[i]['status']) #OK

                crisis_id = data[i]['id']
                crisis_status = data[i]['status']
                crisis_name = data[i]['crisis_title']
                concatDescription = ""

                #SubCrisis Model
                #Missing: None. All accounted
                if(data[i]['crisisreport_set']):
                    for j in range(0, len(data[i]['crisisreport_set'])):
                        # print(data[i]['crisisreport_set'][j]['id'])  #sc_ID
                        # print(data[i]['crisisreport_set'][j]['description'])  #description
                        # print(data[i]['crisisreport_set'][j]['datetime'])  #datetime
                        # print(data[i]['crisisreport_set'][j]['latitude'])  #latitude
                        # print(data[i]['crisisreport_set'][j]['longitude'])  #longitude
                        # print(data[i]['crisisreport_set'][j]['radius'])  #radius
                        # print(data[i]['crisisreport_set'][j]['crisisType'])  #crisis_type

                        sc_id = data[i]['crisisreport_set'][j]['id']  # sc_ID
                        sc_description = data[i]['crisisreport_set'][j]['description']  # description
                        sc_datetime = data[i]['crisisreport_set'][j]['datetime']  # datetime TO FIX
                        sc_latitude = data[i]['crisisreport_set'][j]['latitude']  # latitude
                        sc_longitude = data[i]['crisisreport_set'][j]['longitude']  # longitude
                        sc_radius = data[i]['crisisreport_set'][j]['radius']  # radius
                        sc_type = data[i]['crisisreport_set'][j]['crisisType']  # crisis_type
                        concatDescription += "SubCrisis " + str(data[i]['crisisreport_set'][j]['id']) + ": " + str(data[i]['crisisreport_set'][j]['description']) + " \n"

                        #Add SubCrisis Here
                        newSubCrisis = SubCrisis(sc_ID=sc_id,crisis_ID=data[i]['id'], crisis_type=sc_type, latitude=sc_latitude, longitude=sc_longitude, radius=sc_radius,datetime=sc_datetime,description=sc_description)
                        #newSubCrisis.save()
                        testSubCrisis = SubCrisis.objects.filter(crisis_ID=data[i]['id'], sc_ID=sc_id)
                        if (testSubCrisis):
                            # print(testSubCrisis)
                            testSubCrisis.delete()
                            newSubCrisis.save()
                        else:
                            print(newSubCrisis)
                            newSubCrisis.save()
                else:
                    print("No SubCrisis for Crisis: " + str(crisis_id))

                #Add Crisis Description Here
                #crisis_datetime=data[i]['crisisreport_set'][0]['datetime'] << To FIX
                newCrisis = Crisis(crisis_ID=crisis_id, crisis_name=crisis_name, crisis_description=concatDescription, crisis_datetime=data[i]['crisisreport_set'][0]['datetime'],crisis_status=crisis_status)
                #newCrisis.save()
                testCrisis = Crisis.objects.filter(crisis_ID=crisis_id)
                if(testCrisis):
                    # print(testCrisis)
                    testCrisis.delete()
                    newCrisis.save()
                else:
                    print(newCrisis)
                    newCrisis.save()

                #Plan Model
                #Missing:
                # - plan_crisisID: data[i]['id']    Pseudo Foreign Key (Do a crisis.pk = crisis_ID)
                # - plan_receipt: current time of update
                # - plan_sendtime: ?? << sub with datetime.now() for now
                # - plan_SAFRecommended
                # - plan_SPFRecommended
                # - plan_SCDFRecommended
                # - plan_SAFMaximum
                # - plan_SPFMaximum
                # - plan_SCDFMaximum
                if(data[i]['actionplan_set']):
                    for k in range(0, len(data[i]['actionplan_set'])):
                        # print(data[i]['actionplan_set'][k]['id']) #plan_num *IMPORTANT
                        # print(data[i]['actionplan_set'][k]['plan_number']) #plan_ID *PK IMPORTANT
                        # print(data[i]['actionplan_set'][k]['description']) #plan_description
                        # print(data[i]['actionplan_set'][k]['status']) #plan_status: ENUM
                        # print(data[i]['actionplan_set'][k]['resolution_time']) #plan_projResolutionTime
                        # print(data[i]['actionplan_set'][k]['projected_casualties']) #plan_projCasualtyRate
                        # print(data[i]['actionplan_set'][k]['type']) #??

                        plan_id = data[i]['actionplan_set'][k]['id']  # plan_num *IMPORTANT
                        plan_num = data[i]['actionplan_set'][k]['plan_number']  # plan_ID *PK IMPORTANT
                        plan_description = data[i]['actionplan_set'][k]['description']  # plan_description
                        plan_status = data[i]['actionplan_set'][k]['status']  # plan_status: ENUM
                        plan_projtime = data[i]['actionplan_set'][k]['resolution_time']  # plan_projResolutionTime
                        plan_projcasualty = data[i]['actionplan_set'][k]['projected_casualties']  # plan_projCasualtyRate
                        plan_type = data[i]['actionplan_set'][k]['type']  # ??
                        plan_senttime = data[i]['actionplan_set'][k]['outgoing_time']

                        #buffer input
                        maxSAF = 0
                        maxSPF = 0
                        maxSCDF = 0
                        recSAF = 0
                        recSPF = 0
                        recSCDF = 0

                        if(data[i]['actionplan_set'][k]['forcedeployment_set']):
                            plan_forces = data[i]['actionplan_set'][k]['forcedeployment_set']
                            for force in plan_forces:
                                if(force['name'] == "SAF"):
                                    maxSAF = force['max']
                                    recSAF = force['recommended']
                                elif(force['name'] == "SPF"):
                                    maxSPF = force['max']
                                    recSPF = force['recommended']
                                elif (force['name'] == "SCDF"):
                                    maxSCDF = force['max']
                                    recSCDF = force['recommended']

                        #translate the status..
                        if(data[i]['actionplan_set'][k]['status'] == "PMOApproved"):
                            plan_status = "Approved"
                        #elif(data[i]['actionplan_set'][k]['status'] == "PMOApproved")

                        #plan_projResolutionTime=plan_projtime
                        newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_description=plan_description, plan_status=plan_status, plan_receipt=datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF)
                        #newPlan.save()
                        testPlan = Plan.objects.filter(plan_ID=plan_id)
                        if(testPlan):
                            # print(testPlan)
                            testPlan.delete()
                            newPlan.save()
                        else:
                            print(newPlan)
                            newPlan.save()
                else:
                    print("No Plan for Crisis: " + str(crisis_id))

                #CrisisUpdates Model
                #Missing:
                # - updates_crisisID:  data[i]['id']    Pseudo Foreign Key (Do a crisis.pk = crisis_ID)
                # - updates_curSAF
                # - updates_curSPF
                # - updates_curSCDF
                if(data[i]['efupdate_set']):
                    for l in range(0, len(data[i]['efupdate_set'])):
                        # print(data[i]['efupdate_set'][l]['datetime']) #updates_datetime
                        # print(data[i]['efupdate_set'][l]['affectedRadius'])#??
                        # print(data[i]['efupdate_set'][l]['totalInjured']) #updates_curInjuries
                        # print(data[i]['efupdate_set'][l]['totalDeaths']) #updates_curDeaths
                        # print(data[i]['efupdate_set'][l]['duration']) #??
                        # print(data[i]['efupdate_set'][l]['description'])#updates_description

                        stat_datetime = data[i]['efupdate_set'][l]['datetime']  # updates_datetime
                        stat_radius = data[i]['efupdate_set'][l]['affectedRadius']  # ??
                        stat_injured = data[i]['efupdate_set'][l]['totalInjured']  # updates_curInjuries
                        stat_deaths = data[i]['efupdate_set'][l]['totalDeaths']  # updates_curDeaths
                        stat_duration = data[i]['efupdate_set'][l]['duration']  # ??
                        stat_description = data[i]['efupdate_set'][l]['description']  #?? updates_description

                        # buffer input
                        curSAF = 0
                        curSPF = 0
                        curSCDF = 0

                        if (data[i]['efupdate_set'][l]['forceutilization_set']):
                            plan_forces = data[i]['efupdate_set'][l]['forceutilization_set']
                            for force in plan_forces:
                                if (force['name'] == "SAF"):
                                    curSAF = force['utilization']
                                elif (force['name'] == "SPF"):
                                    curSPF = force['utilization']
                                elif (force['name'] == "SCDF"):
                                    curSCDF = force['utilization']

                        #Fix: updates_datetime=stat_datetime
                        newStat = CrisisUpdates(updates_crisisID=crisis_id, updates_datetime=stat_datetime, updates_curInjuries=stat_injured, updates_curDeaths=stat_deaths, updates_curSAF=curSAF, updates_curSPF=curSPF, updates_curSCDF=curSCDF, updates_description=stat_description)
                        newStat.save()
                        #print(newStat)
                        # testStat = CrisisUpdates.filter(updates_crisisID=crisis_id, updates_datetime=stat_datetime)
                        # if(testStat):
                        #     testStat.delete()
                        #     newStat.save()
                        # else:
                        #     newStat.save()
                else:
                    print("No Statistics for Crisis: " + str(crisis_id))
        else:
            print("No Crisis/Data from CMO")
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
    # do something
        print('Reason: ', e.reason)
    else:
    # do something
        print('CMO Crisis Package Updated successfully!')

# def getJsonValueByAttributes():
#     response = requests.get('http://127.0.0.1:8000/api/plan/plan_ID/')
#     response_dict = response.json()
#     #for result1 in range(0,len(response_dict)):
#     #    print(response_dict[result1])
#     threading.Timer(60.0, getJsonValueByAttributes).start()
#     #set timer to call the api can change to value of 60 current set to 1 min

def login(request):
    return render(request, 'pmoapp/login.html', {})

def otp(request):
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    #Sessionstuff
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    loggedin = request.session['Loggedin'] = False
    curnumNotifications = Notifications.objects.count()
    request.session['NumNotifications'] = curnumNotifications
    #send_mail(subject, str(OTP), from_email, to_email, fail_silently=False)
    print(str(OTP))
    return render(request, 'pmoapp/authotp.html', {})

def resendOTP(request):
    del request.session['OTP']
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    send_mail(subject, str(OTP), from_email, to_email, fail_silently=False)
    print(str(OTP))
    return render(request, 'pmoapp/authotp.html', {})

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
            print("User logged in")
            return True
        else:
            print("User not logged in")
            return False
    else:
        print("Session not found")
        return False

#@user_passes_test(otp_check(requests), login_url='/authotp/')
def home(request):
    if not login_check(request.session):
        return redirect('/logout')
    MyCMOApi()
    template = loader.get_template('pmoapp/home.html')
#Process Account/Session
    updateTime = datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    accountType = curAccount.user_type
    profilePicture = curAccount.profilePicture

    if(curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name +" "+ request.user.first_name
    print(curUser)

#NOTE: WHEN TO PULL FROM CMO: ON EVERY PAGE LOAD, BECAUSE NOTIFICATION COME, CLICKING IT WILL REFRESH A PAGE!

    #Code to receive, process and insert into my database.

#Process Crisis/Plans
    crisisList = Crisis.objects.exclude(crisis_status='Resolved')
    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if plansInCrisis:
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if(plan.plan_ID > max.plan_ID):
                    max = plan
            toDisplay.append(max)

    #print(crisisList)

    context = {
        'toDisplay': toDisplay,
        'ongoingCrisis': crisisList,
        'updateTime': updateTime,
        'accountType': accountType,
        'curUser': curUser,
        # 'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curUser),
        'profilePicture': profilePicture,
    }
    return HttpResponse(template.render(context, request))

def history(request):
    if not login_check(request.session):
        return redirect('/logout')

    template = loader.get_template('pmoapp/history.html')

#Get user info

    updateTime = datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    accountType = curAccount.user_type
    profilePicture = curAccount.profilePicture

    if (curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name + " " + request.user.first_name

#Sidebar display list
    allPlans = Plan.objects.all()
    ongoingPlanList = []
    ongoingCrisisList = Crisis.objects.exclude(crisis_status='Resolved')
    toDisplay2 = []
    for index, crisis in enumerate(ongoingCrisisList):
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if(plansInCrisis):
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if (plan.plan_ID > max.plan_ID):
                    max = plan
                    ongoingPlanList.append(plansInCrisis[index-1])
            toDisplay2.append(max)

# Get all plans where Crisis status = Resolved
    historicalCrisisList = Crisis.objects.filter(crisis_status='Resolved')
    historicalPlanList = []
    for crisis in historicalCrisisList:
        for plan in allPlans:
            if (crisis.crisis_ID == plan.plan_crisisID):
                historicalPlanList.append(plan)

    # print("ongoing:")
    # for a in ongoingPlanList:
    #     print(a.id)
    # print("historical:")
    # for b in historicalPlanList:
    #     print(b.id)

    toDisplay = ongoingPlanList + historicalPlanList
    allCrisis = Crisis.objects.all()
    context = {
        'toDisplay': toDisplay,
        'toDisplay2': toDisplay2,
        'ongoingCrisis': ongoingCrisisList,
        'updateTime': updateTime,
        'allCrisis': allCrisis,
        'curUser': curUser,
        'profilePicture': profilePicture,
    }
    return HttpResponse(template.render(context, request))

def crisis(request, crisis_id):
    if not login_check(request.session):
        return redirect('/logout')

    template = loader.get_template('pmoapp/crisis.html')
    updateTime = datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    curUserType = curAccount.user_type
    allAccounts = Account.objects.all()
    profilePicture = curAccount.profilePicture
    decisionTable = curAccount.decisionTable

    if (curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name + " " + request.user.first_name
    print(curUser)

    #planItem = Plan.objects.filter(plan_ID=plan_id).get()
    crisisItem = Crisis.objects.filter(crisis_ID=crisis_id).get()
    updateItem = []
    planList=Plan.objects.filter(plan_crisisID=crisis_id)
    planItem = []
    plan_id = -1

    if(planList):
        #get max plan id for latest plan
        maxi = planList[0]
        for plan in planList:
            if (plan.plan_ID > maxi.plan_ID):
                maxi = plan

        planItem = maxi
        plan_id = maxi.plan_ID


    if CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID):
        updateItem = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID).latest('updates_datetime')
    else:
        baseUpdate = CrisisUpdates(updates_crisisID=crisisItem.crisis_ID, updates_datetime=updateTime, updates_curInjuries = 0, updates_curDeaths = 0, updates_curSAF = 0, updates_curSPF = 0, updates_curSCDF = 0)
        baseUpdate.save()

    crisisList = Crisis.objects.exclude(crisis_status='Resolved')

    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if(plansInCrisis):
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if(plan.plan_ID > max.plan_ID):
                    max = plan
            toDisplay.append(max)

    graphUpdateList = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)

    #test to see if there is a comment by this minister yet

    if(plan_id != -1):
        allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
        myComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)

        submittedUsers = []
        for c in allComments:
            submittedUsers.append(c.eval_userID.user_type)
    else:
        allComments = []
        myComments = []
        submittedUsers = False

    allSubCrisis = []
    if SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID):
        allSubCrisis = SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID)

    #Approval package:

    myAgencies = ExternalAgency.objects.filter(agency_approver__user_type=curUserType)

    context = {
        'planItem': planItem,
        'profilePicture': profilePicture,
        'decisionTable': decisionTable,
        'ongoingCrisis': crisisList,
        'allAccounts': allAccounts,
        'submittedUsers': submittedUsers,
        'crisisItem': crisisItem,
        'plan_ID': plan_id,
        'allSubCrisis': allSubCrisis,
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'crisis_ID': crisis_id,
        'curName': json.dumps(curUser),
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
        'planID': json.dumps(plan_id),
        'myAgencies': serializers.serialize('json', myAgencies),
    }
    return HttpResponse(template.render(context, request))


def report(request, plan_id):
    if not login_check(request.session):
        return redirect('/logout')

    template = loader.get_template('pmoapp/report.html')
    updateTime = datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    curUserType = curAccount.user_type
    allAccounts = Account.objects.all()
    profilePicture = curAccount.profilePicture
    decisionTable = curAccount.decisionTable

    if (curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name + " " + request.user.first_name
    print(curUser)

    planItem = Plan.objects.filter(plan_ID=plan_id).get()
    crisisItem = Crisis.objects.filter(crisis_ID=planItem.plan_crisisID).get()
    updateItem = []
    if CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID):
        updateItem = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID).latest('updates_datetime')
    else:
        baseUpdate = CrisisUpdates(updates_crisisID=crisisItem.crisis_ID, updates_datetime=updateTime,
                                   updates_curInjuries=0, updates_curDeaths=0, updates_curSAF=0, updates_curSPF=0,
                                   updates_curSCDF=0)
        baseUpdate.save()
    # newAccount = Account(username="benji", password="12345", emailAddress="benjamintanjb@gmail.com", user_type="PM")
    # newAccount.save()
    print(updateItem)

    crisisList = Crisis.objects.exclude(crisis_status='Resolved')
    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if (plansInCrisis):
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if (plan.plan_ID > max.plan_ID):
                    max = plan
            toDisplay.append(max)

    graphUpdateList = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)

    # test to see if there is a comment by this minister yet
    allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
    myComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)

    submittedUsers = []
    for c in allComments:
        submittedUsers.append(c.eval_userID.user_type)

    allSubCrisis = []
    if SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID):
        allSubCrisis = SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID)

    # Approval package:

    myAgencies = ExternalAgency.objects.filter(agency_approver__user_type=curUserType)

    context = {
        'planItem': planItem,
        'profilePicture': profilePicture,
        'decisionTable': decisionTable,
        'ongoingCrisis': crisisList,
        'allAccounts': allAccounts,
        'submittedUsers': submittedUsers,
        'crisisItem': crisisItem,
        'planID': planItem.plan_ID,
        'allSubCrisis': allSubCrisis,
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curUser),
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
        # 'jsonCrisis1': JsonResponse(serializers.serialize(graphUpdateList)),
        'jsonComments': serializers.serialize('json', allComments),
        'allComments': allComments,
        'myComments': myComments,
        'updateItem': updateItem,
        'accountType': curUserType,
        'curUser': curUser,
        'curAccount': curAccount,
        'toDisplay': toDisplay,
        'planID': json.dumps(planItem.plan_ID),
        'myAgencies': serializers.serialize('json', myAgencies),
    }
    return HttpResponse(template.render(context, request))


def sendReport(request):
    if request.POST:
        curPlanID = request.POST['planID']
        #1. Comments

        allComments = EvalPlan.objects.filter(eval_planID=curPlanID) #Will return 5 objects

        concatComments = ""
        if(allComments):
            for n in allComments:
                concatComments += str(n.eval_userID.user_type) + ": " + str(n.eval_text) + " <br> "

        #2. Status

        reportStatus = True
        for n in allComments:
            if(n.eval_hasComment):
                reportStatus = False

        #Change http when we have

        r = requests.post('http://172.21.148.168/api/auth/', data={
            'PlanID': curPlanID,
            'Comments': concatComments,
            'PlanStatus': reportStatus
        })

        print(r.status_code)

        print(curPlanID)
        print(concatComments)
        print(reportStatus)

        #Change the status of report to pending cmo fortesting
        if(reportStatus == True):
            Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Approved")
            Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.now())
        else:
            Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Pending CMO")
            Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.now())

    return HttpResponse('')

def saveComment(request):
    print(request)
    if request.POST:
        getPlanID = request.POST['planID']
        getAccType = request.POST['accType']
        getCommentTxt = request.POST['commentTxt']
        getHasComment = request.POST['hasComment']
        getMyApprovals = request.POST.getlist('myApprovals[]')

        print(getMyApprovals)

        curAccount = Account.objects.filter(user_type=getAccType).get()
        curPlan = Plan.objects.filter(plan_ID=getPlanID).get()
        eval_entry = EvalPlan(eval_planID=curPlan, eval_userID=curAccount, eval_text=getCommentTxt, eval_hasComment=getHasComment)
        testDuplicate = EvalPlan.objects.filter(eval_planID__plan_ID=getPlanID, eval_userID__user_type=getAccType)

        if not testDuplicate:
            eval_entry.save()
        else:
            testDuplicate[0].delete()
            eval_entry.save()
    return HttpResponse('')

def getComments(request, userType, plan_id):
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
        updateItem = []
        if(CrisisUpdates.objects.filter(updates_crisisID=find_id)):
            updateItem = CrisisUpdates.objects.filter(updates_crisisID=find_id).latest('updates_datetime')
        return updateItem

class graphUpdates(ListView):
    template_name='pmoapp/graphUpdates.html'
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
    template_name = 'pmoapp/notificationBell.html'
    def get_queryset(self):
        curNotifications = Notifications.objects.all()
        return curNotifications

    def get_context_data(self, **kwargs):
        # for key in self.request.session.keys():
        #     print key

        curNotifications1 = Notifications.objects.all()
        curCount = curNotifications1.count()
        sessionNotiCount = self.request.session['NumNotifications']

        #Session: User's total read noti
        #From db: Total noti

        # print "User read:"
        # print sessionNotiCount

        leftNotiCount = curNotifications1.count()-sessionNotiCount

        # print "From DB"
        # print curCount
        #
        # print "Bell no. of new:"
        # print leftNotiCount

        context = {
            'sessionNotiCount': sessionNotiCount, #No. of User's Currently Read Notifications
            'outstandingCount': leftNotiCount,  #No. of new notifications shown on bell
            'curNotification': curNotifications1,   #All current notifications
            'curNotificationsJson': serializers.serialize('json', curNotifications1), #All current notifications in JSON
        }
        return context


def updateNotiCount(request):
    # if not request.is_ajax() or not request.method == 'POST':
    #     return HttpResponseNotAllowed(['POST'])

    curNotifications = Notifications.objects.all()
    curNotiCount = curNotifications.count()
    request.session['NumNotifications'] = curNotiCount
    print(request.session['NumNotifications'])
    return HttpResponse('')


def newsfeed(request):
    if not login_check(request.session):
        return redirect('/logout')
    template=loader.get_template('pmoapp/newsfeed.html')

    updateTime = datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    accountType = curAccount.user_type
    profilePicture = curAccount.profilePicture

    if (curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name + " " + request.user.first_name
    print(curUser)

    # NOTE: WHEN TO PULL FROM CMO: ON EVERY PAGE LOAD, BECAUSE NOTIFICATION COME, CLICKING IT WILL REFRESH A PAGE!

    # Process Crisis/Plans
    crisisList = Crisis.objects.exclude(crisis_status='Resolved')
    print(crisisList)

    toDisplay = []
    for crisis in crisisList:
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if (plansInCrisis):
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if (plan.plan_ID > max.plan_ID):
                    max = plan
            toDisplay.append(max)

    print(toDisplay)

    context = {
        'toDisplay': toDisplay,
        'ongoingCrisis': crisisList,
        'updateTime': updateTime,
        'accountType': accountType,
        'curUser': curUser,
        'profilePicture': profilePicture,
        # 'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curUser)
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