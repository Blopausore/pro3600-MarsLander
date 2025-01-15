import pygame
import sys
from solutions.abstract_solution import AbstractSolution
from environment.action import Action

class ManualSolution(AbstractSolution):
    @property
    
    def get_parameters(self) -> dict:
        return {}

    
    def use(self, environment=None) -> Action:
        """
        By given some parameters, use return the next action the lander have to make
        """
        action = Action()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action.rotate = 5
                if event.key == pygame.K_LEFT:
                    action.rotate = -5
                if event.key == pygame.K_UP:
                    action.power = 1
                if event.key == pygame.K_DOWN:
                    action.power = -1
                if event.key == pygame.K_q:
                    action.end = True
            
        return action

    def set_parameters(self, **kargs):
        """
        Will be used for the settings windows on pygame
        """
        for key, value in kargs:
            self.__setattr__(key, value)

