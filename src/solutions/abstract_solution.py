from abc import abstractmethod

from environment.action import Action
class AbstractSolution:
    
    @property
    @abstractmethod
    def get_parameters(self) -> dict:
        pass

    @abstractmethod
    def use(self, Environment=None) -> Action:
        """
        By given some parameters, use return the next action the lander have to make
        """
        pass

    def set_parameters(self, **kargs):
        """
        Will be used for the settings windows on pygame
        """
        for key, value in kargs:
            self.__setattr__(key, value)

