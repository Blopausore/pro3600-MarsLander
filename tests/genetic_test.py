import unittest
import random

from src.solutions.genetic.genetic_solution import GeneticSolution
from src.solutions.genetic.population import Population
from src.solutions.genetic.chromosomes.action_chromosome import ActionChromosome

class TestGenetic(unittest.TestCase):
    def test_population_generator(self):
        population = Population.generator(10, 100, ActionChromosome)
        self.assertEqual(len(population), 10)
        self.assertEqual(len(population[0].genes), 100)
        self.assertEqual(len(population[0].genes), len(population[1].genes))
        self.assertNotEqual(population[0].genes, population[1].genes)
        

    def test_cumulative_wheel(self):
        population = Population.generator(10, 100, ActionChromosome)

        # Set random score
        for index in range(len(population)):
            population[index].score = random.randint(0, 400)
        population.population_sort()

        cumulative_wheel = list(population.cumulative_wheel(10))
        
        cumulative_wheel2 = list(population.cumulative_wheel2(10))
        self.assertEqual(len(cumulative_wheel), 5)
        for childs in cumulative_wheel:
            self.assertEqual(len(childs), 2)
            self.assertIsInstance(childs[0], ActionChromosome)
            self.assertIsInstance(childs[1], ActionChromosome)
            self.assertNotEqual(childs[0].identifier, childs[1].identifier)

    def test_selection(self):
        population = Population.generator(10, 100, ActionChromosome)
        for index in range(len(population)):
            population[index].score = index
        population.population_sort()
        best_chromosome = population.selection()
        self.assertEqual(best_chromosome.score, 9)
