#!/usr/bin/python3
"""Defines the FileStorage class for managing storage."""

import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Stores HBNB objects in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to __objects."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves all objects to the JSON file."""
        serialized_objects = {}
        for key, value in self.__objects.items():
            serialized_objects[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Loads objects from a JSON file"""
        try:
            with open(FileStorage.__file_path, "r") as file:
                loaded_objects = json.load(file)
                for key, value in loaded_objects.items():
                    class_name = key.split(".")[0]
                    object_id = key.split(".")[1]
                    object_class = eval(class_name)
                    self.__objects[key] = object_class(**value)
        except FileNotFoundError:
            return
