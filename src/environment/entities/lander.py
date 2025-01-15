import sys
import numpy as np
from typing import Any

from environment.entities.entity import Entity
from environment.utils.constants import X_SCALE, Y_SCALE, H_SPEED_SCALE, V_SPACE_SCALE, ROTATE_SCALE, POWER_SCALE
    
class Lander(Entity):

    """Define the lander
    x : [0, 6999]
        Coordinate on the horizontal axe
    y : [0, 2999]
        Coordinate on the vertical axe
    h_speed : [-499, 499] 
        horizontal speed
    v_speed : [-499, 499] 
        vertical speed
    fuel : [0, 2000] 
        fuel that remains
    rotate : [-90, 90] 
        angle of the lander with 0 deg at the zenith
    power : [0, 4]
        power of the engine 
    """

    x : int
    y : int
    h_speed : float
    v_speed : float
    fuel : int
    rotate : int
    power : int
    
    def __init__(self, **kargs):
        self.state = np.array([kargs.get('x'), kargs.get('y'), kargs.get('h_speed'), kargs.get('v_speed'), kargs.get('fuel'), kargs.get('rotate'), kargs.get('power')], dtype=np.float64)
        self.fuel = kargs.get('fuel')
        self.rotate = kargs.get('rotate')
        self.power = kargs.get('power')

    @property
    def x(self):
        return self.state[0]
    
    @x.setter
    def x(self, value):
        self.state[0] = value

    @property
    def y(self):
        return self.state[1]
    
    @y.setter
    def y(self, value):
        self.state[1] = value

    @property
    def h_speed(self):
        return self.state[2]
    
    @h_speed.setter
    def h_speed(self, value):
        self.state[2] = value

    @property
    def v_speed(self):
        return self.state[3]
    
    @v_speed.setter
    def v_speed(self, value):
        self.state[3] = value

    @property
    def fuel(self):
        return self._fuel
    
    @fuel.setter
    def fuel(self, value):
        self._fuel = value

    @property
    def rotate(self):
        return self._rotate
    
    @rotate.setter
    def rotate(self, value):
        self._rotate = value

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, value):
        self._power = value

    def update(self, **kargs):
        """Update the lander"""
        for key, value in kargs.items():
            setattr(self, key, value)



    def __str__(self):
        try:
            return f"x, y: {self.x}  {self.y} | speed: {self.h_speed} {self.v_speed} | fuel, rotate, power: {self.fuel} {self.rotate} {self.power}"
        except AttributeError :
            return "lander not yiet initialized"
        

    def __eq__(self, other) -> bool:
        for attr in self.__dict__:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    
    def get_state(self):
        """Get a list of the state"""
        return self.state.copy()

        

