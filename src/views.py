from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import Elevator, ElevatorRequest, ElevatorSystem
from .serializers import ElevatorRequestFullSerializer, ElevatorRequestSerializer, ElevatorSerializer, ElevatorSystemSerializer
from utils.initiate_elevators import initiate_elevators

class ElevatorSystemViewSet(viewsets.ModelViewSet):
    """
        This is a Django view that creates an elevator system and initiates elevators, and also shows
        the elevators associated with a particular elevator system.
        
        :param request: The HTTP request object that contains information about the request being made,
        such as the HTTP method, headers, and data
        :return: The code is a part of a Django REST framework viewset.
    """
    queryset = ElevatorSystem.objects.all()
    serializer_class = ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        elevator_system = serializer.save()
        initiate_elevators(
            number_of_elevators=serializer.data['number_of_elevators'],
            system_id=elevator_system.id
        )
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def show_elevators(self, request, pk=None):
        system_id = self.kwargs['pk']
        elevators = Elevator.objects.filter(elevator_system_id=system_id)
        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data)


class ElevatorViewSet(viewsets.ModelViewSet):
    """
        This is a Django viewset for managing Elevator objects, with actions for showing, updating,
        getting destination, getting current status of requests, making requests, and getting the
        appropriate serializer class.
        :return: This code is defining several custom actions for a viewset for the `Elevator` model.
        The `queryset` and `serializer_class` attributes are also defined.
    """
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['get'])
    def show(self, request, id=None, pk=None):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.get(elevator_system_id=system_id, elevator_number=elevator_number)
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)


    @action(detail=True, methods=['put', 'patch'])
    def custom_update(self, request, id=None, pk=None):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.get(elevator_system__id=system_id, elevator_number=elevator_number)
        serializer = ElevatorSerializer(elevator, data=request.data, partial=True)  # `partial=True` allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    @action(detail=True, methods=['get'])
    def destination(self, request, id=None, pk=None):
        elevator = self.get_object()

        if not elevator.is_operational:
            return Response({'running': False, 'details': 'The Elevator is not operational'})

        requests_pending = ElevatorRequest.objects.filter(elevator=elevator, is_active=True).order_by('request_time')

        if requests_pending.count() == 0:
            return Response({'running': False, 'details': 'The Elevator is not running currently, No pending requests'})

        if requests_pending[0].requested_floor == elevator.current_floor:
            return Response({'running': True, 'details': str(requests_pending[0].destination_floor)})

        return Response({'running': True, 'details': str(requests_pending[0].requested_floor)})

        
    @action(detail=True, methods=['get'])
    def req_current_status(self, request, id=None, pk=None):
        elevator = self.get_object()
        elevator_requests = elevator.elevatorrequest_set.all()
        serializer = ElevatorRequestFullSerializer(elevator_requests, many=True)
        return Response(serializer.data)

    
    @action(detail=True, methods=['post'])
    def make_request(self, request, id=None, pk=None):
        elevator = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(elevator=elevator)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def get_serializer_class(self):
        if self.action == 'make_request':
            return ElevatorRequestSerializer
        return super().get_serializer_class()
