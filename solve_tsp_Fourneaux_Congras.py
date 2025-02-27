# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import cities, os
from random import *


class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, cities: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the lower, the better the fitness)
        """
        self.chromosome = cities
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, city_dict, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        for k in range(pop_size):
            shuffled_cities= list(city_dict.keys())
            shuffle(shuffled_cities)
            self._population.append(Individual(shuffled_cities, -cities.road_length(city_dict, [city for city in shuffled_cities]))) #Append new Individual to the population

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        pop_size = len(self._population) #we save the start population size
        self._population.sort(reverse=True)
        del self._population[int(len(self._population)*self._selection_rate) : ]  #deleting the less adapted individuals
        selection_size = len(self._population)

        print(self._population[0])

        for i in range(selection_size, pop_size):   #crossing 2 surviving ones for 1 child until reaching the start population size
            a = -1
            b = -1
            while a==b:
                a = randint(0, selection_size-1)
                b = randint(0, selection_size-1)

            parent1 = self._population[a]
            parent2 = self._population[b]

            random_number = len(parent1.chromosome) // 2

            child1 = parent1.chromosome[:random_number]

            for city in parent2.chromosome[random_number:]:
                if city not in child1:
                    child1.append(city)

            for city in city_dict:
                if city not in child1:
                    child1.append(city)

            self._population.append(Individual(child1, -cities.road_length(city_dict, child1)))

        for i in range(len(self._population)):  #mutating each new Individual with probability mutation_rate
            if random() < self._mutation_rate:
                chromosome1=-1
                chromosome2=-1
                while chromosome1 == chromosome2:
                    chromosome1 = randint(0, len(self._population[i].chromosome)-1)
                    chromosome2 = randint(0, len(self._population[i].chromosome)-1)
                self._population[i].chromosome[chromosome1], self._population[i].chromosome[chromosome2] = self._population[i].chromosome[chromosome2], self._population[i].chromosome[chromosome1]

        self._population.sort(reverse=True) #sorting population

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        return sorted(self._population, reverse=True)[0] #return the best Individual of the population by fitness

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        cpt=0
        while cpt < max_nb_of_generations and self.get_best_individual().fitness < threshold_fitness:    #while condition for the end of evolution number not met
            self.evolve_for_one_generation()    #call evolve function x times
            cpt += 1


city_dict = cities.load_cities('C:\\Users\\lucas\\OneDrive\\Bureau\\EPF\\4ème Année\\Professionnal Programming\\Genetic\\genetic_part2\\genetic_part2\\cities.txt')
g = GASolver()
g.reset_population(city_dict, 100)
g.evolve_until(max_nb_of_generations=500, threshold_fitness=0)
best = g.get_best_individual()
cities.draw_cities(city_dict, best.chromosome)
