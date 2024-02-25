#!/usr/bin/python3
"""This module contains all models in HBNB console"""

from models.engine.file_storage import FileStorage

# Creating a unique FileStorage instance for the console
storage = FileStorage()
storage.reload()
