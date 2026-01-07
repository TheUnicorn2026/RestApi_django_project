from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):

    EXPENSE_CHOICES = [
        ('money_transfer', 'Money Transfer'),
        ('food', 'Food'),
        ('fuel', 'Fuel'),
        ('grocery', 'Grocery'),
        ('medical', 'Medical'),
        ('other', 'Other'),
        ('investment', 'Investment'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('bill_payment', 'Bill Payment'),
    ]


    type = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    date = serializers.DateField()

    class Meta:
        model = Expense
        fields = '__all__'