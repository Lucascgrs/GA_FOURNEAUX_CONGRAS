# GENETIC_EPF  
Exercise on problem-solving using Genetic Algorithms  

## Authors  
Fourneaux Damien and Congras Lucas  

## 1. Collaboration  
The work was done together on one computer for the last exercise. The Git repository was also shared.

## 2. Usage  
- 'solve_mastermind_Fourneaux_Congras.py' => Solves the Mastermind problem  
- 'solve_tsp_Fourneaux_Congras.py' => Solves the TSP problem
- 'ga_solver.py' => Core file containing all functions for solving problems with a Genetic Algorithm  
- 'tsp_problem.py' and 'mastermind_problem.py' => Define specific problem instances using 'ga_solver'  

## 3. GA Solver  

### Individual Class  
Represents a solution with:  
- A chromosome  
- A fitness score  

### GAProblem Class  
Defines core methods:  
- Selection  
- Mutation  
- Reproduction  
- Random individual generation  

### GASolver Class  
Solves a 'GAProblem' with methods to:  
- Initialize a population ('reset_population(pop_size)')  
- Evolve for one or multiple generations ('evolve_for_one_generation()', 'evolve_until(num_generations)')  
- Get the best solution ('get_best_individual()')  
