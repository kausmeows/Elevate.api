## Model Wise API Endpoints

## Elevator System

Elevator system Model. Equivalent to a building containing a number of elevators Also contains the default ID parameter assigned by django as a primary key. Used to make the project compatible with multiple elevator systems. Minimum floor is assumed as 0 but dynamic minimum floor can be implemented easily.


`GET api/system/show-all/`
View all the elevator systems

#### Response Example
```
200
[
  {
    "id": 0,
    "system_name": "string",
    "total_floors": 0,
    "number_of_elevators": 0
  }
]
```


`POST api/system/add-system/`
Create a new elevator system.

#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
system_name         - required  -----> string (System name) [ 1 .. 20 ] characters
total_floors           - required  ----->integer (Max floor)
number_of_elevators - required  -----> integer (Number of elevators)
```

#### Response Example
```
200
{
  "id": 0,
  "system_name": "string",
  "max_floor": 0,
  "number_of_elevators": 0
}
```

## Elevator
Elevator object model. Represents a single elevator that can move up and down. It is always a part of an entire elevator system. So elevator system is assigned as foreignkey.

`GET api/system/{elevator-system-id}/show-elevators/`
Given an elevator system list all the elevators and their status.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
```

#### Response Example
```
200
[
  {
    "id": 0,
    "elevator_number": 0,
    "current_floor": 0,
    "is_operational": true,
    "is_door_open": true,
    "running_status": 1,
    "elevator_system": 0
  }
]

```

`GET api/system/{elevator-system-id}/elevator/{elevator-number}/show/`
Get details of a specific elevator, given its elevator system id and elevator number with URL

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```

#### Response Example
```
200
{
  "id": 0,
  "elevator_number": 0,
  "current_floor": 0,
  "is_operational": true,
  "is_door_open": true,
  "running_status": 1,
  "elevator_system": 0
}

```

`PUT/PATCH api/system/{elevator-system-id}/elevator/{elevator-number}/update/`
Update details of a specific elevator, given its elevator system and elevator number with URL It can be done together with the previous view, but repeated for better understanding.Put is not a recomended method, so the put method is overridden by patch in the back-end. But while sending requests you can use any of them.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
elevator_number   - required integer (Elevator number)
current_floor	    - integer (Current floor)
is_operational	  - boolean (Is operational)
is_door_open	    - boolean (Is door open)
running_status	  - integer (Running status)Expected numbers : (1 , 0 , -1)
elevator_system   - required integer (Elevator system)
```
#### Response Example
```
200
{
  "elevator_number": 0,
  "current_floor": 0,
  "is_operational": true,
  "is_door_open": true,
  "running_status": 1,
  "elevator_system": 0
}
```

`GET api/system/{elevator-system-id}/elevator/{elevator-number}/destination/`
Fetch the next destination floor for a given elevator

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```

#### Response Example
```
200
{
  'running' : True/False,
  'details' : Number representing the next destination / String representing the current status if not running
}

```

## Elevator Request
User request targeted to a specific elevator. This can be improved further using model managers  to clean the invalid requests like request elevator in negative floor greater than maximum floor request an elevator that doesn't exist.

`GET api/system/{elevator-system-id}/elevator/{elevator-number}/req-current-status/`
List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Params
```
is_active ----> False/0 ---> All the processed requests by the elevator(False is case insensitive)
is_active ----> True/1 ---> All the pending requests by the elevator(True is case insensitive)
```
#### Response Example
```
200
[
  {
    "id": 0,
    "requested_floor": 0,
    "destination_floor": 0,
    "request_time": "2019-08-24T14:15:22Z",
    "is_active": true,
    "elevator": 0
  }
]
```
`POST api/system/{elevator-system-id}/elevator/{elevator-number}/make-request/`
Create a new request for a specific elevator, given its elevator system and elevator number with URL. The inputs of requested and destinatiom floor is sent with the form-data.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
requested_floor       - required integer 
destination_floor	    - required integer
```
#### Response Example
```
201
{
  "requested_floor": 0,
  "destination_floor": 0
}
```
