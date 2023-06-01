from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # Create new elevator systems
    path('elevate/add-system',CreateElevatorSystem.as_view(),name='add-elevator-sys'),
    # Show all the elevator systems
    path('elevate/show-all/',ElevatorSystemList.as_view(),name='show-all-sys'),
    # Show all elevators belonging to an elevator system
    path('elevate/<int:id>/show/',ElevatorsList.as_view(),name='elevator-list'),
    
    # Individual Elevators
    # Show
    path('elevate/<int:id>/elevator/<int:pk>/show/',ViewSingleElevator.as_view(),name='elevator-show'),
    #update
    path('elevate/<int:id>/elevator/<int:pk>/update/',UpdateSingleElevator.as_view(),name='elevator-update'),

]
