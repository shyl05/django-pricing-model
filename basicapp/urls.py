from .views import *
from django.urls import path

# urlpatterns = [
#     path('get-pricing', PricingViewset.as_view({'get': 'list'})),
#     path('create-pricing', PricingViewset.as_view({'get': 'list','post': 'create'})),
#     path('update-pricing', PricingViewset.as_view({'update': 'update'})),
#     path('delete-pricing', PricingViewset.as_view({'get': 'list','delete': 'destroy'})),
#     path('set-pricing', create_pricing),
#     path('calulate', calculate_pricing)
# ]

urlpatterns = [
    path('pricing-list', pricing_list, name='pricing-list'),
    path('pricing-create', pricing_create, name='pricing-create'),
    path('pricing-update/<int:id>', pricing_update, name='pricing-update'),
    path('pricing-delete/<int:id>', pricing_delete, name='pricing-delete'),
    path('calculate', calculate_pricing),
    path('export-csv', export_query_to_csv, name='export-csv'),
    path('rides-list', rides_list, name='rides-list'),
    path('export-ridecsv', export_rides_to_csv, name='export-ridecsv'),
]