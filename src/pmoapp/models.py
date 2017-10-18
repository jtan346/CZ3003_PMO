"""All models for pmoapp Django application."""

from django.db import models
from django.core.validators import *

"""
class CurrentReport(models.Model):
    crisis_ID = models.IntegerField(
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(1)
        ]
    )
    crisis_name = models.CharField(max_length=50)
    crisis_description = models.CharField(max_length=350)
    crisis_dateTime = models.DateTimeField()
    crisis_address = models.CharField(max_length=50)
    crisis_status = models.CharField(max_length=50)  #Enum: Ongoing, Cleaning-Up, Resolved
    updates_curInjuries = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    updates_curDeaths = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    updates_curThreatLevel = models.CharField(max_length=50)  #Enum: Red, Orange, Green?
    updates_curRadius = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  #In Metres: 1,234
    updates_curSAF = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    updates_curCD = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    updates_curSCDF = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_ID = models.IntegerField(
        primary_key=True,
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(1)
        ]
    )  #PK
    plan_description = models.CharField(max_length=500)
    plan_status = models.CharField(max_length=50)  #Enum: PendingPMO, PendingCMO, Approved, CrisisResolved
    plan_projRadius = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  #In Metres: 1,234
    plan_projCasualtyRate = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_projResolutionTime = models.DateTimeField()
    plan_projETAResolution = models.DecimalField(max_digits=4, decimal_places=1)  #In hours: 0.5
    plan_SAFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_CDRecommended = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_SAFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_CDMaximum = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  #Default: 0.0, min; 0.0, max: 100.0
"""

class Account(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    emailAddress = models.EmailField()
    name = models.CharField(max_length=50)
    handphone_number = models.IntegerField(
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(80000000)
        ]
    )
    user_type = models.CharField(max_length=15)  #Enum: PM, DPM, MOHA, MOFA, MinDef

class ExternalAgency(models.Model): #many-to-many
    agency_name = models.CharField(max_length=70, primary_key=True)
    agency_abbrev = models.CharField(max_length=10)
    agency_poc = models.CharField(max_length=50)
    agency_pocContact = models.CharField(max_length=50)
    agency_description = models.CharField(max_length=500, null=True)
    agency_approver = models.ForeignKey(Account)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "External Agencies"

class Crisis(models.Model):
    """Crisis_ID = models.IntegerField(
            primary_key=True,
            validators=[
                MaxValueValidator(9999),
                MinValueValidator(1)
            ]
        )"""
    crisis_ID = models.CharField(
        primary_key=True,
        max_length=4,
        validators=[RegexValidator(regex='^\w{4}$', message='Length has to be 4', code='nomatch')]
    )
    crisis_name = models.CharField(max_length=50)
    crisis_description = models.CharField(max_length=350)
    crisis_datetime = models.DateTimeField()
    crisis_address = models.CharField(max_length=50)
    crisis_status = models.CharField(max_length=50)  # Enum: Ongoing, Cleaning-Up, Resolved
    crisis_extAgencies = models.ManyToManyField(ExternalAgency, through='ApproveAgency', null=True)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis"
    # def __unicode__(self):
    #     return str(self.crisis_ID) + "     " + self.crisis_name

class CrisisUpdates(models.Model):
    updates_ID = models.CharField(
        primary_key=True,
        max_length=4,
        validators=[RegexValidator(regex='^\w{4}$', message='Length has to be 4', code='nomatch')]
    )
    updates_crisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    updates_datetime = models.DateTimeField()
    updates_text = models.CharField(max_length=50, null=True)
    updates_curInjuries = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    updates_curDeaths = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    updates_curThreatLevel = models.CharField(max_length=50)  # Enum: Red, Orange, Green?
    updates_curRadius = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # In Metres: 1,234
    updates_curSAF = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curCD = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    updates_curSCDF = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0

    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Crisis Updates"

class Plan(models.Model):
    plan_ID = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[RegexValidator(regex='^\w{8}$', message='Length has to be 8', code='nomatch')]
    ) # PK
    plan_crisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    plan_description = models.CharField(max_length=500)
    plan_status = models.CharField(max_length=50)  # Enum: PendingPMO, PendingCMO, Approved(only when approved=True)
    plan_approved = models.BooleanField(default=False)
    plan_dateTime = models.DateTimeField()
    plan_projRadius = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # In Metres: 1,234
    plan_projCasualtyRate = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_projResolutionTime = models.DateTimeField()
    #plan_projETAResolution = models.DecimalField(max_digits=4, decimal_places=1)  # In hours: 0.5
    plan_SAFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_CDRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFRecommended = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SAFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_CDMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0
    plan_SCDFMaximum = models.DecimalField(max_digits=4, decimal_places=1)  # Default: 0.0, min; 0.0, max: 100.0

class ApproveAgency(models.Model):
    approve_agency = models.ForeignKey(ExternalAgency, on_delete=models.CASCADE)
    approve_crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    approve_text = models.CharField(max_length=50)
    class Meta: #For naming convention in django/admin
        verbose_name_plural = "Agency Approval"

class EvalPlan(models.Model): #Comments by Ministers
    eval_planID = models.ForeignKey(Plan, on_delete=models.CASCADE)
    eval_userID = models.ForeignKey(Account, on_delete=models.CASCADE)
    eval_text = models.CharField(max_length=500)


"""

Possible classes:

class auth

class session

class admin

"""








