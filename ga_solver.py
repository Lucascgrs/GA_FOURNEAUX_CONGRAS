# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""

from abc import abstractmethod


class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome : List representing the individual's chromosome
            fitness : The individual's fitness (the higher the value, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """
    Genetic Algorithm problem to be solved by GASolver.
    This is an abstract class which could be used by inherant child class
    """
    def __init__(self):
        pass

    @abstractmethod
    def generate_random_individual(self):
        """To implement in subclasses to generate a random individual"""
        pass

    @abstractmethod
    def selection(self, _population, _selection_rate):
        """To implement in subclasses to apply selection on the population"""
        pass

    @abstractmethod
    def reproduction(self, _population, pop_size, selection_size):
        """To implement in subclasses to apply reproduction"""
        pass

    @abstractmethod
    def mutation(self, _population, _mutation_rate):
        """To implement in subclasses to apply mutation on the population"""
        pass


class GASolver:
    """A generic Genetic Algorithm solver that can be applied to any GAProblem."""
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of GASolver for a GAProblem

        Args:
            problem, GAProblem to be solved by this solver
            selection_rate Selection rate between 0 and 1.0
            mutation_rate Mutation rate between 0 and 1.0
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """Initialize the population with pop_size random Individuals."""
        for k in range(pop_size):
            chromosome, fitness = self._problem.generate_random_individual()
            self._population.append(Individual(chromosome, fitness))
        
        self._population.sort(reverse=True)

    def evolve_for_one_generation(self, showBetterFitness=False):
        """Perform one generation of evolution:
            - Selection: Keep the fittest individuals
            - Reproduction: Generate new individuals from selected ones
            - Mutation: Apply randoms mutations to the population
        """
        self._population, pop_size, selection_size = self._problem.selection(self._population, self._selection_rate)
        self._population = self._problem.reproduction(self._population, pop_size, selection_size)
        self._population = self._problem.mutation(self._population, self._mutation_rate)
        
        if showBetterFitness:
            print(self.get_best_individual().fitness)

    def show_generation_summary(self):
        """Function to display population details"""
        pass

    def get_best_individual(self):
        """Return the best individual from the population ranked by fitness"""
        return sorted(self._population, reverse=True)[0]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None, showBetterFitness=False):
        """Run the evolution process until one of the stopping criteria is met:
            - A maximum number of generations is reached
            - An individual reaches the desired fitness threshold
        """
        cpt = 0
        while cpt < max_nb_of_generations and self.get_best_individual().fitness < threshold_fitness:
            self.evolve_for_one_generation(showBetterFitness)  # Run one generation
            cpt += 1
            