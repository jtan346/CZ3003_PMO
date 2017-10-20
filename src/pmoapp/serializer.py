from rest_framework import serializers
from .models import EvalPlan,Plan

class EvalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvalPlan
        #fields =('approve,approveDP')
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields =('plan_ID','plan_approved')