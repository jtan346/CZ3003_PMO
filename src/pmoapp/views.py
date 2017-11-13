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
from rest_framework import permissions, viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializer import *
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import warnings
import datetime

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def CMOApi(Request):
    if(Request.method == "POST"):
        serializer = CMOSerializer(data=Request.data)
        print(serializers)
        print(Request.data)
        if(serializer.is_valid()):
            rawData=serializer.data
            incData = Notifications(PlanNum=rawData['PlanNum'], PlanID=rawData['PlanID'], CrisisID=rawData['CrisisID'], CrisisTitle=rawData['CrisisTitle'], DateTime=rawData['DateTime'])
            incData.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status.HTTP_400_BAD_REQUEST)

def startupInitializer():
    initStorage()
    MyCMOApi()
    initNotifications()
    print("startupInits")

def initStorage():
    Plan.objects.all().delete()
    Crisis.objects.all().delete()
    SubCrisis.objects.all().delete()
    CrisisUpdates.objects.all().delete()
    print("Storage Reset and ready to receive CMO Data.")

def initNotifications():
    Notifications.objects.all().delete()
    #save all current plans in notification db
    plans = Plan.objects.all()
    if(plans):
        for plan in plans:
            crisis = Crisis.objects.filter(crisis_ID=plan.plan_crisisID).get()
            newNoti = Notifications(PlanNum=plan.plan_num, PlanID=plan.plan_ID, CrisisID=crisis.crisis_ID, CrisisTitle=crisis.crisis_name, DateTime=plan.plan_sendtime)
            newNoti.save()
    noti = Notifications.objects.all()
    print("initNotifications: There are currently " + str(noti.count()) + " Notifications")

def CMOListener():
    #If numNotifications > numPlans (ongoing), means CMO post me something
    curPlans = Plan.objects.all()
    curNotis = Notifications.objects.all()

    if(curNotis.count() > curPlans.count()):
        #call mycmoapi to pull new plan into db
        MyCMOApi()
        print("CMOListener activated")
    else:
        print("CMOListener not activated. No. of Plans (" + str(curPlans.count()) + "), No. of Notifications ("+str(curNotis.count())+")")

def MyCMOApi():
    warnings.simplefilter("ignore", RuntimeWarning)
    # Delete all preextings
    # Plan.objects.all().delete()
    # Crisis.objects.all().delete()
    # SubCrisis.objects.all().delete()
    CrisisUpdates.objects.all().delete()

    #MyCMOAPI is manually parsed to account for data integrity and manual translations of several parts of code.
    #This is because the ORM structure of the DB is very strict and a buffer, or wrapper, is needed (i.e. Provisional)

    try:
        url = urllib.request.urlopen('http://172.21.148.168/api/pmo/', timeout=5)
        s = url.read()
        data = json.loads(s.decode('utf-8'))

        #Crisis Model
        #Missing: None. All accounted
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
                        sc_id = data[i]['crisisreport_set'][j]['id']  # sc_ID
                        sc_description = data[i]['crisisreport_set'][j]['description']  # description
                        sc_datetime = data[i]['crisisreport_set'][j]['datetime']  # datetime TO FIX
                        sc_latitude = data[i]['crisisreport_set'][j]['latitude']  # latitude
                        sc_longitude = data[i]['crisisreport_set'][j]['longitude']  # longitude
                        sc_radius = data[i]['crisisreport_set'][j]['radius']  # radius
                        sc_type = data[i]['crisisreport_set'][j]['crisisType']  # crisis_type
                        concatDescription += "SubCrisis " + str(data[i]['crisisreport_set'][j]['id']) + ": " + str(data[i]['crisisreport_set'][j]['description']) + " \n"

                        newSubCrisis = SubCrisis(sc_ID=sc_id,crisis_ID=data[i]['id'], crisis_type=sc_type, latitude=sc_latitude, longitude=sc_longitude, radius=sc_radius,datetime=sc_datetime,description=sc_description)
                        testSubCrisis = SubCrisis.objects.filter(crisis_ID=data[i]['id'], sc_ID=sc_id)
                        if not testSubCrisis:
                            newSubCrisis.save()
                        else:
                            print("SubCrisis already exists.")
                else:
                    print("No SubCrisis for Crisis: " + str(crisis_id))

                #Add Crisis Description Here
                newCrisis = Crisis(crisis_ID=crisis_id, crisis_name=crisis_name, crisis_description=concatDescription, crisis_datetime=data[i]['crisisreport_set'][0]['datetime'],crisis_status=crisis_status)
                testCrisis = Crisis.objects.filter(crisis_ID=crisis_id)
                if not testCrisis:
                    newCrisis.save()
                else:
                    print("Crisis already exists.")

                #Plan Model
                #Missing: None. All accounted
                if(data[i]['actionplan_set']):
                    for k in range(0, len(data[i]['actionplan_set'])):
                        plan_id = data[i]['actionplan_set'][k]['id']  # plan_num *IMPORTANT
                        plan_num = data[i]['actionplan_set'][k]['plan_number']  # plan_ID *PK IMPORTANT
                        plan_description = data[i]['actionplan_set'][k]['description']  # plan_description
                        #plan_status = data[i]['actionplan_set'][k]['status']  # plan_status: Needs Translation
                        plan_projtime = data[i]['actionplan_set'][k]['resolution_time']  # plan_projResolutionTime
                        plan_projcasualty = data[i]['actionplan_set'][k]['projected_casualties']  # plan_projCasualtyRate
                        plan_type = data[i]['actionplan_set'][k]['type']  # included
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

                        #translate the status.. awaitingPMOapproval, rejected (reject by cmo and pmo) and pmoapproval
                        if(data[i]['actionplan_set'][k]['status'] == "PMOApproved"):
                            plan_status = "Approved"
                            if (data[i]['actionplan_set'][k]['comment']):
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=data[i]['actionplan_set'][k]['comment']['text'])
                            else:
                                fillercomment = "No comments for: Crisis " + str(crisis_id) + " - Plan " + str(plan_num)
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=fillercomment)
                            testPlan = Plan.objects.filter(plan_ID=plan_id)
                            if not testPlan:
                                newPlan.save()
                                print("Plan saved: " + str(plan_id) + " " + str(plan_status))
                            else:
                                print("Plan already exists")

                        elif(data[i]['actionplan_set'][k]['status'] == "PMORequest"):
                            plan_status = "Pending PMO"
                            if (data[i]['actionplan_set'][k]['comment']):
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=data[i]['actionplan_set'][k]['comment']['text'])
                            else:
                                fillercomment = "No comments for: Crisis " + str(crisis_id) + " - Plan " + str(plan_num)
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=fillercomment)
                            testPlan = Plan.objects.filter(plan_ID=plan_id)
                            if not testPlan:
                                newPlan.save()
                                print("Plan saved: " + str(plan_id) + " " + str(plan_status))
                            else:
                                print("Plan already exists")

                        elif data[i]['actionplan_set'][k]['status'] == "Rejected":
                            #Rejected validation done at CMO Side and data[i]['actionplan_set'][k]['author'] == "PMO"
                            #I rejected
                            plan_status = "Pending CMO"
                            if (data[i]['actionplan_set'][k]['comment']):
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=data[i]['actionplan_set'][k]['comment']['text'])
                            else:
                                fillercomment = "No comments for: Crisis " + str(crisis_id) + " - Plan " + str(plan_num)
                                newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status, plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime, plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF, plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF, plan_comments=fillercomment)
                            testPlan = Plan.objects.filter(plan_ID=plan_id)
                            if not testPlan:
                                newPlan.save()
                                print("Plan saved: " + str(plan_id) + " " + str(plan_status))
                            else:
                                print("Plan already exists")
                        else:
                            #disregard plan
                            #plan_status = "Throw"
                            print("Plan is Thrown.")
                else:
                    print("No Plan for Crisis: " + str(crisis_id))

                #CrisisUpdates Model
                #Missing: None. All acounted
                # - updates_crisisID:  data[i]['id'] --- Pseudo Foreign Key (Do a crisis.pk = crisis_ID)

                if(data[i]['efupdate_set']):
                    for l in range(0, len(data[i]['efupdate_set'])):
                        stat_id = data[i]['efupdate_set'][l]['id']
                        stat_datetime = data[i]['efupdate_set'][l]['datetime']  # updates_datetime
                        stat_radius = data[i]['efupdate_set'][l]['affectedRadius']  # ??
                        stat_injured = data[i]['efupdate_set'][l]['totalInjured']  # updates_curInjuries
                        stat_deaths = data[i]['efupdate_set'][l]['totalDeaths']  # updates_curDeaths
                        stat_duration = data[i]['efupdate_set'][l]['duration']  # ??
                        # stat_description = data[i]['efupdate_set'][l]['description']  #?? updates_description

                        # buffer input
                        curSAF = 0
                        curSPF = 0
                        curSCDF = 0

                        if(data[i]['efupdate_set'][l]['description']):
                            stat_description=data[i]['efupdate_set'][l]['description']
                        else:
                            stat_description="No description for crisis at: "+str(stat_datetime)

                        if (data[i]['efupdate_set'][l]['forceutilization_set']):
                            plan_forces = data[i]['efupdate_set'][l]['forceutilization_set']
                            for force in plan_forces:
                                if (force['name'] == "SAF"):
                                    curSAF = force['utilization']
                                elif (force['name'] == "SPF"):
                                    curSPF = force['utilization']
                                elif (force['name'] == "SCDF"):
                                    curSCDF = force['utilization']
                            newStat = CrisisUpdates(id=stat_id, updates_crisisID=crisis_id, updates_datetime=stat_datetime, updates_curInjuries=stat_injured, updates_curDeaths=stat_deaths, updates_curSAF=curSAF, updates_curSPF=curSPF, updates_curSCDF=curSCDF, updates_description=stat_description)
                        else:
                            newStat = CrisisUpdates(id=stat_id, updates_crisisID=crisis_id, updates_datetime=stat_datetime, updates_curInjuries = 0, updates_curDeaths = 0, updates_curSAF = 0, updates_curSPF = 0, updates_curSCDF = 0, updates_description=stat_description)

                        testStat = CrisisUpdates.objects.filter(id=stat_id)
                        if not (testStat):
                            newStat.save()
                        else:
                            print("Stat already exists")

                else:
                    newStat = CrisisUpdates(updates_crisisID=crisis_id, updates_datetime=datetime.datetime.now(),updates_curInjuries=0, updates_curDeaths=0, updates_curSAF=0,updates_curSPF=0, updates_curSCDF=0, updates_description="")
                    newStat.save()
                    print("No Statistics for Crisis: " + str(crisis_id)+". Creating filler data.")
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

def login(request):
    return render(request, 'pmoapp/LoginGUI/login.html', {})

def logout(request):
    return render(request, 'pmoapp/LoginGUI/logout.html', {})

def otplogout(request):
    return render(request, 'pmoapp/LoginGUI/otplogout.html', {})

def otp(request):
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    #Sessionstuff
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    loggedin = request.session['Loggedin'] = False
    curnumNotifications = Notifications.objects.count()
    request.session['NumNotifications'] = curnumNotifications
    email_text = str(request.user) + ": " +str(OTP)
    send_mail(subject, email_text, from_email, to_email, fail_silently=False)
    # send_mail(subject, str(OTP), from_email, to_email, fail_silently=False)
    print(str(OTP))
    return render(request, 'pmoapp/LoginGUI/authotp.html', {})

def resendOTP(request):
    del request.session['OTP']
    subject = 'OTP'
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]
    OTP = request.session['OTP'] = randint(10000000, 99999999)
    email_text = str(request.user) + ": " + str(OTP)
    send_mail(subject, email_text, from_email, to_email, fail_silently=False)
    return render(request, 'pmoapp/LoginGUI/authotp.html', {})

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
            #print("User logged in")
            return True
        else:
            #print("User not logged in")
            return False
    else:
        #print("Session not found")
        return False

def home(request):
    if not login_check(request.session):
        return redirect('/otplogout')
    #MyCMOApi()
    CMOListener()
    template = loader.get_template('pmoapp/HomeGUI/home.html')
#Process Account/Session
    updateTime = datetime.datetime.now()
    curUsername = request.user
    curAccount = Account.objects.filter(username=curUsername).get()  # in session or something
    accountType = curAccount.user_type
    profilePicture = curAccount.profilePicture

    if(curAccount.gender):
        salutation = "Mr."
    else:
        salutation = "Ms."

    curUser = salutation + " " + request.user.last_name +" "+ request.user.first_name

    #Process Crisis/Plans
    crisisList = Crisis.objects.exclude(crisis_status='Resolved').order_by('crisis_ID')
    for crisis in crisisList:
        print(crisis)
    toDisplay = []
    planIDS = []
    for crisis in crisisList:
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if plansInCrisis:
            max = plansInCrisis[0]
            for plan in plansInCrisis:
                if(plan.plan_ID > max.plan_ID):
                    max = plan
            toDisplay.append(max)
            planIDS.append(max.plan_crisisID)

    context = {
        'toDisplay': toDisplay,
        'ongoingCrisis': crisisList,
        'updateTime': updateTime,
        'accountType': accountType,
        'curUser': curUser,
        'planIDs': planIDS,
        'curName': json.dumps(curUser),
        'profilePicture': profilePicture,
    }
    return HttpResponse(template.render(context, request))

def history(request):
    if not login_check(request.session):
        return redirect('/otplogout')

    template = loader.get_template('pmoapp/HistoricalGUI/history.html')

    #Get user info

    updateTime = datetime.datetime.now()
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

    for index, crisis in enumerate(ongoingCrisisList):
        #print(index, crisis)
        plansInCrisis = Plan.objects.filter(plan_crisisID=crisis.crisis_ID)
        if(plansInCrisis):
            max = plansInCrisis[0]
            for index2, plan in enumerate(plansInCrisis):
                #print(index2, plan)
                if (plan.plan_ID > max.plan_ID):
                    max = plan
                    ongoingPlanList.append(plansInCrisis[index2-1])

    # Get all plans where Crisis status = Resolved
    historicalCrisisList = Crisis.objects.filter(crisis_status='Resolved')
    historicalPlanList = []
    for crisis in historicalCrisisList:
        for plan in allPlans:
            if (crisis.crisis_ID == plan.plan_crisisID):
                historicalPlanList.append(plan)

    toDisplay = ongoingPlanList + historicalPlanList
    allCrisis = Crisis.objects.all()
    context = {
        'toDisplay': toDisplay,
        'ongoingCrisis': ongoingCrisisList,
        'updateTime': updateTime,
        'allCrisis': allCrisis,
        'accountType':accountType,
        'curUser': curUser,
        'profilePicture': profilePicture,
    }
    return HttpResponse(template.render(context, request))

def crisis(request, crisis_id):
    if not login_check(request.session):
        return redirect('/otplogout')

    template = loader.get_template('pmoapp/CrisisGUI/crisis.html')
    updateTime = datetime.datetime.now()
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
        baseUpdate = CrisisUpdates(updates_crisisID=crisisItem.crisis_ID, updates_datetime=updateTime, updates_curInjuries = 0, updates_curDeaths = 0, updates_curSAF = 0, updates_curSPF = 0, updates_curSCDF = 0, updates_description="")
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

    #display update comments:
    allUpdates = []
    if(CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)):
        allUpdates = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)

    #test to see if there is a comment by this minister yet

    if(plan_id != -1):
        if (EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)):
            allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
        else:
            allComments = []

        if (EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)):
            myComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)
        else:
            myComments = []

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


    if(ApproveAgency.objects.filter(approve_approver__user_type=curUserType, approve_crisis__crisis_ID=crisis_id)):
        curAgencies = ApproveAgency.objects.filter(approve_approver__user_type=curUserType, approve_crisis__crisis_ID=crisis_id)
    else:
        curAgencies = []

    context = {
        'planItem': planItem,
        'allUpdates': allUpdates,
        'curAgencies': serializers.serialize('json', curAgencies),
        'profilePicture': profilePicture,
        'decisionTable': decisionTable,
        'ongoingCrisis': crisisList,
        'allAccounts': allAccounts,
        'submittedUsers': submittedUsers,
        'crisisItem': crisisItem,
        'plan_ID': plan_id,
        'allSubCrisis': allSubCrisis,
        'crisisStatus':json.dumps(crisisItem.crisis_status),
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'crisis_ID': crisis_id,
        'curName': json.dumps(curUser),
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
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
        return redirect('/otplogout')

    template = loader.get_template('pmoapp/CrisisGUI/report.html')
    updateTime = datetime.datetime.now()
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

    #print(updateItem)

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
    if (EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)):
        allComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id)
    else:
        allComments = []

    if(EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)):
        myComments = EvalPlan.objects.filter(eval_planID__plan_ID=plan_id, eval_userID__user_type=curUserType)
    else:
        myComments = []

    submittedUsers = []
    for c in allComments:
        submittedUsers.append(c.eval_userID.user_type)

    allSubCrisis = []
    if SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID):
        allSubCrisis = SubCrisis.objects.filter(crisis_ID=crisisItem.crisis_ID)

    # Approval package:

    myAgencies = ExternalAgency.objects.filter(agency_approver__user_type=curUserType)

    if (ApproveAgency.objects.filter(approve_approver__user_type=curUserType, approve_crisis__crisis_ID=crisisItem.crisis_ID)):
        curAgencies = ApproveAgency.objects.filter(approve_approver__user_type=curUserType, approve_crisis__crisis_ID=crisisItem.crisis_ID)
    else:
        curAgencies = []

    allUpdates = []
    if (CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)):
        allUpdates = CrisisUpdates.objects.filter(updates_crisisID=crisisItem.crisis_ID)

    print("open")
    print(crisisItem.crisis_status)
    print(planItem.plan_comments)
    print("closed")

    context = {
        'planItem': planItem,
        'allUpdates': allUpdates,
        'profilePicture': profilePicture,
        'decisionTable': decisionTable,
        'ongoingCrisis': crisisList,
        'allAccounts': allAccounts,
        'submittedUsers': submittedUsers,
        'crisisItem': crisisItem,
        'plan_ID': planItem.plan_ID,
        'curAgencies': serializers.serialize('json', curAgencies),
        'allSubCrisis': allSubCrisis,
        'crisisID': json.dumps(crisisItem.crisis_ID),
        'curName': json.dumps(curUser),
        'jsonCrisis': serializers.serialize('json', graphUpdateList),
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
        'crisisStatus': json.dumps(crisisItem.crisis_status),
        'crisis_ID': crisisItem.crisis_status,
    }
    return HttpResponse(template.render(context, request))

def sendReport(request):
    if request.POST:
        curPlanID = request.POST['planID']
        action = request.POST['planAction']
        #1. Comments

        allComments = EvalPlan.objects.filter(eval_planID=curPlanID) #Will return 5 objects

        concatComments = ""
        if(allComments):
            for n in allComments:
                concatComments += str(n.eval_userID.user_type) + ": " + str(n.eval_text) + " \r\n"

        print(concatComments)

        #2. Status

        reportStatus = True

        if(action == "Approve"):
            reportStatus = True
        elif(action == "Reject"):
            reportStatus = False

        #Change http when we have

        try:
            requests.post('http://172.21.148.168/api/auth/', data={
                'PlanID': curPlanID,
                'Comments': concatComments,
                'PlanStatus': reportStatus
            })
            print("Report Sent")
            print(curPlanID)
            print(concatComments)
            print(reportStatus)

        except HTTPError as e:
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        else:
            # do something
            print('Plan sent to CMO successfully!')

        #update plan_comments in comments box.

        # Change the status of report to pending cmo fortesting
        if (reportStatus == True):
            Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Approved")
            Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())
        else:
            Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Pending CMO")
            Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())

    return HttpResponse('')

def saveComment(request):
    print(request)
    if request.POST:
        getPlanID = request.POST['planID']
        getAccType = request.POST['accType']
        getCommentTxt = request.POST['commentTxt']
        getHasComment = request.POST['hasComment']
        getMyApprovals = request.POST.getlist('myApprovals[]')

        curAccount = Account.objects.filter(user_type=getAccType).get()
        curPlan = Plan.objects.filter(plan_ID=getPlanID).get()
        eval_entry = EvalPlan(eval_planID=curPlan, eval_userID=curAccount, eval_text=getCommentTxt, eval_hasComment=getHasComment)
        testDuplicate = EvalPlan.objects.filter(eval_planID__plan_ID=getPlanID, eval_userID__user_type=getAccType)

        crisis_id = curPlan.plan_crisisID
        curCrisis = Crisis.objects.filter(crisis_ID=crisis_id).get()

        curAgencies = []
        if (ApproveAgency.objects.filter(approve_approver__user_type=getAccType, approve_crisis__crisis_ID=crisis_id)):
            curAgencies = ApproveAgency.objects.filter(approve_approver__user_type=getAccType, approve_crisis__crisis_ID=crisis_id)
            for item in curAgencies:
                item.delete()

        for agency in getMyApprovals:
            theagency = ExternalAgency.objects.filter(agency_abbrev=agency).get()
            newAgency = ApproveAgency(approve_approver=curAccount,approve_agency=theagency,approve_crisis=curCrisis)
            newAgency.save()

        print("open")
        print(curAgencies)

        testmyinserts = ApproveAgency.objects.filter(approve_approver__user_type=getAccType, approve_crisis__crisis_ID=crisis_id)
        for item in testmyinserts:
            print(item.approve_agency)

        print("close")

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


def newsfeed(request):
    if not login_check(request.session):
        return redirect('/otplogout')
    template=loader.get_template('pmoapp/NewsfeedGUI/newsfeed.html')

    updateTime = datetime.datetime.now()
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
        'curName': json.dumps(curUser)
    }
    return HttpResponse(template.render(context, request))
