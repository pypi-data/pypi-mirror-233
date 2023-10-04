from __init__ import *

class Float():
    def __init__(self, value = Const.INF, limit = [Const.FLOAT_MIN, Const.FLOAT_MAX]):
        self.limit = limit
        self.value = self.__rand__() if value == Const.INF or not self.__check__(value) else value
        
    def __check__(self, x):
        """
        Check if a floating-point number is legal.
        """
        
        if type(x) != float or x < self.limit[0] or x > self.limit[1]:
            return False
        return True
        
    def __rand__(self):
        """
        Generate a legal floating-point number.
        """
        
        self.value = random.uniform(self.limit[0], self.limit[1])
        return self.value
    
    def set(self, x):
        """
        Set the value to a legal floating-point number.
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