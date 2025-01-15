import random


from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.config import GRADED_RETAIN_PERCENT, NONGRADED_RETAIN_PERCENT, POPULATION_SIZE, CHROMOSOME_SIZE
from solutions.genetic.chromosomes.action_chromosome import ActionChromosome

class Population:
    """Represent a population of chromosome
    This population can evolve with different function
        * Selection
        * Mutation
        * Crossover
    
    """
    chromosomes : list[AbstractChromosome]

    def __init__(self, chromosomes: list[AbstractChromosome]):
        self.chromosomes = chromosomes
        self.new_chromosomes = []
        self.chromosomes_score = [0]*len(chromosomes)
        self.population_size = len(chromosomes)
        self.chromosome_size = len(chromosomes[0])
        self.best_score = 0


    @staticmethod
    def generator(population_size: int=POPULATION_SIZE, chromosome_size=CHROMOSOME_SIZE, chromosome_type=ActionChromosome, **kargs):
        chromosomes = [chromosome_type.generator(identifier=identifier, chromosome_size=chromosome_size) for identifier in range(population_size)]
        return Population(chromosomes=chromosomes)
    
    def __len__(self):
        return len(self.chromosomes)
    
    def __getitem__(self, key):
        return self.chromosomes[key]
    

    @property
    def get_length(self) -> int:
        return len(self.chromosomes)
    
    def reset(self):
        for index in range(self.get_length):
            self.chromosomes[index].reset()
    
    def __iter__(self):
        return iter(self.chromosomes)
    
    def __next__(self):
        return next(self)
    
    def population_sort(self):
        """Sort the population by score"""
        self.chromosomes.sort(key=lambda chromosome: chromosome.score, reverse=False)

    def selection(self):
        """ Do the population go trought a selection process
        - Take the best GRADED_RETAIN_PERCENT

        """
        self.new_chromosomes.extend(self.chromosomes[-int(self.get_length*GRADED_RETAIN_PERCENT):])
        #Take the size_skipped best
        self.best_score = self.chromosomes[-1].score
        return self.chromosomes[-1]

    
    def cumulative_wheel2(self, number_of_childs) -> GeneratorExit(list[AbstractChromosome]):
        """
        Generate with the cumulative wheel algorithm, random pair of chromosome
        We assume that the population is already sorted by score
        """
        total_score = sum(map(lambda chromosome: chromosome.score, self.chromosomes))
        cumulative_scores = list()
        cumulative_score = 0
        for identifier in range(self.get_length):
            cumulative_score += self.chromosomes[identifier].score / total_score 
            cumulative_scores.append(cumulative_score)
        
        paired = False

        for j in range(number_of_childs):
                random_percent = min(0.99999, random.random())
                index = self.get_length - 1
                for i in range(self.get_length):
                    if cumulative_scores[i] > random_percent:
                        index = i
                        break    
                if not paired:
                    chromosome_parent0 = self.chromosomes[index]
                    paired = True
                elif chromosome_parent0 != self.chromosomes[index]:
                    paired = False
                    yield [chromosome_parent0, self.chromosomes[index]]
                    
    def cumulative_wheel(self, number_of_childs) -> GeneratorExit(list[AbstractChromosome]):
        """
        Generate with the cumulative wheel algorithm, random pair of chromosome
        We assume that the population is already sorted by score
        """
        total_score = sum(map(lambda chromosome: chromosome.score, self.chromosomes))
        cumulative_scores = [chromosome.score/total_score for chromosome in self.chromosomes]
        i=0
        while i < number_of_childs:
            parent0, parent1 = random.choices(self.chromosomes, weights=cumulative_scores, k=2)
            if parent0 != parent1:
                yield [parent0, parent1]
                i+=2


    def mutate(self):
        """Create a new population by making them mutate and mixing together"""
        mutated_partition_size = int(self.get_length*(1 - GRADED_RETAIN_PERCENT))
        for parent0, parent1 in self.cumulative_wheel(mutated_partition_size):               
            child0, child1 = parent0.crossover(parent1)
            child0.mutate()
            child1.mutate()
            self.new_chromosomes.append(child0)
            self.new_chromosomes.append(child1)
            # self.chromosomes[i0] = child0
            # self.chromosomes[i1] = child1 
            # i0 +=1
            # i1 +=1

    def fill_with_new_chromosome(self):
        """Create new random chromosome"""
        if len(self.new_chromosomes) > self.population_size:
            raise ValueError("New chromosomes are more than the population size")
        for identifier in range(self.population_size - len(self.chromosomes)):
            self.chromosomes.append(
                ActionChromosome.generator(identifier=identifier, chromosome_size=CHROMOSOME_SIZE)
            )

    def population_switch(self):
        """Switch between two slots of population
        It have the goal to save performances. Not implemented yiet
        """
        self.chromosomes = self.new_chromosomes.copy()
        self.new_chromosomes = []

    def set_score(self, index, score):
        """Set the score of a chromosome"""
        self.chromosomes[index].score += score
        # identifier = self.chromosomes[index].identifier
        # self.chromosomes_score[identifier] += score
        #self.chromosomes_score[index] += score

    def evolution(self):
        """Make the population evolve"""
        #self.generate_score()
        self.population_sort()
        best_chromosome = self.selection()
        self.mutate()
        self.fill_with_new_chromosome()
        self.population_switch()
        self.reset()
        return best_chromosome




