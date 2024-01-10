from django.db import models

# Create your models here.
class Pricing(models.Model):
    name = models.CharField(max_length=10)
    active = models.BooleanField(default = False)
    distance_base_tier1 = models.DecimalField(max_digits = 5, decimal_places = 2)
    distance_base_tier2 = models.DecimalField(max_digits = 5, decimal_places = 2)
    distance_base_tier3 = models.DecimalField(max_digits = 5, decimal_places = 2)
    
    distance_add_tier1 = models.DecimalField(max_digits = 5, decimal_places = 2)
    distance_add_tier2 = models.DecimalField(max_digits = 5, decimal_places = 2)
    
    tmf_tier1 = models.DecimalField(max_digits = 5, decimal_places = 2)
    tmf_tier2 = models.DecimalField(max_digits = 5, decimal_places = 2)
    tmf_tier3 = models.DecimalField(max_digits = 5, decimal_places = 2)
    
    wc_tier1 = models.DecimalField(max_digits = 5, decimal_places = 2)
    wc_tier2 = models.DecimalField(max_digits = 5, decimal_places = 2)
    
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.name

class Ride(models.Model):
    username = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    starttime = models.CharField(max_length=50)
    endtime = models.CharField(max_length=50)
    waittime = models.CharField(max_length=50)
    totalhours = models.CharField(max_length=50)
    totalprice = models.CharField(max_length=50)
     
    def __str__(self):
        return self.username