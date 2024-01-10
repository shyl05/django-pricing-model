from django import forms
from django.forms import ModelForm,  Textarea
from .models import Pricing

class PricingForm(ModelForm):
    class Meta:
        model = Pricing
        fields = "__all__"
    