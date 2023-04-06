from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class UserPredictDataModel(models.Model):
    Engine_Size = models.CharField(max_length=100)
    Cylinders = models.CharField(max_length=100)
    Transmission = models.CharField(max_length=100)
    Fuel_Type = models.CharField(max_length=100)
    FC_City = models.CharField(max_length=100)
    FC_Hwy = models.CharField(max_length=100)
    FC_Comb_km = models.CharField(max_length=100)
    FC_Comb_mpg = models.CharField(max_length=100)
    CO2_Emission_Rating = models.CharField(max_length=100)

def __str__(self):
    return self.Engine_Size, self.Cylinders,self.Transmission,self.Fuel_Type,self.FC_City,self.FC_Hwy,self.FC_Comb_km,self.FC_Comb_mpg,self.CO2_Emission_Rating
    
class FeedModel(models.Model):
    Feedback = models.TextField(max_length=100)

    def __str__(self):
        return str(self.Feedback)