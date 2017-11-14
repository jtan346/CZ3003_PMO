"""All models for pmoapp Django application."""

from django.db import models
from django.core.validators import *
import datetime
from django.contrib.auth.models import User

class Account(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    handphone_number = models.IntegerField(
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(80000000)
        ]
    )
    user_type = models.CharField(max_length=200)  #Enum: PM, DPM, MOHA, MOFA, MDef
    appointment = models.CharField(max_length=150) #Long form of their user_type
    profilePicture = models.ImageField(upload_to='profilepics', blank=True)
    decisionTable = models.ImageField(upload_to='decisiontables', blank=True)
    gender = models.BooleanField(default=True) #True = male, False = female
    def __str__(self):
        return self.user_type

class ExternalAgency(models.Model): #many-to-many
    agency_name = models.CharField(max_length=200)
    agency_abbrev = models.CharField(max_length=200, primary_key=True)
    agency_poc = models.CharField(max_length=200)
    agency_pocContact = models.CharField(max_length=200)
    agency_description = models.CharField(max_length=500, null=True)
    agency_approver = models.ForeignKey(Account)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "External Agencies"
    def __str__(self):
        return self.agency_name

class Crisis(models.Model):
    crisis_ID = models.IntegerField(primary_key=True)
    crisis_name = models.CharField(max_length=500)
    crisis_description = models.TextField(null=True, blank=True)
    crisis_datetime = models.DateTimeField() #Initial 911
    crisis_status = models.CharField(max_length=200)  # Enum: Ongoing, Cleaning-Up, Resolved
    crisis_extAgencies = models.ManyToManyField(ExternalAgency, through='ApproveAgency', null=True)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis"
    def __str__(self):
        return str(self.crisis_ID)

class SubCrisis(models.Model): #For address, and granularity
    sc_ID = models.IntegerField(primary_key=True)
    crisis_ID = models.IntegerField()
    crisis_type = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    radius = models.IntegerField(verbose_name="Radius(Metres)", validators=[MinValueValidator(0)])
    datetime = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Sub Crisis"

class CrisisUpdates(models.Model): #EF Updates
    id = models.IntegerField(primary_key=True)
    updates_crisisID = models.IntegerField()
    updates_datetime = models.DateTimeField()
    updates_curInjuries = models.IntegerField(null=True, default=0)
    updates_curDeaths = models.IntegerField(null=True, default=0)
    updates_curSAF = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curSPF = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curSCDF = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    updates_description = models.TextField(null=True, blank=True)

    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis Updates"

class Plan(models.Model):
    plan_ID = models.IntegerField(primary_key=True)
    plan_num = models.IntegerField()
    plan_crisisID = models.IntegerField()
    plan_description = models.TextField(null=True, blank=True)
    plan_status = models.CharField(max_length=25)  # Enum: PendingPMO, PendingCMO, Approved(only when approved=True)
    plan_receipt = models.DateTimeField(null=True) #ReceiptTime
    plan_sendtime = models.DateTimeField(null=True, blank=True) #sendtime
    plan_projCasualtyRate = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # Default: 0.0, min; 0.0, max: 100.0
    plan_projResolutionTime = models.TextField(blank=True, null=True)
    plan_SAFRecommended = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SPFRecommended = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFRecommended = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SAFMaximum = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SPFMaximum = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFMaximum = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)  # Default: 0.0, min; 0.0, max: 100.0
    plan_comments = models.TextField(blank=True, null=True) #comments posted to CMO, updated internally
    plan_type = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.plan_ID)

class ApproveAgency(models.Model):
    approve_agency = models.ForeignKey(ExternalAgency, on_delete=models.CASCADE)
    approve_crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    approve_approver = models.ForeignKey(Account, on_delete=models.CASCADE)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Agency Approval"

class EvalPlan(models.Model): #Comments by Ministers
    eval_planID = models.ForeignKey(Plan, on_delete=models.CASCADE, null=False)
    eval_userID = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    eval_text = models.CharField(max_length=500, null=True, blank=True)
    eval_hasComment = models.BooleanField(default=False) #True: Reject with Comment, False: Approved
    class Meta:
        unique_together = ["eval_planID", "eval_userID"]

class Notifications(models.Model):
    PlanNum = models.IntegerField() #Autoincrement
    PlanID = models.IntegerField()
    CrisisID = models.IntegerField()
    CrisisTitle = models.CharField(max_length=500, null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Notifications"







