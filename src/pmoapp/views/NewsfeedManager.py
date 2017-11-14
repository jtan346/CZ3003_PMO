from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template import loader
from pmoapp.models import *
from pmoapp.views import *
from datetime import datetime
import json
from pmoapp.serializer import *
from django.shortcuts import redirect
import datetime

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