##
#%%
from enum import Enum, auto

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from environment.environment import Environment

from score.scoring_manager import ScoringManager

from solutions.abstract_solution import AbstractSolution

from solutions.genetic.population import Population
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.chromosomes.action_chromosome import ActionChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.config import POPULATION_SIZE, CHROMOSOME_SIZE, MAXIMUM_EPOCH



class AlgoType(Enum):
    ACTION = 1

    def get_chromosome_type(algo_type: int):
        if algo_type == 1:
            return ActionChromosome
        
    def get_gene_type(algo_type: int):
        if algo_type == 1:
            return ActionGene


##
    #%%

class GeneticSolution(AbstractSolution):
    """Class that implement Genetic Algorithm
    Wkipedia : https://fr.wikipedia.org/wiki/Algorithme_g%C3%A9n%C3%A9tique

    Fields :
        * population_size : int
        * chromsome_size : int
        * algo_type : AlgoType
        * population : list[Chromosome]
        * epoch : int
        * best_chromosome : Chromosome
        * scoring_manager : ScoringManager
        
    """
    def __init__(self, 
                environment : Environment,
                population_size: int = POPULATION_SIZE, 
                chromosome_size: int = CHROMOSOME_SIZE,
                ):
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.algo_type = AlgoType.ACTION
        self.population = Population.generator(
            population_size=population_size
        )
        self.epoch = 0
        self.best_chromosome : AbstractChromosome = None
        self.scoring_manager = ScoringManager()
        self.evolution(environment)

    @property
    def get_index_best(self):
        """Get the identifier of the best chromosome"""
        return self.best_chromosome.identifier
    
    def reset(self, environment: Environment):
        """Reset the environment"""
        self.__init__(environment=environment)

    def get_parameters(self) -> dict:
        """Get the parameters of the GA"""
        return {
            "Population size": self.population_size,
            "Chromosome size": self.chromosome_size,
            "Epoch number" : self.epoch,
            "Best score" : int(self.population.best_score),
        }

    def use(self, **kargs):
        """Use for a step a chromosome"""
        action = self.best_chromosome.use()
        return action
    
    def evolution(self, environment: Environment):
        """Simulate the evolution of the population"""
        while self.epoch < MAXIMUM_EPOCH:
            done = self.one_evolution(environment)
            if done: break
            
    def use_chromosome(self, chromosome_index, environment):
        """Use a chromsome to is fulest and compute his score"""
        done = False
        environment.reset()
        trajectory = []
        while not done:
            action = self.population.chromosomes[chromosome_index].use()
            done = environment.step(action)
            trajectory.append((environment.lander.x, environment.lander.y))
        if environment.successful_landing():
            self.best_chromosome = self.population.chromosomes[chromosome_index]
            self.best_chromosome.reset()
            return True, trajectory, 0
        score = self.scoring_manager.compute_score(environment)
        self.population.set_score(chromosome_index, score)
        environment.reset()
        return False, trajectory, score


    def one_evolution(self, environment: Environment):
        """Compute all chromosome trajectory and compute the scores"""
        self.epoch +=1  
        if self.epoch == MAXIMUM_EPOCH:
            raise Exception("The maximum epoch has been reached")
        trajectories = [[] for _ in range(self.population_size)]
        scores = [0]*self.population_size
        self.population.reset()
        for chromosome_index in range(self.population_size):
            done, trajctory, score = self.use_chromosome(chromosome_index, environment)

            trajectories[chromosome_index] = trajctory
            scores[chromosome_index] = score
            
            if done:
                return done, trajectories
        self.best_chromosome = self.population.evolution()
        self.population.reset()
        return False, trajectories