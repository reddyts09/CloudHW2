# Develop Restful Webservice to host weather information
This assignment requires us to add REST API endpoints to our application, to accept the input data as input parameters to either a GET or POST operation, that will return JSON result in plain-text to the user.

# Configuration Details:
1. To connect to the aws cloud service:
- ssh -i "red.pem" ubuntu@ec2-3-17-59-123.us-east-2.compute.amazonaws.com

2. After logging in:
- sudo apt-get update 
- sudo apt-get install python3-pip python3-dev python3-setuptools git
- sudo apt-get install language-pack-en
- sudo locale-gen en_GB.UTF-8

3. Install Django and djangorestframework
- pip3 install django
- pip3 install djangorestframework
- pip3 install django-import-export

4. Use git command to clone the project from github to var folder:
- sudo -i
- cd /var
- git clone https://github.com/reddyts09/cloud234.git

5. HW2 folder contains some files and their contents are as follows:
- apps.py:
  ```from django.apps import AppConfig
     class Hw2Config(AppConfig):
     name = 'hw2'
- models.py:
  ```from django.db import models
     class Book(models.Model):
     DATE = models.CharField(max_length=8, unique=True)
     TMAX = models.FloatField(default=0)
     TMIN = models.FloatField(default=0)
     class Meta:
        ordering = ('DATE'),
- serializers.py:
  ```from rest_framework import serializers
     from .models import Book
     class BookSerializer(serializers.ModelSerializer):
     class Meta:
        model = Book
        fields = ('DATE', 'TMAX', 'TMIN')
     class BookSerializer2(serializers.ModelSerializer):
     class Meta:
        model = Book
        fields = ('DATE',)
- urls.py:
  ```from django.urls import path
     from . import views
     #from django.views.decorators.csrf import csrf_exempt
     urlpatterns = [
     path('historical/', views.record_list),
     path('historical/<int:dt>/', views.record_detail),
     path('forecast/<int:dt>/', views.forecast),
     ]
- views.py:
  ```from django.shortcuts import render
     from hw2.models import Book
     from hw2.serializers import BookSerializer, BookSerializer2
     from rest_framework.decorators import api_view
     from rest_framework.response import Response
     from rest_framework import status
     import datetime
     from django.http import HttpResponse, JsonResponse
     from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def record_list(request):
    @api_view(['GET', 'POST'])
    def dummy1(request):
        if request.method == 'GET':
            record = Book.objects.all()
            ser_record = BookSerializer2(record, many=True)
            return Response(ser_record.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            copy1 = request.data.copy()
            q1 = Book.objects.filter(DATE=copy1['DATE'])
            if q1:
                q1.delete()
           
            ser_record = BookSerializer(data=request.data)
            if ser_record.is_valid():
                ser_record.save()
                return Response(ser_record.data, status=status.HTTP_201_CREATED)
            return Response(ser_record.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return dummy1(request)
    
    @api_view(['GET', 'DELETE'])
    def record_detail(request, dt):
    try:
        record = Book.objects.get(DATE=dt)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        ser_record = BookSerializer(record)
        return Response(ser_record.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
   @api_view(['GET'])
   def forecast(request, dt):
    list_date = [str(dt)]
    year = int(str(dt)[:4])
    month = int(str(dt)[4:6])
    day = int(str(dt)[6:8])
    given = datetime.date(year, month, day)
    for i in range(1,7):
        td = datetime.timedelta(i)
        ans = given+td
        
        year = str(ans.year)
        month = str(ans.month)
        day = str(ans.day)
        
        if len(month)==1:
            month = '0' + month
        if len(day)==1:
            day = '0' + day
        
        date_ans = year+month+day
        
        list_date.append(date_ans)
    
    list_ans = []
    for i in list_date:
        dict1 = {}
        record = Book.objects.filter(DATE=i)
        if record:
            list_ans.append({'DATE': record[0].DATE, 'TMAX': record[0].TMAX, 'TMIN': record[0].TMIN})
        else:
            id_pull = int(i)%2278
            while 1:
                record = Book.objects.filter(id=id_pull)
                if record:
                    list_ans.append({'DATE': i, 'TMAX': record[0].TMAX, 'TMIN': record[0].TMIN})
                    break
                else:
                    id_pull += 1
                    if id_pull > 2277:
                        id_pull = 1
            
    ser_record_final = BookSerializer(list_ans, many=True)
    return Response(ser_record_final.data, status=status.HTTP_200_OK)
    
6. The main cloud234 contains the file urls.py and its contents are as follows:
   ```from django.contrib import admin
      from django.urls import path, include
      #from django.views.decorators.csrf import csrf_exempt
      from rest_framework_swagger.views import get_swagger_view

      schema_view =  get_swagger_view(title = "WeatherAPI")

      urlpatterns = [
    
      path('', include('hw3.urls')),
      path('admin/', admin.site.urls),
      path('', include('hw2.urls')),
      path('swagger/', schema_view),
      ]

7. To access the REST API Endpoints we use:
- For /historical :
  ```
  http://ec2-3-17-59-123.us-east-2.compute.amazonaws.com/historical
- For /historical/YYYYMMDD:
  ```
  http://ec2-3-17-59-123.us-east-2.compute.amazonaws.com/historical/20130202
- For /forecast/YYYYMMDD:
  ```
  http://ec2-3-17-59-123.us-east-2.compute.amazonaws.com/forecast/20130209

# Built With
- Django,AWS: Web Framework used
- JSON, Python, XML: Development Applications used
- Restful WebServices: To develop the API's
- Database: sqlite3
- Github: repository for code

# Acknowledgements
I Thank Prof.Giridhar for provding me with the opportunity to work on this project that deals with hands on experience with Cloud, AWS, Resful API and Django framework.
