from django.contrib import admin
from .models import *
# Register your models here.

@admin.action(description="Mark pricing model as Active")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)

class PricingAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    ordering = ["name"]
    actions = [make_active]

admin.site.register(Pricing, PricingAdmin)
admin.site.register(Ride)
