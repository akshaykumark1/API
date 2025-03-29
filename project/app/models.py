from django.db import models

# Create your models here.
from django.db import models

class student(models.Model):
    roll = models.IntegerField()
    name = models.CharField(max_length=50)
    age = models.IntegerField()
   
    def __str__(self):
        return self.name
