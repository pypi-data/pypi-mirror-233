import requests
from typing import Literal

from .types import TypeModel
from .types.rooms import Room
from .types.events import Event
from .types.booking import Booking


class BookSystemSDK:
    def __init__(
            self,
            api_url: str,
            rooms: list[Room] | None = None,
            events: list[Event] | None = None,
            booking: list[Booking] | None = None):
        """
            Initialize the BookSystemSDK.

            :param api_url: The base URL for the API.
            :param rooms: A list of Room objects (optional).
            :param events: A list of Event objects (optional).
            :param booking: A list of Booking objects (optional).
        """
        self.api_url = api_url
        self._rooms = rooms
        self._events = events
        self._booking = booking
    
    @property
    def rooms(self) -> list[Room]:
        """
            Get a list of Room objects from the API.

            :return: A list of Room objects.
        """
        if not self._rooms:
            url = f"{self.api_url}/rooms/"
            self._rooms = [Room.from_json(room) for room in self._make_request(url=url, method="GET")]
        return self._rooms

    @property
    def events(self) -> list[Event]:
        """
            Get a list of Event objects from the API.

            :return: A list of Event objects.
        """
        if not self._events:
            url = f"{self.api_url}/events/"
            self._events = [Event.from_json(event) for event in self._make_request(url=url, method="GET")]
        return self._events
    
    @property
    def booking(self) -> list[Booking]:
        """
            Get a list of Booking objects from the API.

            :return: A list of Booking objects.
        """
        if not self._booking:
            url = f"{self.api_url}/booking/"
            self._booking = [Booking.from_json(booking) for booking in self._make_request(url=url, method="GET")]
        return self._booking

    def _make_request(
            self,
            url: str,
            method: Literal["GET", "POST", "PATCH", "DELETE"],
            body: dict | None = None,
            params: dict | None = None) -> dict:
        """
            Make an HTTP request to the API.

            :param url: The URL to make the request to.
            :param method: The HTTP method for the request.
            :param body: The request body data (optional).
            :param params: Query parameters for the request (optional).

            :return: The JSON response from the API.
        """
        response = requests.request(method=method, url=url, json=body, params=params)
        json = response.json() if response.status_code != 204 else None
        if response.status_code not in [200, 201, 204]:
            raise ValueError(json["detail"])
        return json
    
    def create(self, obj: TypeModel) -> TypeModel:
        """
            Create a new object on the API.

            :param obj: An object of a specific type to create.

            :return: The newly created object.
        """
        url = f"{self.api_url}{obj.base_path}"
        return obj.from_json(self._make_request(url=url, method="POST", body=obj.body, params=obj.params))
    
    def refresh(self, obj: TypeModel) -> TypeModel:
        """
            Refresh the data of an existing object on the API.

            :param obj: An object of a specific type to refresh.

            :return: The refreshed object.
        """
        url = f"{self.api_url}{obj.base_path}{obj.id}/"
        return obj.from_json(self._make_request(url=url, method="PATCH", body=obj.body))

    def delete(self, obj: TypeModel | list[TypeModel]) -> None:
        """
            Delete an object or a list of objects from the API.

            :param obj: An object or list of objects to delete.
        """
        url = f"{self.api_url}{obj.base_path}{obj.id}"
        self._make_request(url=url, method="DELETE")

    def get(self, model: TypeModel, by: TypeModel | None = None, by_id: int | None = None,  **kwargs) -> TypeModel:
        """
            Retrieve an object from the API.

            :param model: The type of object to retrieve.
            :param by: An optional filter object to narrow down the query.
            :param by_id: An optional ID to retrieve a specific object.
            :param kwargs: Additional query parameters.

            :return: The retrieved object or None if not found.
        """
        if not by and by_id:
            url = f"{self.api_url}{model.base_path}{by_id}/"
        elif by and by_id:
            url = f"{self.api_url}{by.base_path}{by_id}{model.base_path}"
        else:
            url = f"{self.api_url}{model.base_path}"
        json = self._make_request(url=url, method="GET", params=kwargs)
        if not isinstance(json, list):
            return model.from_json(json) if json else None
        return model.from_json(json[0]) if len(json) == 1 else [model.from_json(obj) for obj in json]
