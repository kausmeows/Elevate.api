from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # Create new elevator systems
    path('system/add-system',CreateElevatorSystem.as_view(),name='add-elevator-sys'),
    # Show all the elevator systems
    path('system/show-all/',ElevatorSystemList.as_view(),name='show-all-sys'),
    # Show all elevators belonging to an elevator system
    path('system/<int:id>/show-elevators/',ElevatorsList.as_view(),name='elevator-list'),
    
    # Individual Elevators
    # Show
    path('system/<int:id>/elevator/<int:pk>/show/',ViewSingleElevator.as_view(),name='elevator-show'),
    #update
    path('system/<int:id>/elevator/<int:pk>/update/',UpdateSingleElevator.as_view(),name='elevator-update'),
    #Fetch destination
    path('system/<int:id>/elevator/<int:pk>/destination/',FetchDestination.as_view(),name='fetch-destination'),

    # Request to an elevator
    # post
    path('system/<int:id>/elevator/<int:pk>/make-request/',CreateElevatorRequest.as_view(),name='add-new-req'),
    #view
    path('system/<int:id>/elevator/<int:pk>/req-current-status/',ElevatorRequestList.as_view(),name='req-list'),
]
