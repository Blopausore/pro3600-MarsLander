import math
import numpy as np
import numba as nb

from environment.surface import Surface
from environment.entities.lander import Lander
from environment.action import Action
from environment.utils.constants import MARS_GRAVITY, X_SCALE, Y_SCALE, ROTATE_SCALE, POWER_SCALE, PI_180

from utils.segment import Segment
from utils.point import Point


def next_dynamics_parameters(state, dt=1):
    """Calcul the next dynamic step states"""
    accel = state[6] *np.array([-math.sin(state[5]*PI_180), math.cos(state[5]*PI_180)]) + np.array([0, MARS_GRAVITY])
    state[2:4] += accel*dt
    state[0:2] += state[2:4]*dt + 0.5*accel*dt**2
    return state


class Environment:
    """ Environment of the Mars lander puzzle of CodinGames    
    FIELDS : 
        surface : 

    """

    surface : Surface
    lander : Lander

    def __init__(self, surface : list, initial_state):
        self.surface : Surface = surface
        self.initial_state = initial_state
        if isinstance(initial_state, dict):
            self.lander = Lander(**initial_state)
        else :
            self.lander = initial_state
            self.initial_state = self.lander.get_state()
        self.collision_area = None


    def __str__(self) -> str:
        #return "\n".join([score_info,coord_info,speed_info,rotate_info,fuel_info])
        return str(self.lander)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        
        return  self.surface == other.surface and\
                self.initial_state == other.initial_state and \
                self.lander == other.lander
 
    def reset(self):
        """Reset the lander"""
        self.lander.update(**self.initial_state)

    def exit_zone(self) -> bool:
        """Check if the lander is out of the map"""
        return not (0 <= self.lander.x < X_SCALE and 0 <= self.lander.y < Y_SCALE)

    def landing_on_site(self) -> bool:
        """Check if lander lands on the landing site"""
        if self.collision_area is None: return False
        return self.collision_area == self.surface.landing_area

    def landing_angle(self) -> bool:
        """Check if the landing angle respect a succesful landing"""
        return self.lander.rotate == 0

    def landing_vertical_speed(self) -> bool:
        """Check if the landing vertical speed respect a succesful landing"""
        return abs(self.lander.v_speed) <= 40

    def landing_horizontal_speed(self) -> bool:
        """Check if the landing horizontal speed respect a succesful landing"""
        return abs(self.lander.h_speed) <= 20

    def successful_landing(self) -> bool:
        """For a landing to be successful, the ship must:
            - land on flat ground
            - land in a vertical position (tilt angle = 0°)
            - vertical speed must be limited ( ≤ 40m/s in absolute value)
            - horizontal speed must be limited ( ≤ 20m/s in absolute value)
        """
        return (\
            self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed()
            )
  
    def next_dynamics_parameters(self, dt=1):
        """Calcul the next dynamic step states"""
        accel = self.lander.power *np.array([-math.sin(self.lander.rotate*PI_180), math.cos(self.lander.rotate*PI_180)]) + np.array([0, MARS_GRAVITY])

        self.lander.state[2:4] += accel*dt
        self.lander.state[0:2] += self.lander.state[2:4]*dt + 0.5*accel*dt**2
        

    def step(self, action: Action, dt=1) -> bool:
        """        
        -rotate is the desired rotation angle for Mars lander. 
        Please note that for each turn the actual value of the angle 
        is limited to the value of the previous turn +/- 15°.
        
        - power is the desired thrust power. 
        0 = off. 4 = maximum power. 
        Please note that for each turn the value of the actuaNl power 
        is limited to the value of the previous turn +/- 1.
        """
        
        rotate = max(-ROTATE_SCALE, min(
            ROTATE_SCALE,
            self.lander.rotate + action.rotate
        )) 

        power = max(0, min(
            POWER_SCALE,
            self.lander.power + action.power
        ))
        
        fuel = int(self.lander.fuel - power*dt)
        if fuel <= 0 :
            power = self.lander.fuel
            fuel = 0
        self.lander.fuel = fuel
        self.lander.rotate = rotate
        self.lander.power = power
        prev_position = Point(self.lander.x, self.lander.y)
        self.lander.state = next_dynamics_parameters(self.lander.state, dt=dt)
        actu_position = Point(self.lander.x, self.lander.y)
        trajectory = Segment(prev_position, actu_position)
        collision_area = self.surface.they_collide(trajectory)

        if not collision_area is None or self.exit_zone():
            self.collision_area = collision_area
            return True
        else:
            return False
        