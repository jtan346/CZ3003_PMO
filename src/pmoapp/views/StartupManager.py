from pmoapp.models import *
from pmoapp.serializer import *
from pmoapp.views import *

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
    ApproveAgency.objects.all().delete()
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