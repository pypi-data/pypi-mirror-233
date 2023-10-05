from . import TypeModel


class Seat(TypeModel):
    base_path = "/seats/"

    def __init__(
            self,
            row: int,
            column: int,
            number: int,
            booked: bool = False,
            id: int | None = None,
            additional_data: dict | None = None):
        """
            Initialize a Seat object.

            :param row: The row number of the seat.
            :param column: The column number of the seat.
            :param number: The seat number.
            :param booked: Whether the seat is booked (default is False).
            :param id: The ID of the seat (optional).
            :param additional_data: Additional data related to the seat (optional).
        """
        self.id = id
        self.row = row
        self.column = column
        self.number = number
        self.booked = booked
        self.additional_data = additional_data

    @classmethod
    def from_json(cls, seat: dict):
        """
            Create a Seat object from a JSON dictionary obtained from the API.

            :param seat: JSON dictionary representing a seat.

            :return: A Seat object.
        """
        return cls(
            id=seat["id"],
            row=seat["row"], 
            column=seat["column"], 
            number=seat["number"], 
            booked=seat["booked"], 
            additional_data=seat["additional_data"]
        )

    @property
    def body(self) -> dict:
        """
            Get the data of the Seat object in a dictionary format for API requests.

            :return: Dictionary representation of the Seat object.
        """
        return dict(
            row=self.row,
            column=self.column, 
            number=self.number, 
            booked=self.booked, 
            additional_data=self.additional_data
        )

    @property
    def params(self) -> dict:
        """
            Get query parameters for API requests (currently empty).

            :return: An empty dictionary.
        """
        return {}
