from django.contrib import admin
from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter
from .views import ElevatorSystemViewSet, ElevatorViewSet

router = DefaultRouter()
router.register(r'system', ElevatorSystemViewSet, basename='system')
router.register(r'system/(?P<id>\d+)/elevator', ElevatorViewSet, basename='elevator')
urlpatterns = router.urls

'''
URLs:-
GET/POST: api/system- show all elevator systems or add an elevator system

GET: api/system/{elevator-system-id}/show_elevators- Given an elevator system list all the elevators and their status.

GET/PUT: api/system/{elevator-system-id}/elevator/{elevator-number}/- view and update the details of any elevator of the system

POST: api/system/{elevator-system-id}/elevator/{elevator-number}/make_request- Create a new request for a specific elevator, given its elevator system and elevator number

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/destination- Fetch the next destination floor for a given elevator

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/req_current_status- List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.
'''