from rest_framework import serializers
from .models import Deposite

class DepositeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    deposite_id = serializers.CharField(max_length= 10)
    created_at = serializers.DateTimeField(read_only=True)  # Mark it as read-only

    class Meta:
        model = Deposite
        fields = '__all__'
    
