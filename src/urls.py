from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # Create new elevator systems
    path('elevate/add-system',CreateElevatorSystem.as_view(),name='add-elevator-sys'),
]
