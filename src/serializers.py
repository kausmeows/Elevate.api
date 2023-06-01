from rest_framework import serializers
from .models import ElevatorSystem, Elevator, ElevatorRequest


class ElevatorSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorSystem
        fields = '__all__'


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = ('requested_floor', 'destination_floor')


class ElevatorRequestFullSerializer(serializers.ModelSerializer):
    current_floor = serializers.SerializerMethodField()
    class Meta:
        model = ElevatorRequest
        fields = (
            'id',
            'current_floor',
            'requested_floor',
            'destination_floor',
            'request_time',
            'is_active',
            'elevator',
        )
        
    def get_current_floor(self, obj):
        return obj.elevator.current_floor
