"""Used by Django admin application to get a list of registered models.

To register a model:

from pmoapp.models import YourModel
admin.site.register(YourModel)
"""

from django.contrib import admin
from .models import *
from django.contrib import admin
import inspect
from django.db.models import Model

class CrisisAdmin(admin.ModelAdmin):
    model = Crisis
    list_display = ('crisis_ID','crisis_name','crisis_status')

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('username','appointment','user_type')

class UpdateAdmin(admin.ModelAdmin):
    model = CrisisUpdates
    list_display = ('get_crisisID', 'updates_curInjuries', 'updates_curDeaths', 'updates_curSAF', 'updates_curSCDF', 'updates_curSPF')
    def get_crisisID(self, obj):
        return obj.updates_crisisID
    get_crisisID.admin_order_field = 'crisis'  # Allows column order sorting
    get_crisisID.short_description = 'Crisis ID '  # Renames column head

class SubCrisisAdmin(admin.ModelAdmin):
    model = SubCrisis
    list_display = ('sc_ID', 'datetime', 'crisis_ID', 'latitude', 'longitude', 'radius')

class PlanAdmin(admin.ModelAdmin):
    Model = Plan
    list_display = ('plan_num', 'plan_ID', 'get_crisisID', 'plan_status', 'plan_projResolutionTime', 'plan_projCasualtyRate', 'plan_SAFRecommended', 'plan_SPFRecommended', 'plan_SCDFRecommended',
                    'plan_SAFMaximum', 'plan_SPFMaximum', 'plan_SCDFMaximum')
    def get_crisisID(self, obj):
        return obj.plan_crisisID
    get_crisisID.admin_order_field = 'plan_crisisID'  # Allows column order sorting
    get_crisisID.short_description = 'Crisis ID '  # Renames column head

class ExternalAgencyAdmin(admin.ModelAdmin):
    Model = ExternalAgency
    list_display = ('get_approver','agency_name','agency_abbrev','agency_poc','agency_pocContact')
    def get_approver(self, obj):
        return obj.agency_approver.user_type
    get_approver.admin_order_field = 'agency_approver'   # Allows column order sorting
    get_approver.short_description = 'Approver'  # Renames column head\

class ApproveAgencyAdmin(admin.ModelAdmin):
    Model = ApproveAgency
    list_display = ('crisis', 'agency')
    def agency(self, obj):
        return obj.approve_agency.agency_abbrev
    def crisis(self, obj):
        return obj.approve_crisis.crisis_ID

class EvalPlanAdmin(admin.ModelAdmin):
    Model = EvalPlan
    list_display = ('id', 'eval_planID','get_userID','eval_text','eval_hasComment')

    def get_planID(self, obj):
        return obj.eval_planID

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plan":
            kwargs["queryset"] = Plan.objects.order_by('id')
        return super(EvalPlanAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_userID(self, obj):
        return obj.eval_userID.user_type

class NotificationAdmin(admin.ModelAdmin):
    Model = Notifications
    list_display = ('PlanNum', 'PlanID', 'CrisisID', 'CrisisTitle', 'DateTime')

admin.site.register(Notifications, NotificationAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Crisis, CrisisAdmin)
admin.site.register(CrisisUpdates, UpdateAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(SubCrisis, SubCrisisAdmin)
admin.site.register(ExternalAgency, ExternalAgencyAdmin)
admin.site.register(ApproveAgency, ApproveAgencyAdmin)
admin.site.register(EvalPlan, EvalPlanAdmin)
