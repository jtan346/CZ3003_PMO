from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template import loader
from pmoapp.models import *
from datetime import datetime
from django.core import serializers
import json
from pmoapp.serializer import *
from pmoapp.views import *
from django.shortcuts import redirect
import datetime

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