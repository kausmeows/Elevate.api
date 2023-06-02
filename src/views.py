from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Elevator, ElevatorRequest, ElevatorSystem
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ElevatorRequestFullSerializer, ElevatorRequestSerializer, ElevatorSerializer, ElevatorSystemSerializer
from utils.initiate_elevators import initiate_elevators


class ElevatorSystemList(generics.ListAPIView):
	'''
	This is a Django REST framework API view that lists all instances of the ElevatorSystem model using
	the ElevatorSystemSerializer for serialization.
	'''
	queryset = ElevatorSystem.objects.all()
	serializer_class = ElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
	"""
	This function creates an elevator system and initiates the elevators associated with it.
		
	:param serializer: The serializer is an instance of the ElevatorSystemSerializer class, which is
	responsible for converting the data received in the request into a Python object and vice versa
	"""
	serializer_class = ElevatorSystemSerializer
  
	def perform_create(self, serializer):
		elevator_system = serializer.save()

		initiate_elevators(
			number_of_elevators=serializer.data['number_of_elevators'],
			system_id=elevator_system.id
		)
		
class ElevatorsList(generics.ListAPIView):
	"""
	This function returns a queryset of Elevator objects filtered by the elevator system ID passed
	as a parameter.
 
	:return: The `get_queryset` method is returning a queryset of `Elevator` objects filtered by the
	`id` of the `elevator_system` associated with the `Elevator` objects. The serializer class used
	to serialize the queryset is `ElevatorSerializer`.
	"""
	serializer_class = ElevatorSerializer

	def get_queryset(self):
		system_id = self.kwargs['id']
		queryset = Elevator.objects.filter(elevator_system__id = system_id)

		return queryset

class ViewSingleElevator(generics.RetrieveAPIView):
	"""
	This function retrieves a specific Elevator object based on the system ID and elevator number
	provided in the URL.
 
	:return: The `get_object` method is returning a single `Elevator` object that matches the
	`system_id` and `elevator_number` specified in the URL. The method first filters the `Elevator`
	queryset based on these parameters and then returns the first object in the resulting queryset.
	"""
	serializer_class = ElevatorSerializer

	def get_object(self):
		system_id = self.kwargs['id']
		elevator_number = self.kwargs['pk']

		queryset = Elevator.objects.filter(
		elevator_system__id = system_id,
		elevator_number = elevator_number
		)

		return queryset[0]
	
class UpdateSingleElevator(generics.UpdateAPIView):
	"""
	This function retrieves a specific Elevator object based on the system ID and elevator number
	provided in the URL.
 
	:return: The `get_object` method is returning a single `Elevator` object that matches the
	`system_id` and `elevator_number` specified in the URL. The method first filters the `Elevator`
	queryset based on these parameters and then returns the first object in the resulting queryset.
	"""
	serializer_class = ElevatorSerializer

	def get_object(self):
		system_id = self.kwargs['id']
		elevator_number = self.kwargs['pk']

		queryset = Elevator.objects.filter(
		elevator_system__id = system_id,
		elevator_number = elevator_number
		)

		return queryset[0]

	#overriding put method by patch
	def put(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)
	
	
class CreateElevatorRequest(generics.CreateAPIView):
	"""
	This function overrides the perform_create method to save an elevator object based on system_id
	and elevator_number.
		
	:param serializer: The serializer is an instance of the ElevatorRequestSerializer class, which
	is used to convert the request data into a format that can be saved to the database
	"""
	serializer_class = ElevatorRequestSerializer

	# Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
	def perform_create(self, serializer):
		system_id = self.kwargs['id']
		elevator_number = self.kwargs['pk']

		queryset = Elevator.objects.filter(
		elevator_system__id = system_id,
		elevator_number = elevator_number
		)
		elevator_object = queryset[0]

		serializer.save(elevator = elevator_object)
		

class ElevatorRequestList(generics.ListAPIView):
	"""
	This function returns a filtered queryset of ElevatorRequest objects based on the elevator
	system ID and elevator number provided in the URL.
		
  	:return: The `get_queryset` method is returning a filtered queryset of `ElevatorRequest`
	objects that are associated with a specific `Elevator` object. The `Elevator` object is
	identified by the `system_id` and `elevator_number` parameters passed in the URL. The queryset
	is filtered using the `filter` method to only include `ElevatorRequest` objects that have a
	foreign key
	"""
	serializer_class = ElevatorRequestFullSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['is_active']

	def get_queryset(self):
		system_id = self.kwargs['id']
		elevator_number = self.kwargs['pk']

		elevator_object = Elevator.objects.filter(
		elevator_system__id = system_id,
		elevator_number = elevator_number
		)

		queryset = ElevatorRequest.objects.filter(elevator = elevator_object[0])
		return queryset


class FetchDestination(APIView):
	"""
	This function retrieves information about a specific elevator and its pending requests.
		
	:param request: The HTTP request object
	:param id: The id parameter is used to identify the elevator system to which the elevator belongs
	:param pk: The "pk" parameter is a variable that stands for "primary key". It is commonly used in 
 			   Django to refer to the unique identifier of a database record. In this specific code snippet,
			   "pk" is used to represent the elevator number.
		
	:return: a Response object containing a dictionary with keys 'running' and 'details'. The value
			 of 'running' is a boolean indicating whether the elevator is currently running or not, and the
			 value of 'details' provides additional information about the elevator's status.
	"""
	def get(self, request, id, pk):
		system_id = id
		elevator_number = pk

		elevator_object = Elevator.objects.filter(
		elevator_system__id = system_id,
		elevator_number = elevator_number
		)

		requests_pending = ElevatorRequest.objects.filter(
		elevator = elevator_object[0],
		is_active = True,
		).order_by('request_time')

		return_dict = {

		}

		if elevator_object.count() !=1:
			return_dict = {
				'running' : False,
				'details' : 'The Elevator number is incorrect'
			}
		
		elif not elevator_object[0].is_operational:
			return_dict = {
				'running' : False,
				'details' : 'The Elevator is not operational'
			}
			
		elif requests_pending.count() == 0:
			return_dict = {
				'running' : False,
				'details' : 'The Elevator is not running currently, No pending requests'
			}
			
		elif requests_pending[0].requested_floor == elevator_object[0].current_floor:
			return_dict = {
				'running' : True,
				'details' : str(requests_pending[0].destination_floor)
			}
			
		else:
			return_dict = {
				'running' : True,
				'details' : str(requests_pending[0].requested_floor)
			}

		return Response(return_dict)