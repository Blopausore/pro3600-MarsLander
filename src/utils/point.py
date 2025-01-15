##
#%%
import math
from typing import Any
import numpy as np

class Point:
    """Define point of space
        x : [0, 6999]
        y : [0, 2999]
    """
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __iter__(self):
        return iter([self.x, self.y])
    
    def __next__(self):
        return next(self)
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index out of range")
        
    def __eq__(self, other, epsilon=0.01) -> bool:
        """Here the notion of equality is discretised"""
        if self.x is None :
            print("Error : self is None")
        elif other[0] is None:
            print("Error : other is None")
        else:
            return (abs(self.x - other[0]) < epsilon and abs(self.y - other[1]) < epsilon)

    def distance(self, other) -> float:
        """Calcul the distance between two points"""
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 )

# %%
