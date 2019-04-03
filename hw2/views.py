from django.shortcuts import render
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
