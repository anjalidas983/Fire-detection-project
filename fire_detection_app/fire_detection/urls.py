from django.urls import path
from . import views

urlpatterns = [

    path('',views.fire_detection,name='fire_detection'),
]
