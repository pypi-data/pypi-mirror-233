from . import TypeModel


class Event(TypeModel):
    base_path = "/events/"
    
    def __init__(
            self,
            title: str,
            id: int | None = None,
            additional_data: dict | None = None):
        """
            Initialize an Event object.

            :param title: The title of the event.
            :param id: The ID of the event (optional).
            :param additional_data: Additional data related to the event (optional).
        """
        self.id = id
        self.title = title
        self.additional_data = additional_data

    @classmethod
    def from_json(cls, event: dict):
        """
            Create an Event object from a JSON dictionary obtained from the API.

            :param event: JSON dictionary representing an event.

            :return: An Event object.
        """
        return cls(id=event["id"], title=event["title"], additional_data=event["additional_data"])

    @property
    def body(self) -> dict:
        """
            Get the data of the Event object in a dictionary format for API requests.

            :return: Dictionary representation of the Event object.
        """
        return dict(title=self.title, additional_data=self.additional_data)

    @property
    def params(self) -> dict:
        """
            Get query parameters for API requests (currently empty).

            :return: An empty dictionary.
        """
        return {}
