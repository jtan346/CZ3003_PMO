from rest_framework import serializers
from .models import EvalPlan,Plan,testmyfuckingapi,Notifications

class EvalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvalPlan
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields =('plan_ID','plan_approved')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = testmyfuckingapi
        fields = '__all__'

class CMOSerializer(serializers.ModelSerializer):
     class Meta:
         model = Notifications
         fields = '__all__'