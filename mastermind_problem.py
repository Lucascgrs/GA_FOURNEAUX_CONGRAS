# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem, Individual
import mastermind as mm
from random import *

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
    def __init__(self, match):
        super().__init__()
        
        self.Match = match

    def generate_random_individual(self):
        """Generates a random chromosome and evaluates its fitness"""
        chromo = self.Match.generate_random_guess()
        fitness = self.Match.rate_guess(chromo)

        return chromo, fitness
    
    def selection(self, _population, _selection_rate):
        """Selects the fittest individuals with the selection rate"""
        pop_size = len(_population)

        _population.sort(reverse=True)
        del _population[int(len(_population)*_selection_rate):]  # Remove less fit individuals
        selection_size = len(_population)

        return _population, pop_size, selection_size
    
    def reproduction(self, _population, pop_size, selection_size):
        """Doing crossover between selected individuals to create new individuals"""
        for i in range(selection_size, pop_size):  # Generate new individuals until reaching initial population size
            a = -1
            b = -1
            while a == b:
                a = randint(0, selection_size-1)
                b = randint(0, selection_size-1)

            parent1 = _population[a]
            parent2 = _population[b]

            random_number = randint(0, len(parent1.chromosome)-1)
            
            # Create a child by combining genes from two parents
            child1 = parent1.chromosome[:random_number] + parent2.chromosome[random_number:]
            _population.append(Individual(child1, self.Match.rate_guess(child1)))

        return _population

    def mutation(self, _population, _mutation_rate):
        """Applies mutation to individuals based on _mutation_rate"""
        for i in range(len(_population)):
            if random() < _mutation_rate:  # Mutate with a given probability
                random_chromosome_to_mute = randint(0, len(_population[i].chromosome)-1)
                _population[i].chromosome[random_chromosome_to_mute] = choice(mm.get_possible_colors())
                _population[i].fitness = self.Match.rate_guess(_population[i].chromosome)

        _population.sort(reverse=True)
        return _population


if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=6)  # Creates a Mastermind match
    problem = MastermindProblem(match)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_for_one_generation()
    solver.evolve_until(threshold_fitness=match.max_score())  # Evolves until the solution is found

    # Prints the best solution found
    print(f"Best guess {solver.get_best_individual().chromosome} {solver.get_best_individual().fitness}")
    print(f"Problem solved? {match.is_correct(solver.get_best_individual().chromosome)}")