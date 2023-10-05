# book-system-SDK
## Introduction
The Book-System SDK is a powerful tool designed to simplify the integration of the Book-System API into your application. This SDK streamlines the process of accessing and utilizing the API's features, making it easy for developers to incorporate event management, room configuration, and seat booking functionality into their software solutions.

## Key Features
- Easy Integration: The SDK provides a straightforward and developer-friendly interface for interacting with the Book-System API. You can quickly integrate booking capabilities into your application without the need for complex API calls.

- Event Management: Effortlessly create, retrieve, and manage events in your venue. The SDK abstracts away the intricacies of event handling, allowing you to focus on providing a seamless booking experience to your users.

- Room Configuration: Easily configure and manage rooms to suit various event types. Whether you're dealing with theaters, cinemas, or any other venue, this SDK has you covered in adapting room setups to your needs.

- Seat Booking: Simplify the seat booking process by using the SDK's intuitive methods. Your users can enjoy a hassle-free experience when reserving seats for their chosen events.

## Installation

You can install SDK using pip:

```
pip install book-system-sdk
```

## Examples

### Example 1: Creating a Room and Fetching Room Details
```python

from your_module import BookSystemSDK, Room

# Initialize the BookSystemSDK with the API URL
sdk = BookSystemSDK(api_url="https://example.com/api")

# Create a new room
new_room = Room(name="Conference Room A", columns=5, rows=10)
created_room = sdk.create(new_room)
print("Created Room:", created_room.name)

# Fetch room details by ID
room_id_to_fetch = created_room.id
fetched_room = sdk.get(model=Room, by_id=room_id_to_fetch)
print("Fetched Room:", fetched_room.name)
```
### Example 2: Creating an Event and Fetching Event Details
```python

from your_module import BookSystemSDK, Event

# Initialize the BookSystemSDK with the API URL
sdk = BookSystemSDK(api_url="https://example.com/api")

# Create a new event
new_event = Event(title="Product Launch")
created_event = sdk.create(new_event)
print("Created Event:", created_event.title)

# Fetch event details by ID
event_id_to_fetch = created_event.id
fetched_event = sdk.get(model=Event, by_id=event_id_to_fetch)
print("Fetched Event:", fetched_event.title)
```
### Example 3: Booking a Seat for an Event
```python

from your_module import BookSystemSDK, Booking, Event, Room

# Initialize the BookSystemSDK with the API URL
sdk = BookSystemSDK(api_url="https://example.com/api")

# Fetch an event and room to book
event_to_book = sdk.get(model=Event, by_id=1)
room_to_book = sdk.get(model=Room, by_id=2)

# Define booking details
booking_start = datetime.datetime(2023, 9, 30, 10, 0)
booking_end = datetime.datetime(2023, 9, 30, 12, 0)

# Create a booking
new_booking = Booking(
    time_start=booking_start,
    time_finish=booking_end,
    event=event_to_book,
    room=room_to_book
)
created_booking = sdk.create(new_booking)
print("Created Booking ID:", created_booking.id)
```

The `BookSystemSDK` class provides an interface for interacting with a booking system API. It allows you to manage rooms, events, and bookings within the system.

## Constructor
### `__init__(self,api_url: str, rooms: List[Room] | None = None, events: List[Event] | None = None, booking: List[Booking] | None = None)`

- `api_url` (str): The base URL of the API.
- `rooms` (List[Room] | None): Optional initial list of Room objects.
- `events` (List[Event] | None): Optional initial list of Event objects.
- `booking` (List[Booking] | None): Optional initial list of Booking objects.

## Properties
### `rooms`

- Returns a list of Room objects fetched from the API.

### `events`

- Returns a list of Event objects fetched from the API.

### `booking`

- Returns a list of Booking objects fetched from the API.

## Methods

### `create(self, obj: TypeModel) -> TypeModel`

- Creates a new object of the specified type in the API.

### `refresh(self, obj: TypeModel) -> TypeModel`

- Refreshes the data of an existing object in the API.

### `delete(self, obj: TypeModel | List[TypeModel]) -> None`

- Deletes an object or a list of objects from the API.

### `get(self, model: TypeModel, by: TypeModel | None = None, by_id: int | None = None,  **kwargs) -> TypeModel`

- Retrieves an object from the API based on specified filters and parameters.

### `_make_request(self, url: str, method: Literal["GET", "POST", "PATCH", "DELETE"], body: dict | None = None, params: dict | None = None) -> dict`

- Makes an HTTP request to the API and handles responses.

# Seat Documentation

The `Seat` class represents a seat in a room and provides methods to interact with seat data.

## Constructor
### `__init__(self, row: int, column: int, number: int, booked: bool = False, id: int | None = None, additional_data: dict | None = None)`

- `row` (int): The row number of the seat.
- `column` (int): The column number of the seat.
- `number` (int): The seat number.
- `booked` (bool): Whether the seat is booked (default is False).
- `id` (int | None): The ID of the seat (optional).
- `additional_data` (dict | None): Additional data related to the seat (optional).

## Class Methods
### `from_json(cls, seat: dict)`

- Creates a Seat object from a JSON dictionary obtained from the API.

## Properties
### `room`

- TODO: A property that is intended to fetch the room associated with the seat in the database. (To be implemented)

### `body`

- Returns the data of the Seat object in a dictionary format for API requests.

### `params`

- Returns query parameters for API requests (currently empty).

# Room Documentation

The `Room` class represents a room in the booking system and provides methods to interact with room data.

## Constructor
### `__init__(self, id: int | None = None, name: str | None = None, seats: list[Seat] | None = None, autogenerate_seats: bool = False, columns: int | None = None, rows: int | None = None)`

- `id` (int | None): The ID of the room (optional).
- `name` (str | None): The name of the room (optional).
- `seats` (list[Seat] | None): A list of Seat objects associated with the room (optional).
- `autogenerate_seats` (bool): Whether to automatically generate seats (default is False).
- `columns` (int | None): The number of columns for seat generation (optional).
- `rows` (int | None): The number of rows for seat generation (optional).

## Class Methods
### `from_json(cls, room: dict)`

- Creates a Room object from a JSON dictionary obtained from the API.

## Properties
### `body`

- Returns the data of the Room object in a dictionary format for API requests.

### `params`

- Returns query parameters for API requests.

# Event Documentation

The `Event` class represents an event in the booking system and provides methods to interact with event data.

## Constructor
### `__init__(self, title: str, id: int | None = None, additional_data: dict | None = None)`

- `title` (str): The title of the event.
- `id` (int | None): The ID of the event (optional).
- `additional_data` (dict | None): Additional data related to the event (optional).

## Class Methods
### `from_json(cls, event: dict)`

- Creates an Event object from a JSON dictionary obtained from the API.

## Properties
### `body`

- Returns the data of the Event object in a dictionary format for API requests.

### `params`

- Returns query parameters for API requests (currently empty).

# Booking Documentation

The `Booking` class represents a booking in the booking system and provides methods to interact with booking data.

## Constructor
### `__init__(self, time_start: datetime.datetime, time_finish: datetime.datetime, event_id: int | None = None, room_id: int | None = None, event: Event | None = None, room: Room | None = None, id: int | None = None, additional_data: dict | None = None)`

- `time_start` (datetime.datetime): The start time of the booking.
- `time_finish` (datetime.datetime): The end time of the booking.
- `event_id` (int | None): The ID of the associated event (optional).
- `room_id` (int | None): The ID of the associated room (optional).
- `event` (Event | None): An Event object associated with the booking (optional).
- `room` (Room | None): A Room object associated with the booking (optional).
- `id` (int | None): The ID of the booking (optional).
- `additional_data` (dict | None): Additional data related to the booking (optional).

## Class Methods
### `from_json(cls, booking: dict)`

- Creates a Booking object from a JSON dictionary obtained from the API.

## Properties
### `body`

- Returns the data of the Booking object in a dictionary format for API requests.

### `params`

- Returns query parameters for API requests (currently empty).
