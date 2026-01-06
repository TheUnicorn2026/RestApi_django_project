from rest_framework import serializers
from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
    Type = serializers.CharField(max_length = 20)
    StartDate = serializers.DateField
    Duration = serializers.IntegerField
    created_at = serializers.DateTimeField(read_only=True)



    class Meta:
        model = Plan
        fields = '__all__'
