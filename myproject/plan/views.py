from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Plan
from .serializer import PlanSerializer

# Create your views here.

class PlanAPI(APIView):
    
    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                plan = Plan.objects.get(id=id)  # Corrected to .objects
            except Plan.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PlanSerializer(plan)
            return Response(serializer.data)

        plans = Plan.objects.all()  # Corrected to .objects
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        if id:
            try:
                plan = Plan.objects.get(id=id)  # Corrected to .objects
            except Plan.DoesNotExist:  # Corrected exception type
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PlanSerializer(plan, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            plan = Plan.objects.get(id=id)
        except Plan.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response({"message": "Customer Deleted"}, status=status.HTTP_204_NO_CONTENT)
