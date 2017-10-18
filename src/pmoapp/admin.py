"""Used by Django admin application to get a list of registered models.

To register a model:

from pmoapp.models import YourModel
admin.site.register(YourModel)
"""

from django.contrib import admin
from .models import *

class CrisisAdmin(admin.ModelAdmin):
    model = Crisis
    list_display = ('crisis_ID','crisis_name','crisis_status')

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('username','password','emailAddress','user_type', 'name')

class UpdateAdmin(admin.ModelAdmin):
    model = CrisisUpdates
    list_display = ('updates_ID', 'get_crisisID', 'updates_curInjuries', 'updates_curDeaths', 'updates_curRadius', 'updates_curSAF', 'updates_curSCDF', 'updates_curCD')
    def get_crisisID(self, obj):
        return obj.updates_crisisID.crisis_ID
    get_crisisID.admin_order_field = 'crisis'  # Allows column order sorting
    get_crisisID.short_description = 'Crisis ID '  # Renames column head


class PlanAdmin(admin.ModelAdmin):
    Model = Plan
    list_display = ('plan_ID', 'get_crisisID', 'plan_status', 'plan_projResolutionTime', 'plan_projCasualtyRate', 'plan_SAFRecommended', 'plan_CDRecommended', 'plan_SCDFRecommended',
                    'plan_SAFMaximum', 'plan_CDMaximum', 'plan_SCDFMaximum')
    def get_crisisID(self, obj):
        return obj.plan_crisisID.crisis_ID
    get_crisisID.admin_order_field = 'crisis'  # Allows column order sorting
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
    list_display = ('crisis', 'agency', 'approve_text')
    def agency(self, obj):
        return obj.approve_agency.agency_abbrev
    def crisis(self, obj):
        return obj.approve_crisis.crisis_ID

class EvalPlanAdmin(admin.ModelAdmin):
    Model = EvalPlan
    list_display = ('eval_planID','eval_userID','eval_text')

admin.site.register(Account, AccountAdmin)
#admin.site.register(CurrentReport)
admin.site.register(Crisis, CrisisAdmin)
admin.site.register(CrisisUpdates, UpdateAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(ExternalAgency, ExternalAgencyAdmin)
admin.site.register(ApproveAgency, ApproveAgencyAdmin)
admin.site.register(EvalPlan, EvalPlanAdmin)

