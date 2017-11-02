"""All models for pmoapp Django application."""

from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User

class Account(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    #password = models.CharField(max_length=15)
    #emailAddress = models.EmailField()
    #name = models.CharField(max_length=50)
    handphone_number = models.IntegerField(
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(80000000)
        ]
    )
    user_type = models.CharField(max_length=15)  #Enum: PM, DPM, MOHA, MOFA, MDef
    appointment = models.CharField(max_length=150) #Long form of their user_type
    profilePicURL = models.CharField(max_length=150, null=True, blank=True)
    gender = models.BooleanField(default=True) #True = male, False = female
    def __str__(self):
        return self.user_type

class ExternalAgency(models.Model): #many-to-many
    agency_name = models.CharField(max_length=70)
    agency_abbrev = models.CharField(max_length=10, primary_key=True)
    agency_poc = models.CharField(max_length=50)
    agency_pocContact = models.CharField(max_length=50)
    agency_description = models.CharField(max_length=500, null=True)
    agency_approver = models.ForeignKey(Account)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "External Agencies"
    def __str__(self):
        return self.agency_name

class Crisis(models.Model):
    crisis_ID = models.IntegerField(
        primary_key=True,
        #max_length=4,
        #validators=[RegexValidator(regex='^\w{4}$', message='Length has to be 4', code='nomatch')]
    )
    crisis_name = models.CharField(max_length=50)
    crisis_description = models.TextField()
    crisis_datetime = models.DateTimeField() #Initial 911
    #crisis_address = models.CharField(max_length=50) #Sub with CrisisReports
    crisis_status = models.CharField(max_length=50)  # Enum: Ongoing, Cleaning-Up, Resolved
    crisis_extAgencies = models.ManyToManyField(ExternalAgency, through='ApproveAgency', null=True)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis"
    def __str__(self):
        return str(self.crisis_ID)

class SubCrisis(models.Model): #For address, and granularity
    sc_ID = models.IntegerField(primary_key=True)
    #crisis_ID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    crisis_ID = models.IntegerField()
    crisis_type = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius = models.IntegerField(verbose_name="Radius(Metres)", validators=[MinValueValidator(0)])

    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Sub Crisis"

class CrisisUpdates(models.Model): #EF Updates
    # updates_ID = models.CharField(
    #     primary_key=True,
    #     max_length=4,
    #     validators=[RegexValidator(regex='^\w{4}$', message='Length has to be 4', code='nomatch')]
    # )
    # updates_crisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    updates_crisisID = models.IntegerField()
    updates_datetime = models.DateTimeField()
    #updates_text = models.CharField(max_length=50, null=True)
    updates_curInjuries = models.IntegerField()
    updates_curDeaths = models.IntegerField()
    #updates_curThreatLevel = models.CharField(max_length=50)  # Enum: Red, Orange, Green?
    # updates_curRadius = models.IntegerField(
    #     validators=[MinValueValidator(0)]
    # )  # In Metres: 1,234
    updates_curSAF = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curCD = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curSCDF = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0

    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis Updates"

class Plan(models.Model):
    plan_ID = models.IntegerField()
        #primary_key=True,
        #max_length=8,
        #validators=[RegexValidator(regex='^\w{8}$', message='Length has to be 8', code='nomatch')]
    # ) # PK
    #plan_crisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    plan_crisisID = models.IntegerField()
    plan_description = models.TextField()
    plan_status = models.CharField(max_length=25)  # Enum: PendingPMO, PendingCMO, Approved(only when approved=True)
    #plan_approved = models.BooleanField(default=False) #True: No comments, ready to go. False: Has comments
    #plan_submitted = models.BooleanField(default=False) #True: Plan locked, no changes to be made.
    # plan_dateTime = models.DateTimeField() #ReceiptTime
    plan_receipt = models.DateTimeField() #ReceiptTime
    plan_sendtime = models.DateTimeField(null=True, blank=True) #sendtime
    # plan_projRadius = models.IntegerField(
    #     validators=[MinValueValidator(0)]
    # )  # In Metres: 1,234
    plan_projCasualtyRate = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_projResolutionTime = models.DateTimeField()
    #plan_projETAResolution = models.DecimalField(max_digits=4, decimal_places=1)  # In hours: 0.5
    plan_SAFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_CDRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SAFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_CDMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0

    def __str__(self):
        return str(self.id)

class ApproveAgency(models.Model):
    approve_agency = models.ForeignKey(ExternalAgency, on_delete=models.CASCADE)
    approve_crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    approve_text = models.CharField(max_length=50)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Agency Approval"

class EvalPlan(models.Model): #Comments by Ministers
    eval_planID = models.ForeignKey(Plan, on_delete=models.CASCADE, null=False)
    eval_userID = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    eval_text = models.CharField(max_length=500, null=True, blank=True)
    eval_hasComment = models.BooleanField(default=False) #True: Reject with Comment, False: Approved
    class Meta:
        unique_together = ["eval_planID", "eval_userID"]

class testmyfuckingapi(models.Model):
    PlanID = models.IntegerField()
    Comments = models.CharField(max_length=5000, null=True, blank=True)
    PlanStatus = models.CharField(max_length=500, null=True, blank=True)

class Notifications(models.Model):
    PlanNum = models.IntegerField(primary_key=True) #Autoincrement
    PlanID = models.IntegerField()
    CrisisID = models.IntegerField()
    CrisisTitle = models.CharField(max_length=500, null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Notifications"
    # def __str__(self):
    #     return str(self.PlanID)

"""

Possible classes:

class auth

class session

class admin

"""







