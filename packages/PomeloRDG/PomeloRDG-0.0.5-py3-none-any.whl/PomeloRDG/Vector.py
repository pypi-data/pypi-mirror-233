from PomeloRDG.__init__ import *

class Vector():
    def __init__(self, size, **kwarg):
        self.size = size
        self.type = kwarg.get("type", Int)
        self.value = self.__rand__()
        
    def __check__(self, x):
        """
        Check if the vector elements are legal.
        """
        
        if type(x) != list or len(x) != self.size:
            return False
        for _ in x:
            if self.type().__check__(_):
                return False
        return True
        
    def __rand__(self):
        """
        Generate a legal vector.
        """
        
        self.value = [self.type() for _ in range(self.size)]
        return self.value
    
    def set(self, x):
        """
        Set the value to a legal vector.
        """
        
        if self.__check__(x):
            self.value = x
            return x
        
    def get(self):
        """
        Return the value.
        """
        
        return [self.value[i].value for i in range(self.size)]