"""Used by Django admin application to get a list of registered models.

To register a model:

from pmoapp.models import YourModel
admin.site.register(YourModel)
"""

from django.contrib import admin
from .models import *

class CrisisAdmin(admin.ModelAdmin):
    list_display = ('crisis_ID','crisis_name','crisis_status')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','password','emailAddress','user_type')

# class UpdateAdmin(admin.ModelAdmin):
#     list_display = ('crisis_ID')

admin.site.register(Account, AccountAdmin)
#admin.site.register(CurrentReport)
admin.site.register(Crisis, CrisisAdmin)
admin.site.register(CurrentUpdates)
admin.site.register(Plan)

