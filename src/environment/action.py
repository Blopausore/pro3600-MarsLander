import random

from environment.utils.constants import ACTION_POWER_SCALE, ACTION_ROTATE_SCALE
from environment.utils.utils import clamp

class Action:
    """
    Action of the lander :
    It represents an action that the lander can do

    FIELDS
        rotate : [-15,15]
            action of rotation
        power : [-1,1]
            action of power
    """

    def __init__(self, rotate : int=0, power : int=0):
        """Initiate the action and make sure they are in the space of action"""
        self.rotate = clamp(rotate, -ACTION_ROTATE_SCALE, ACTION_ROTATE_SCALE)
        self.power = clamp(power, -ACTION_POWER_SCALE, ACTION_POWER_SCALE)
        self.end = False

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def __eq__(self, other) -> bool:
        """An action is equal to another id they do the same thing"""
        return self.rotate == other.rotate and self.power == other.power

    def last_action(self, rotate):
        """Choose the best action to choose by straighten up the drone """
        if abs(rotate) <= 15:
            self.rotate = -rotate

