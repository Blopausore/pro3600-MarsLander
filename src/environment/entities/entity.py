import sys
from typing import Any

from environment.utils.constants import X_SCALE, Y_SCALE, H_SPEED_SCALE, V_SPACE_SCALE, ROTATE_SCALE, POWER_SCALE
    

class Entity:


    """Define a dynamic entity
    An entity do not have a form 
    x : [0, 6999]
        Coordinate on the horizontal axe
    y : [0, 2999]
        Coordinate on the vertical axe
    h_speed : [-499, 499] 
        horizontal speed
    v_speed : [-499, 499] 
        vertical speed
    """

    x : int
    y : int
    h_speed : float
    v_speed : float
    
    def __init__(self, **kargs):
        self.x = kargs.get('x')
        self.y = kargs.get('y')
        self.h_speed = kargs.get('h_speed')
        self.v_speed = kargs.get('v_speed')

    def __str__(self):
        """Return the dymamic states of the entity in string"""
        try:
            return f"Position : {self.x} | {self.y} \nVitesse: {self.h_speed} | {self.v_speed}"
        except AttributeError :
            return "Entity not yiet initialized"
        
    
    def update(self, **kwargs):
        """Update the fields with kargs value"""
        for cle, valeur in kwargs.items():
            if hasattr(self, cle):
                setattr(self, cle, valeur)
            else:
                print(f"Attention : Le champ '{cle}' n'existe pas dans la classe.", file=sys.stderr)
        
    def get_state(self):
        """Return a list of the state"""
        return [self.x, self.y, self.h_speed, self.v_speed]


    def __eq__(self, other) -> bool:
        """An entity is equal to another if it have the same state"""
        for self_attr, other_attr in zip(vars(self).values(), vars(other).values()):
            if not round(self_attr) == round(other_attr):
                return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
        
    def copy(self, other):
        """Copy other into self"""
        self.update(vars(other))
