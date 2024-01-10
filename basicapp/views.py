from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework import status
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PricingForm
from .models import Pricing, Ride
from .serializers import PricingSerializer
from rest_framework.response import Response
from datetime import datetime
import csv
from django.http import StreamingHttpResponse

# class PricingViewset(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]
#     qs = Pricing.objects.all()
#     serializer_class = PricingSerializer

#     def list(self, request):
#         qs = Pricing.objects.all()
#         print(len(qs))
#         serializer = self.serializer_class(qs, many=True)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

#     def retrieve(self, request, pk=None):
#         project = self.qs.get(pk=pk)
#         serializer = self.serializer_class(project)
#         return Response(serializer.data)

#     @action(detail=True, methods=["put"])
#     def update(self, request, pk=None):
#         project = self.qs.get(pk=pk)
#         serializer = self.serializer_class(project, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

#     def destroy(self, request, pk=None):
#         project = self.qs.get(pk=pk)
#         project.delete()
#         return Response(status=204)

# Create your views here.
def pricing_list(request):  
    items = Pricing.objects.all()  
    return render(request,"list.html",{'items': items})  

def pricing_create(request):  
    if request.method == "POST":  
        form = PricingForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('pricing-list')  
            except:  
                pass  
    else:  
        form = PricingForm()  
    return render(request,'create.html',{'form':form})  

def pricing_update(request, id):  
    item = Pricing.objects.get(id=id)
    form = PricingForm(initial={'name': item.name, 
                                'active': item.active, 
                                'created_by': item.created_by, 
                                'created_at': item.created_at, 
                                'distance_base_tier1': item.distance_base_tier1,
                                'distance_base_tier2': item.distance_base_tier2,
                                'distance_base_tier3': item.distance_base_tier3,
                                'distance_add_tier1': item.distance_add_tier1, 
                                'distance_add_tier2': item.distance_add_tier2, 
                                'tmf_tier1': item.tmf_tier1,
                                'tmf_tier2': item.tmf_tier2,
                                'tmf_tier3': item.tmf_tier3,
                                'wc_tier1': item.wc_tier1,
                                'wc_tier2': item.wc_tier2,
                            })
    if request.method == "POST":  
        form = PricingForm(request.POST, instance=item)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('/pricing-list')  
            except Exception as e: 
                pass    
    return render(request,'update.html',{'form':form})  

def pricing_delete(request, id):
    item = Pricing.objects.get(id=id)
    try:
        item.delete()
    except:
        pass
    return redirect('pricing-list')


def find_match(arr, day):
    if day in arr:
        return True
    else:
        return False

# API for getting ride price
@api_view(['POST'])
@csrf_exempt
def calculate_pricing(request):
    type1 = ['Tue', 'Wed', 'Thur']
    type2 = ['Sat', 'Mon']
    
    data = request.data
    print(data)
    
    username = data['username']
    distance = data['distance']
    day = datetime.now().strftime('%a')
    start_time = data['starttime']
    end_time = data['endtime']
    starttime = datetime.strptime(start_time, "%H:%M:%S")
    endtime = datetime.strptime(end_time, "%H:%M:%S")
    ride_time = endtime - starttime
    sec = ride_time.total_seconds()
    ridehours = sec / (60 * 60)
    total_ridehours = float(ridehours) 
    wait = data['wait']
    wait_convert = datetime.strptime(wait, "%H:%M:%S").minute
    waitingtime = float(wait_convert) 

    distance_base = 0.0
    distance_add = 0.0
    tmf = 0.0
    
    pricing_model = Pricing.objects.get(active = 'True')
    if(distance <= 3):
        distance_add = pricing_model.distance_add_tier1
        if(find_match(type1, day) == True):
            distance_base = pricing_model.distance_base_tier1
        elif(find_match(type2, day) == True):
            distance_base = pricing_model.distance_base_tier2
        elif(day == 'Sun'):
            distance_base = pricing_model.distance_base_tier3
    elif(distance > 3):
        distance_add = pricing_model.distance_add_tier2
        if(find_match(type1, day) == True):
            distance_base = pricing_model.distance_base_tier1
        elif(find_match(type2, day)):
            distance_base = pricing_model.distance_base_tier2
        elif(day == 'Sun'):
            distance_base = pricing_model.distance_base_tier3
            
    if(total_ridehours <= 1):
        tmf = pricing_model.tmf_tier1
    elif(total_ridehours > 1 and total_ridehours <= 2):
        tmf = pricing_model.tmf_tier2
    else:
        tmf = pricing_model.tmf_tier3
    
    initailwait = 3
    wc_price = 0
    if(waitingtime < initailwait):
        wc_price = total_ridehours*pricing_model.wc_tier1
    else:
        wc = total_ridehours/initailwait
        print(wc)
        wc_price = float(pricing_model.wc_tier2) * wc
    
    dap = distance_add * distance
    tmf_val = total_ridehours * float(tmf)
    
    print('distance_base', distance_base)
        
    totalprice = float(distance_base) + float(dap) + tmf_val + wc_price
    print(totalprice)
    
    table_data = {
        "username" :  username,
        "distance" : distance,
        "starttime": start_time,
        "endtime": end_time,
        "totalhours": total_ridehours,
        "wait": wait,
        "totalprice": totalprice
    }
    
    print(table_data)
    
    ride =  Ride()
    ride.username = username
    ride.distance = distance
    ride.starttime = str(start_time),
    ride.endtime = str(end_time),
    ride.totalhours = str(total_ridehours),
    ride.waittime = str(wait),
    ride.totalprice = totalprice
    ride.save()
    
    response_data = {
        "total-price": totalprice
    }
    
    return JsonResponse(response_data)

# Export Pricing Modal to CSV
def export_query_to_csv(request):
    data = Pricing.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pricing.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 
                     'Distance Base on (Tue, Wed, Thur)', 
                     'Distance Base on (Sat, Mon)',
                     'Distance Base on (Sun)',
                     'Distance Add (upto 3km)',
                     'Distance Add (after 3km)',
                     'TMF (upto 1hr)',
                     'TMF (upto 2hrs)',
                     'TMF (upto 3hrs)',
                     'Waiting Charges (upto 3mins)',
                     'Waiting Charges (after 3mins)',
                     'Created At',
                     'Created By',
                    ])  # CSV header

    for pricing in data:
        writer.writerow([pricing.name, 
                         pricing.distance_base_tier1, 
                         pricing.distance_base_tier2,
                         pricing.distance_base_tier3,
                         pricing.distance_add_tier1,
                         pricing.distance_add_tier2,
                         pricing.tmf_tier1,
                         pricing.tmf_tier2,
                         pricing.tmf_tier3,
                         pricing.wc_tier1,
                         pricing.wc_tier2,
                         pricing.created_at,
                         pricing.created_by
                         ])

    return response

def rides_list(request):  
    items = Ride.objects.all()  
    return render(request,"ride-list.html",{'items': items}) 

# Export All Rides to CSV
def export_rides_to_csv(request):
    data = Ride.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rides.csv"'

    writer = csv.writer(response)
    writer.writerow(['User Name', 
                     'Distance', 
                     'Start Time',
                     'End Time',
                     'Total Hours',
                     'Waiting Time',
                     'Total Price',
                    ])  # CSV header

    for ride in data:
        writer.writerow([ride.username, 
                         ride.distance,
                         ride.starttime,
                         ride.endtime,
                         ride.totalhours,
                         ride.waittime,
                         ride.totalprice,
                         ])
    return response