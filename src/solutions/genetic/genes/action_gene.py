import random

from environment.action import Action
from solutions.genetic.genes.abstract_gene import AbstractGene
from solutions.genetic.config import WEIGHTS_POWER, WEIGHTS_ROTATION
class ActionGene(AbstractGene, Action):


    def __init__(self, **kargs):
        super().__init__(**kargs)

    @staticmethod
    def generator():
        gene = ActionGene(
            power = 0,
            rotate = 0
        )
        gene.mutate()
        return gene


    def mutate(self):
        """Mutate a gene
        The law of probability that they followed is not generaly uniform 
        but is generaly centered and symetrical.

        """
        self.rotate = random.choices(list(range(-15, 16)), WEIGHTS_ROTATION )[0]
        self.power = random.choices([-1, 0, 1], WEIGHTS_POWER)[0]

