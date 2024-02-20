from peewee import Field
from ast import literal_eval

class DictField(Field):
    field_type = 'text'
    
    def db_value(self, value):
        return str(value)
    
    def python_value(self, value) -> dict:
        return literal_eval(value)