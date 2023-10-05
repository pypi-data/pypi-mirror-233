from abc import ABC, abstractclassmethod, abstractproperty


class TypeModel(ABC):
    @abstractclassmethod
    def from_json(cls, object_json: dict):
        """
            Create an object of the implementing class from a JSON dictionary obtained from the API.

            :param object_json: JSON dictionary representing an object.

            :return: An instance of the implementing class.
        """
        raise NotImplementedError()
    
    @abstractproperty
    def body(self):
        """
            Get the data of the object in a dictionary format for API requests.

            :return: Dictionary representation of the object's data.
        """
        raise NotImplementedError()
    
    @abstractproperty
    def params(self):
        """
            Get query parameters for API requests.

            :return: Dictionary of query parameters.
        """
        raise NotImplementedError()
