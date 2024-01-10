from rest_framework import serializers
from .models import Pricing, Ride

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ['id', 'name', 'distance_base', 'distance_add', 'tmf', 'wc']
        
class RidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'username', 'distance', 'starttime', 'endtime', 'totalhours', 'wait', 'totalprice']