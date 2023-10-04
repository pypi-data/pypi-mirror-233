from __init__ import *

class String():
    def __init__(self, size = 0, value = "", limit = Const.CHARS):
        self.limit = limit
        self.size = size
        self.value = self.__rand__() if value == "" or not self.__check__(value) else value
        
    def __check__(self, x):
        """
        Check if the string is legal.
        """
        
        if type(x) != str or len(self.value) != self.size:
            return False
        else:
            for _ in x:
                if _ not in self.limit:
                    return False
        return True
        
    def __rand__(self):
        """
        Generate a legal string.
        """
        
        string = ""
        for _ in range(self.size):
            string += random.choice(self.limit)
        self.value = string
        return string
    
    def set(self, x):
        """
        Set the value to a legal string.
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