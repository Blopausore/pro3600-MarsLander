import random
from environment.action import Action
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.config import CHROMOSOME_MUTATION_PROBABILITY


class ActionChromosome(AbstractChromosome):
    """The chromosome is a sequel of action
    
    It is the basic chromosome. 
    """
    def __init__(self, genes_: list[ActionGene], identifier: int = 0):
        super().__init__(genes_=genes_, identifier=identifier)
        self.iterator = 0

    def __len__(self):
        return len(self.genes)

    def __str__(self) -> str:
        """Return a string representation of the chromosome"""
        return f"Chromosome {self.identifier} : {len(self.genes)}"
    
    def __iter__(self):
        """Generate his iterator"""
        return iter(self.genes)
    
    def __next__(self):
        return next(self)
    
    def __ne__(self, other: object) -> bool:
        """Test if two chromosome are different"""
        for g0,g1 in zip(self, other):
            if g0 != g1:
                return True
        return False
    
    def __eq__(self, other: object) -> bool:
        """Test if two chromosome are equals"""
        return not self.__ne__(other)
    
    @staticmethod
    def generator(identifier: int, chromosome_size: int):    
        """Generate a random chromosome"""
        genes = [ActionGene.generator() for _ in range(chromosome_size)]
        return ActionChromosome(identifier=identifier, genes_=genes)
    
    @property
    def get_length(self):
        return len(self.genes)

    def mutate(self):
        """Mutate the chromsome"""
        for gene in self.genes:
            if random.random() < CHROMOSOME_MUTATION_PROBABILITY:
                gene.mutate()

    def reset(self):
        """Reset his simulation"""
        super().reset()
        self.iterator = 0

    def use(self):
        """Use an action of the chromosome"""
        if self.iterator >= self.get_length:
            return Action(0, 0)
        action = self.genes[self.iterator]
        self.iterator +=1
        return action
    
    def crossover(self,other):
        """Make a crossover between self and other
        It returns two childs chromosome from it 
        """
        random_percent = random.random()
        child0,child1 = [], []

        for g0,g1 in zip(self, other):
            rotate0 = round(random_percent * g0.rotate + (1-random_percent) * g1.rotate)
            rotate1 = round(random_percent * g1.rotate + (1-random_percent) * g0.rotate)
            power0 = round(random_percent * g0.power + (1-random_percent) * g1.power)
            power1 = round(random_percent * g1.power + (1-random_percent) * g0.power)
            child0.append(ActionGene(power=power0, rotate=rotate0))
            child1.append(ActionGene(power=power1, rotate=rotate1))

        return ActionChromosome(child0), ActionChromosome(child1)
    
