from typing import ClassVar, Dict, List
from numpy import isin
from pydantic import BaseModel, validator, Extra, Field
import json 
import functools
from typeguard import check_type

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# using wonder's beautiful simplification: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects/31174427?noredirect=1#comment86638618_31174427

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        if type(obj) == list:
            return [rgetattr(o, attr) for o in obj]
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

class SieveBaseModel(BaseModel, extra=Extra.allow):

    fields: ClassVar[Dict[str, type]] = {
    }

    defaults: ClassVar[Dict[str, Field]] = {
    }

    def to_dict(self):
        """
        Converts the object to a dictionary
        """
        return self.dict()
    
    def to_json(self):
        """
        Converts the object to a JSON string
        """
        return json.dumps(self.to_dict())
    
    def to_json_pretty(self):
        """
        Converts the object to a pretty JSON string
        """
        return json.dumps(self.to_dict(), indent=4)

    def from_dict(self, d):
        """
        Unpacks a dictionary into the object
        """
        return self.parse_obj(d)
    
    def from_json(self, j):
        """
        Unpacks a JSON string into the object
        """
        return self.parse_raw(j)

    def update(self, other_object):
        """
        Recusively update attrs of self with attrs of other_object
        """
        for attr, value in other_object.__dict__.items():
            if isinstance(value, SieveBaseModel):
                self.update(value)
            else:
                setattr(self, attr, value)

    # Validate the fields and set defaults if not present
    def __init__(self, **data):
        fields, defaults = self.init_fields()
        data = self.recursive_populate_data(fields, **data)
        super().__init__(**data)
        self.check_fields(fields, defaults)

    def init_fields(self):
        """
        Returns the fields of the object recursively for all super classes if they are SieveBaseModel
        """
        # Populate fields in order of inheritance
        fields = {}
        for cls in reversed(self.__class__.__mro__):
            if issubclass(cls, SieveBaseModel):
                if hasattr(cls, "fields"):
                    fields.update(cls.fields)
        if self.fields:
            fields.update(self.fields)

        #Populate defaults in order of inheritance
        defaults = {}
        for cls in reversed(self.__class__.__mro__):
            if issubclass(cls, SieveBaseModel):
                if hasattr(cls, "defaults"):
                    defaults.update(cls.defaults)
        if self.defaults:
            defaults.update(self.defaults)
        return fields, defaults

    def recursive_populate_data(self, fields, **data):
        """
        Recursively populates the fields dictionary with the fields of the object and its parents
        """

        # Add the fields of the current class
        for data_field, data_value in data.items():
            if data_field in fields:
                if isinstance(data_value, dict):
                    if issubclass(fields[data_field], BaseModel):
                        data[data_field] = fields[data_field](**data_value)
                # Slightly messy code to check and unpack list that should be changed at some point
                elif isinstance(data_value, list) and fields[data_field].__origin__ == list and issubclass(fields[data_field].__args__[0], BaseModel):
                    for i, item in enumerate(data_value):
                        if isinstance(item, dict):
                            data_value[i] = fields[data_field].__args__[0](**item)
        
        return data

    def check_fields(self, fields, defaults):
        """
        Checks if the fields have a valid type and are present
        """
        for field, field_type in fields.items():
            # Check if the field is present
            if field not in self.__dict__:
                # Check if the field has a default
                if field in defaults:
                    self.__dict__[field] = defaults[field]
                else:
                    raise ValueError(f"Missing field {field}")

    def get_attribute(self, attr, default=None):
        """
        Gets an attribute of the object recursively with . notation with aliasing support
        """
        try:
            return rgetattr(self, attr)
        except AttributeError:
            return default

    
    def set_attribute(self, attr, value):
        """
        Sets an attribute of the object recursively with . notation
        """
        return rsetattr(self, attr, value)

    def has_attribute(self, attr):
        """
        Checks if the object has an attribute recursively with . notation
        """
        try:
            rgetattr(self, attr)
            return True
        except AttributeError:
            return False



    # Print json schema for the class with all fields and defaults filled in
    @classmethod
    def print_schema(cls):
        print(json.dumps(cls.schema(), indent=4))
    
