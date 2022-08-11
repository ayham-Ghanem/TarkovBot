

from mimetypes import init


class SingletonMeta(type):
   

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Queue_dict(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.dict = {}
    

    def add(self,key,value):

        self.dict[key] = value
    
    def get_queue(self,key):

        return self.dict.get(key,None)
    


class Channels_dict(metaclass=SingletonMeta):

    def __init__(self):
        self.dict = {}
    
    def get_dict(self):
        return self.dict
    
    def add(self,key,value):
        #key is id vlaue is channel id
        self.dict[key] = value
    
    def find_by_value(self,value):
        
        keys = [k for k, v in self.dict.items() if v == value]
        return keys[0]

