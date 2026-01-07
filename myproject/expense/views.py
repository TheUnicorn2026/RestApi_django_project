from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Expense
from .serializer import ExpenseSerializer

class ExpenseAPI(APIView):
        
     # GET all or single
    def get(self, request, id=None):
        try:
            if id:
                expense = Expense.objects.get(id=id)
                serializer = ExpenseSerializer(expense)
                return Response(serializer.data)
            expenses = Expense.objects.all()
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "Expense not found"}, status=404)

    # POST
    def post(self, request):
        try:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Something went wrong"}, status=400)

    # PUT
    def put(self, request, id):
        try:
            expense = Expense.objects.get(id=id)
            serializer = ExpenseSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Update failed"}, status=400)

    # DELETE
    def delete(self, request, id):
        try:
            expense = Expense.objects.get(id=id)
            expense.delete()
            return Response({"message": "expense deleted"})
        except:
            return Response({"error": "Delete failed"}, status=400)
