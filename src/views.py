from rest_framework import generics

from .models import Elevator, ElevatorSystem

from .serializers import ElevatorSerializer, ElevatorSystemSerializer
from utils.initiate_elevators import initiate_elevators


class ElevatorSystemList(generics.ListAPIView):
    queryset = ElevatorSystem.objects.all()
    serializer_class = ElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
    serializer_class = ElevatorSystemSerializer

    def perform_create(self, serializer):
        elevator_system = serializer.save()

        initiate_elevators(
            number_of_elevators=serializer.data['number_of_elevators'],
            system_id=elevator_system.id
        )
        
class ElevatorsList(generics.ListAPIView):
    serializer_class = ElevatorSerializer

    def get_queryset(self):
        system_id = self.kwargs['id']
        queryset = Elevator.objects.filter(elevator_system__id = system_id)

        return queryset

class ViewSingleElevator(generics.RetrieveAPIView):
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