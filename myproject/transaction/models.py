from django.db import models
from customer.models import Customer
from deposite.models import Deposite
from expense.models import Expense


# Create your models here.
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    credit_amt = models.IntegerField()
    debit_amt = models.IntegerField()
    customer_id = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_id"
    )
    deposit_type_id = models.ForeignKey(
        Deposite,
        on_delete=models.CASCADE,
        related_name="deposite_type_id"
    )
    expense_type_id = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name="expense_type_id"
    )