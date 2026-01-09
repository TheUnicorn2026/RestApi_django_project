from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from .models import User
from .serializer import UserSerializer

# Create your views here.

class UserAPI(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)  # Corrected to .objects
            except User.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(serializer.data)

        users = User.objects.all()  # Corrected to .objects
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        if id:
            try:
                user = User.objects.get(id=id)  # Corrected to .objects
            except User.DoesNotExist:  # Corrected exception type
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "Customer Deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            
            serializer = UserSerializer(user)
            # return Response(serializer.data)
            print(serializer.data)
            print(user.password, user.phone)
        
            # if password == serializer.data.password:
            if check_password(password, user.password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": serializer.data
                        # "user": {
                        #     "id": serializer.data.id,
                        #     "name": serializer.data.name,
                        #     "email": serializer.data.email,
                        #     "phone": serializer.data.phone,
                        #     "type": serializer.data.type,
                        #     "created_at": serializer.data.created_at
                        # }
                    },
                    status=status.HTTP_200_OK
                )
            else: 
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # if not check_password(password, user.password):
        if password != user.password:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "type": user.type,
                    "created_at": user.created_at
                }
            },
            status=status.HTTP_200_OK
        )
