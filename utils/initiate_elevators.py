# Import required model
from src.models import Elevator

def initiate_elevators(number_of_elevators: int, system_id: int):
    print(f"Initiating {number_of_elevators} elevators for system {system_id}")
    for i in range(number_of_elevators):
        elevator_object = Elevator.objects.create(
            elevator_system_id=system_id,
            elevator_number=i + 1,
        )
        print(f"Created elevator {elevator_object.elevator_number} for system {system_id}")
    print("Elevator initiation completed")
