"""All models for pmoapp Django application."""

from django.db import models
from django.core.validators import *


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

class user(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    emailAddress = models.EmailField()
    user_type = models.CharField(max_length=15)  #Enum: PM, DPM, MOHA, MOFA, MinDef

"""

Possible classes:

class auth

class session

class admin

"""








