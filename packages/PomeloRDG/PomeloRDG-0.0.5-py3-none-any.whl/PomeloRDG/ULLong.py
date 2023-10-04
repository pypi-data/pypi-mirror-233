from PomeloRDG.__init__ import *

class ULLong():
    def __init__(self, value = Const.INF, limit = [Const.ULLONG_MIN, Const.ULLONG_MAX]):
        self.limit = limit
        self.value = self.__rand__() if value == Const.INF or not self.__check__(value) else value
        
    def __check__(self, x):
        """
        Check if an unsigned long integer is legal.
        """
        
        if type(x) != int or x < self.limit[0] or x > self.limit[1]:
            return False
        return True
        
    def __rand__(self):
        """
        Generate a legal unsigned long integer.
        """
        
        self.value = random.randint(self.limit[0], self.limit[1])
        return self.value
    
    def set(self, x):
        """
        Set the value to a legal unsigned long integer.
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