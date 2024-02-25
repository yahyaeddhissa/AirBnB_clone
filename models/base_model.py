#!/usr/bin/python3
"""Defines the BaseModel class for all other classes."""

from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Defines all common attributes and methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Creates an instance of BaseModel class."""
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        from models import storage

        storage.new(self)

    def save(self):
        """Saves an instance."""
        self.updated_at = datetime.today()

        from models import storage

        storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary."""
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """Returns the string representation of a BaseModel instance."""

        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
