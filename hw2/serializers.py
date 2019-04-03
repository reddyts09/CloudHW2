from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('DATE', 'TMAX', 'TMIN')
        
class BookSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('DATE',)