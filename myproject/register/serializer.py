from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = ['name', 'email', 'password', 'phone', 'type', 'created_at']
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)



# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from .models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return User.objects.create(**validated_data)
