from abc import abstractmethod

from environment.action import Action

class AbstractGene:
    """
    Abstract Class of a gene.

    METHODS : 

    """
    @staticmethod
    @abstractmethod
    def generator(**kargs):
        pass

    @abstractmethod
    def mutate(self):
        pass





    