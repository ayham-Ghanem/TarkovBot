

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
        # key is host id vlaue is queue obj
        self.dict[key] = value
    
    def get_queue(self,key):

        return self.dict.get(key,None)
    


class Channels_dict(metaclass=SingletonMeta):

    def __init__(self):
        self.dict = {}
    
    def get_dict(self):
        return self.dict
    
    def add(self,key,value):
        #key is id value is channel id
        self.dict[key] = value
    
    def find_by_value(self,value):
        
        keys = [k for k, v in self.dict.items() if v == value]
        return keys[0]

class Hosts_set(metaclass=SingletonMeta):

    def __init__(self):
        self.set = set()
    
    def get_dict(self):
        return self.set
    
    def add(self,host_id):
        
        self.set.add(host_id)
    
    def remove(self,host_id):
        self.set.discard(host_id)
    
    def check_if_hosting(self,host_id):
        
        return host_id in self.set
        
        
