import rest_framework.serializers
from .models import *

class CMOSerializer(rest_framework.serializers.ModelSerializer):
     class Meta:
         model = Notifications
         fields = '__all__'