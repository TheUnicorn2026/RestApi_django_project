from django.db import models

# Create your models here.
class Deposite(models.Model):
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    deposite_id = models.CharField(max_length= 10)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.namepass

