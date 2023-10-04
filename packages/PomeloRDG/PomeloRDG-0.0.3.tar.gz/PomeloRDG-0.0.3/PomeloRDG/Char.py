from __init__ import *

class Char():
    def __init__(self, value = '', limit = Const.CHARS):
        self.limit = limit
        self.value = self.__rand__() if value == '' or not self.__check__(value) else value
        
    def __check__(self, x):
        """
        Check if the char is legal.
        """
        
        if type(x) != str or len(self.value) != 1:
            return False
        else:
            for _ in x:
                if _ not in self.limit:
                    return False
        return True
        
    def __rand__(self):
        """
        Generate a legal char.
        """
        
        char = random.choice(self.limit)
        self.value = char
        return char
    
    def set(self, x):
        """
        Set the value to a legal char.
        """
        
        if self.__check__(x):
            self.value = x
            return x
        
    def get(self):
        """
        Return the value.
        """
        
        return self.value
    
    def __str__(self):
        return self.get()