from django.db import models
from datetime import date

class Expense(models.Model):

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

    type = models.CharField(max_length= 50, choices = EXPENSE_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.get_type_display()