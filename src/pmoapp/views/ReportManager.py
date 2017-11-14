from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template import loader
from pmoapp.models import *
from pmoapp.views import *
from datetime import datetime
from django.core import serializers
import requests
import json
from pmoapp.serializer import *
from django.shortcuts import redirect
from urllib.error import URLError, HTTPError
import datetime

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

        planItem = Plan.objects.filter(plan_ID=curPlanID).get()
        crisisItem = Crisis.objects.filter(crisis_ID=planItem.plan_crisisID).get()

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

        #3. Agencies

        agencyText = ""
        if(ApproveAgency.objects.filter(approve_crisis__crisis_ID=crisisItem.crisis_ID)):
            for item in ApproveAgency.objects.filter(approve_crisis__crisis_ID=crisisItem.crisis_ID):
                thisAgency = item.approve_agency
                thisApprover = item.approve_approver
                eachagency = ""
                eachagency += "Approver: " + str(thisApprover.user_type) + "(" + str(thisApprover.appointment) + ")\r\n"
                eachagency += "Agency: " + str(thisAgency.agency_abbrev) + "(" + str(thisAgency.agency_name) + ")\r\n"
                eachagency += "Point of Contact: " + str(thisAgency.agency_poc) + "(" + str(thisAgency.agency_pocContact) + ")\r\n"
                eachagency += "Description: " + str(thisAgency.agency_description) + "\r\n"
                print(eachagency)
                agencyText += eachagency + "\r\n"


        #send plan
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

            if (reportStatus == True):
                Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Approved")
                Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())
                if (planItem.plan_status == "Resolved"):
                    Crisis.objects.filter(crisis_ID=planItem.plan_crisisID).update(crisis_status="Resolved")
            else:
                Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Pending CMO")
                Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())

        except HTTPError as e:
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        else:
            # do something
            print('Plan sent to CMO successfully!')

        # #send agencies
        # try:
        #     requests.post('http://172.21.148.168/api/auth/', data={
        #         'PlanID': curPlanID,
        #         'Comments': concatComments,
        #         'PlanStatus': reportStatus
        #     })
        #     print("Report Sent")
        #     print(curPlanID)
        #     print(concatComments)
        #     print(reportStatus)
        #
        # except HTTPError as e:
        #     print('Error code: ', e.code)
        # except URLError as e:
        #     # do something
        #     print('Reason: ', e.reason)
        # else:
        #     # do something
        #     print('Plan sent to CMO successfully!')

        #update plan_comments in comments box.

        # Change the status of report to pending cmo fortesting
        # if (reportStatus == True):
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Approved")
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_comments=concatComments)
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_agencies=agencyText)
        #     #remember update my comments
        #     #agencies already FK to comments
        # else:
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_status="Pending CMO")
        #     Plan.objects.filter(plan_ID=curPlanID).update(plan_sendtime=datetime.datetime.now())

        Plan.objects.filter(plan_ID=curPlanID).update(plan_comments=concatComments)
        Plan.objects.filter(plan_ID=curPlanID).update(plan_agencies=agencyText)

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

        # print("open")
        # print(curAgencies)
        #
        # testmyinserts = ApproveAgency.objects.filter(approve_approver__user_type=getAccType, approve_crisis__crisis_ID=crisis_id)
        # for item in testmyinserts:
        #     print(item.approve_agency)
        #
        # print("close")

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