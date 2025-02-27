# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem, Individual
import cities, os
from random import *

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def __init__(self):
        super().__init__()
        
        # Load the city_dict from a file
        self.city_dict = cities.load_cities(os.getcwd() + '\\cities.txt')

    def generate_random_individual(self):
        chromosome = list(self.city_dict.keys())    #Generate and shuffle a chromosome with all the cities in the city_dict
        shuffle(chromosome)
        # Computing the fitness with the negative road length
        fitness = -cities.road_length(self.city_dict, [city for city in chromosome])
        return chromosome, fitness
    
    def selection(self, _population, _selection_rate):
        # Sort population by fitness and remove the worst individuals
        pop_size = len(_population)
        _population.sort(reverse=True)
        del _population[int(len(_population) * _selection_rate):]  # Keep only the best individuals
        selection_size = len(_population)
        return _population, pop_size, selection_size
    
    def reproduction(self, _population, pop_size, selection_size):
        # Generate enought new individuals by crossing the surviving ones to create (pop_size - selection_size) individuals
        for i in range(selection_size, pop_size):
            a = -1
            b = -1
            while a == b:
                a = randint(0, selection_size - 1)
                b = randint(0, selection_size - 1)
            
            parent1 = _population[a]
            parent2 = _population[b]
            
            # Doing crossover by taking half from the first parent and completing with the second one
            random_number = len(parent1.chromosome) // 2
            child1 = parent1.chromosome[:random_number]
            
            for city in parent2.chromosome[random_number:]:
                if city not in child1:
                    child1.append(city)
            
            # Ensure all cities are included
            for city in self.city_dict:
                if city not in child1:
                    child1.append(city)
            
            # Create new individual
            _population.append(Individual(child1, -cities.road_length(self.city_dict, child1)))
        
        return _population

    def mutation(self, _population, _mutation_rate):
        # Mutate individuals with a given probability "_mutation_rate"
        for i in range(len(_population)):
            if random() < _mutation_rate:
                chromosome1 = -1
                chromosome2 = -1
                while chromosome1 == chromosome2:
                    chromosome1 = randint(0, len(_population[i].chromosome) - 1)
                    chromosome2 = randint(0, len(_population[i].chromosome) - 1)
                # Swap two cities
                _population[i].chromosome[chromosome1], _population[i].chromosome[chromosome2] = _population[i].chromosome[chromosome2], _population[i].chromosome[chromosome1]
        
        _population.sort(reverse=True)
        return _population

if __name__ == '__main__':
    from ga_solver import GASolver
    
    # Initialization for the tsp problem
    problem = TSProblem()
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until(threshold_fitness=0, max_nb_of_generations=1000, showBetterFitness=True)
    
    # Visualize the best route
    cities.draw_cities(problem.city_dict, solver.get_best_individual().chromosome)
    
    print(f"Best guess {solver.get_best_individual().chromosome} {solver.get_best_individual().fitness}")
