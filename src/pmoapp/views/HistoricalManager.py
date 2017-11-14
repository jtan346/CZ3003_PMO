from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template import loader
from pmoapp.models import *
from datetime import datetime
from pmoapp.serializer import *
from pmoapp.views import *
from django.shortcuts import redirect
import datetime

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