import random
import uuid
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, PasswordResetOTP
from .serializer import UserSerializer


OTP_EXP_MINUTES = 5
MAX_OTP_ATTEMPTS = 5

# Create your views here.

class UserAPI(APIView):
    
    def post(self, request):
        data = request.data.copy()
        data['password'] = make_password(data['password'])

        serializer = UserSerializer(data=data)
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
            
        
            # if password == serializer.data.password:
            if password == user.password or check_password(password, user.password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": serializer.data
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
        

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.ok
    except Exception:
        return False



class ForgotPasswordAPI(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # do NOT reveal user existence
            return Response(
                {"message": "If account exists, OTP sent"},
                status=status.HTTP_200_OK
            )

        if not user.telegram_chat_id:
            return Response(
                {"error": "Telegram not linked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = f"{random.randint(0, 999999):06d}"
        expires_at = timezone.now() + timedelta(minutes=5)

        PasswordResetOTP.objects.create(
            user=user,
            otp=otp,
            expires_at=expires_at
        )

        send_telegram_message(
            user.telegram_chat_id,
            f"Password reset OTP: {otp}\nValid for 5 minutes."
        )

        return Response(
            {"message": "If account exists, OTP sent"},
            status=status.HTTP_200_OK
        )


class VerifyOTPAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response(
                {"error": "email and otp required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            reset = PasswordResetOTP.objects.filter(user=user).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_used or reset.is_expired():
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        if reset.otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        reset.is_verified = True
        reset.reset_token = uuid.uuid4().hex
        reset.save()

        return Response(
            {"reset_token": reset.reset_token},
            status=status.HTTP_200_OK
        )


class ResetPasswordAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        reset_token = request.data.get('reset_token')
        new_password = request.data.get('new_password')

        if not email or not reset_token or not new_password:
            return Response(
                {"error": "email, token, password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            reset = PasswordResetOTP.objects.get(
                user=user,
                reset_token=reset_token,
                is_verified=True,
                is_used=False
            )
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        reset.is_used = True
        reset.save()

        send_telegram_message(
            user.telegram_chat_id,
            "✅ Your password has been changed successfully."
        )

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )




