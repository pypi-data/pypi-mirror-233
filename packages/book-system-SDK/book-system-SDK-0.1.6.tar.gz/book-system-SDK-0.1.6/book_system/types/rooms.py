from .seats import Seat
from . import TypeModel


class Room(TypeModel):
    base_path = "/rooms/"
    def __init__(
            self, 
            id: int | None = None,
            name: str | None = None, 
            seats: list[Seat] | None = None,
            additional_data: dict | None = None,
            autogenerate_seats: bool = False, 
            columns: int | None = None,
            rows: int | None = None):
        """
            Initialize a Room object.

            :param id: The ID of the room (optional).
            :param name: The name of the room (optional).
            :param seats: A list of Seat objects associated with the room (optional).
            :param additional_data: Additional data related to the room (optional).
            :param autogenerate_seats: Whether to automatically generate seats (default is False).
            :param columns: The number of columns for seat generation (optional).
            :param rows: The number of rows for seat generation (optional).

            :raises ValueError: If autogenerate_seats is True but columns or rows are not provided.
        """
        
        if autogenerate_seats and (not columns or not rows):
            raise ValueError("If you want to use autogenerate you should pass the number of columns and rows")
        self.id = id
        self.name = name
        self.columns = columns
        self.rows = rows
        self.seats = seats
        self.autogenerate_seats = autogenerate_seats
        self.additional_data = additional_data

    @classmethod
    def from_json(cls, room: dict):
        """
            Create a Room object from a JSON dictionary obtained from the API.

            :param room: JSON dictionary representing a room.

            :return: A Room object.
        """
        seats = room.get("seats")
        seats = [Seat.from_json({**seat}) for seat in seats] if seats else None
        return cls(id=room["id"], name=room["name"], seats=seats, additional_data=room["additional_data"])

    @property
    def body(self) -> dict:
        """
            Get the data of the Room object in a dictionary format for API requests.
            :return: Dictionary representation of the Room object.
        """
        seats_dict = [seat.body for seat in self.seats] if self.seats else None
        return dict(
            name=self.name, 
            additional_data=self.additional_data,
            seats=seats_dict
        )

    @property
    def params(self) -> dict:
        """
            Get query parameters for API requests.

            :return: Dictionary with autogenerate, columns, and rows parameters.
        """
        return dict(
            autogenerate=self.autogenerate_seats, 
            columns=self.columns, 
            rows=self.rows
        )
