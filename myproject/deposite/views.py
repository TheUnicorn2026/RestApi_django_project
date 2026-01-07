from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Deposite
from .serializer import DepositeSerializer

class DepositeAPI(APIView):
        
     # GET all or single
    def get(self, request, id=None):
        try:
            if id:
                deposite = Deposite.objects.get(id=id)
                serializer = DepositeSerializer(deposite)
                return Response(serializer.data)
            deposites = Deposite.objects.all()
            serializer = DepositeSerializer(deposites, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "Expense not found"}, status=404)

    # POST
    def post(self, request):
        try:
            serializer = DepositeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Something went wrong"}, status=400)

    # PUT
    def put(self, request, id):
        try:
            deposite = Deposite.objects.get(id=id)
            serializer = DepositeSerializer(deposite, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Update failed"}, status=400)

    # DELETE
    def delete(self, request, id):
        try:
            deposite = Deposite.objects.get(id=id)
            deposite.delete()
            return Response({"message": "expense deleted"})
        except:
            return Response({"error": "Delete failed"}, status=400)
