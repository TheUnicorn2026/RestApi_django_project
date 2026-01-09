from django.urls import path
from .views import RegisterAPIView

urlpatterns = [
    path('', RegisterAPIView.as_view(), name='root'),
    path('register/', RegisterAPIView.as_view(), name='register')
]
