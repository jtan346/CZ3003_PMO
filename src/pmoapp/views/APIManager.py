from pmoapp.models import *
from datetime import datetime
from django.core import serializers
import json
from rest_framework import permissions, viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from pmoapp.serializer import *
from pmoapp.views import *
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
                        # elif data[i]['actionplan_set'][k]['status'] == "Resolved":
                        #     plan_status = "Resolved"
                        #     if (data[i]['actionplan_set'][k]['comment']):
                        #         newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id, plan_type=plan_type, plan_description=plan_description, plan_projResolutionTime=plan_projtime, plan_status=plan_status,plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime,plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF, plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF,plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF,plan_comments=data[i]['actionplan_set'][k]['comment']['text'])
                        #     else:
                        #         fillercomment = "No comments for: Crisis " + str(crisis_id) + " - Plan " + str(plan_num)
                        #         newPlan = Plan(plan_ID=plan_id, plan_num=plan_num, plan_crisisID=crisis_id,plan_type=plan_type, plan_description=plan_description,plan_projResolutionTime=plan_projtime, plan_status=plan_status,plan_receipt=datetime.datetime.now(), plan_sendtime=plan_senttime,plan_projCasualtyRate=plan_projcasualty, plan_SAFRecommended=recSAF,plan_SPFRecommended=recSPF, plan_SCDFRecommended=recSCDF,plan_SAFMaximum=maxSAF, plan_SPFMaximum=maxSPF, plan_SCDFMaximum=maxSCDF,plan_comments=fillercomment)
                        #     testPlan = Plan.objects.filter(plan_ID=plan_id)
                        #     if not testPlan:
                        #         newPlan.save()
                        #         print("Plan saved: " + str(plan_id) + " " + str(plan_status))
                        #     else:
                        #         print("Plan already exists")
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