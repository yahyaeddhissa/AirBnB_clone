#!/usr/bin/python3
"""HBNB console module."""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBConsole(cmd.Cmd):
    """The HBNG command interpreter class.

    Attributes:
        prompt (str): Command prompt leading string
    """

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
    }

    def precmd(self, line):
        """Reformats the command to support the new syntax."""
        if "(" in line and ")" in line:
            args = line.replace("(", " ").replace(")", "").split(".")

            if len(args[1].split(" ")) > 1:
                command = args[1].split(" ")[0]
                props = []
                for prop in args[1].split(" ")[1:]:
                    props.append(prop.replace(",", ""))
                return "{} {} {}".format(command, args[0], " ".join(props))
            return "{} {}".format(args[1], args[0])
        return line

    def do_all(self, arg):
        """Prints all objects as strings."""
        objects_list = []

        if not arg:
            for object in storage.all().values():
                objects_list.append(str(object))
            return print(objects_list)

        args = arg.split()
        class_name = args[0]

        if class_name not in HBNBConsole.classes:
            print("** class doesn't exist **")
            return

        for key, object in storage.all().items():
            if key.split(".")[0] == class_name:
                objects_list.append(str(object))
        return print(objects_list)

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key in storage.all().keys():
            if args == key.split(".")[0]:
                count += 1
        print(count)

    def do_create(self, arg):
        """Creates a new object and saves it."""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]

        if class_name not in HBNBConsole.classes:
            print("** class doesn't exist **")

        new_object = self.classes[arg]()
        new_object.save()
        print(new_object.id)

    def do_show(self, arg):
        """Displays an object as a string based on the classname or id."""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]

        if class_name not in HBNBConsole.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        id = args[1]
        if id[0] == '"' and id[-1] == '"':
            id = id[1:-1]

        key = "{}.{}".format(class_name, id)

        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return
        print(objects[key])

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attribute."""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]

        if class_name not in HBNBConsole.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        object_id = args[1]

        if object_id[0] == '"' and object_id[-1] == '"':
            object_id = object_id[1:-1]

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = args[2]

        if attribute_name[0] == '"' and attribute_name[-1] == '"':
            attribute_name = attribute_name[1:-1]

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_value = args[3]

        if attribute_value[0] == '"' and attribute_value[-1] == '"':
            attribute_value = attribute_value[1:-1]

        key = "{}.{}".format(class_name, object_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        object = objects[key]
        setattr(object, attribute_name, attribute_value)
        object.save()

    def do_destroy(self, arg):
        """Deletes an object based on the classname and the id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBConsole.classes:
            print("** class doesn't exist **")
            return

        instance_id = args[1]
        if not instance_id:
            print("** instance id missing **")
            return

        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()

        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def emptyline(self):
        """Do nothing when empty line is entered."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handles EOF."""
        print("")
        return True


if __name__ == "__main__":
    HBNBConsole().cmdloop()
