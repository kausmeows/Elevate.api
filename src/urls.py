from django.contrib import admin
from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter
from .views import ElevatorSystemViewSet, ElevatorViewSet

router = DefaultRouter()
router.register(r'system', ElevatorSystemViewSet, basename='system')

urlpatterns = [
    path('system/<int:pk>/show_elevators/', ElevatorSystemViewSet.as_view({'get': 'show_elevators'}), name='elevator-system-show-elevators'),
    path('system/<int:id>/elevator/<int:pk>/', ElevatorViewSet.as_view({'get': 'show', 'put': 'custom_update', 'patch': 'custom_update'}), name='elevator-show'),
    path('system/<int:id>/elevator/<int:pk>/make_request/', ElevatorViewSet.as_view({'post': 'make_request'}), name='elevator-make-request'),
    path('system/<int:id>/elevator/<int:pk>/destination/', ElevatorViewSet.as_view({'get': 'destination'}), name='elevator-destination'),
    path('system/<int:id>/elevator/<int:pk>/req_current_status/', ElevatorViewSet.as_view({'get': 'req_current_status'}), name='elevator-req-current-status'),
] + router.urls

'''
URLs:-
GET/POST: api/system- show all elevator systems or add an elevator system

GET: api/system/{elevator-system-id}/show_elevators- Given an elevator system list all the elevators and their status.

GET/PUT: api/system/{elevator-system-id}/elevator/{elevator-number}/- view and update the details of any elevator of the system

POST: api/system/{elevator-system-id}/elevator/{elevator-number}/make_request- Create a new request for a specific elevator, given its elevator system and elevator number

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/destination- Fetch the next destination floor for a given elevator

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/req_current_status- List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.
'''