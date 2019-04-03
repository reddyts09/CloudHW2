from django.db import models

# Create your models here.
class Book(models.Model):
    DATE = models.CharField(max_length=8, unique=True)
    TMAX = models.FloatField(default=0)
    TMIN = models.FloatField(default=0)
    
    class Meta:
        ordering = ('DATE'),