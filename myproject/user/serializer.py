from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=20, default='')
    type = serializers.CharField(max_length = 50)
    created_at = serializers.DateTimeField(read_only=True)  # Mark it as read-only

    class Meta:
        model = User
        fields = '__all__'



# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = '__all__'
#         read_only_fields = ['created_at']

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return User.objects.create(**validated_data)
