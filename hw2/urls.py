from django.urls import path
from . import views
#from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('historical/', views.record_list),
    path('historical/<int:dt>/', views.record_detail),
    path('forecast/<int:dt>/', views.forecast),
    ]
