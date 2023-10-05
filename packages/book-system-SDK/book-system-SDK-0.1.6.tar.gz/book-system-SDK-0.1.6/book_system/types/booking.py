import datetime

from . import TypeModel
from .events import Event
from .rooms import Room


class Booking(TypeModel):
    base_path = "/booking/"
    def __init__(
            self, 
            time_start: datetime.datetime,
            time_finish: datetime.datetime, 
            event_id: int | None = None,
            room_id: int | None = None,
            event: Event | None = None,
            room: Room | None = None,
            id: int | None = None,
            additional_data: dict | None = None):
        """
            Initialize a Booking object.

            :param time_start: The start time of the booking as a datetime object.
            :param time_finish: The end time of the booking as a datetime object.
            :param event_id: The ID of the associated event (optional).
            :param room_id: The ID of the associated room (optional).
            :param event: An Event object associated with the booking (optional).
            :param room: A Room object associated with the booking (optional).
            :param id: The ID of the booking (optional).
            :param additional_data: Additional data related to the booking (optional).

            :raises ValueError: If event and room instances are not provided and event_id or room_id is missing.
        """
        
        self.id = id
        if (not event or not room) and (not event_id or not room_id):
            raise ValueError("You should pass event and room instances or their IDs")
        self.event = event
        self.room = room
        self.event_id = event_id
        self.room_id = room_id
        self.time_start = time_start
        self.time_finish = time_finish
        self.additional_data = additional_data

    @classmethod
    def from_json(cls, booking: dict):
        """
            Create a Booking object from a JSON dictionary obtained from the API.

            :param booking: JSON dictionary representing a booking.

            :return: A Booking object.
        """
        return cls(
            id=booking["id"],
            event_id=booking["event_id"], 
            room_id=booking["room_id"], 
            time_start=datetime.datetime.fromisoformat(booking["time_start"]), 
            time_finish=datetime.datetime.fromisoformat(booking["time_finish"]),
            additional_data=booking["additional_data"])

    @property
    def body(self):
        """
            Get the data of the Booking object in a dictionary format for API requests.

            Note: This method may cause an error if the associated room or event is not saved in the database.

            :return: Dictionary representation of the Booking object.
        """
        return dict(
            time_start=self.time_start.isoformat(),
            time_finish=self.time_finish.isoformat(), 
            additional_data=self.additional_data,
            room_id=self.room.id if self.room else self.room_id,
            event_id=self.event.id if self.event else self.event_id)

    @property
    def params(self) -> dict:
        """
            Get query parameters for API requests (currently empty).

            :return: An empty dictionary.
        """
        return {}
