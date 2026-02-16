"""
Genetic Algorithm Template This is a class template for implementing a genetic
algorithm. You can customize the individual creation, fitness evaluation,
selection, crossover, and mutation functions as needed.

# Vocabulary 
    # population: A collection of individuals.
    # individual or chromosome: A single candidate solution in the population. 
    # gene: A single element or parameter of a chromosome.
    # fitness: A function that evaluates how good an individual is at solving the problem.
    # selection: The process of choosing individuals from the population to create offspring.
    # crossover: The process of combining two parent individuals to create offspring.
    # mutation: The process of randomly altering genes in an individual to maintain genetic diversity.
"""

import random
from prettytable import PrettyTable
from dataclasses import dataclass

class Individual:
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness

@dataclass
class ProblemConfig:
    """A struct to hold problem-specific parameters for the genetic algorithm."""
    function_name: str
    gene_range: tuple
    gene_length: int
    population_size: int
    max_generations: int
    mutation_probability: float
    crossover_probability: float
    generation_improvement_count: int
    pass_method: str = 'splat'  # 'splat' or 'list'
    best_individual: Individual = None

class Population:
    def __init__(self, config: ProblemConfig, individual_factory):
        self.config = config
        self.individuals = self.initialize_population(individual_factory)

    def initialize_population(self, individual_factory):
        """Creates a list of Individuals using the provided factory."""
        population_list = []
        for _ in range(self.config.population_size):
            population_list.append(individual_factory())
        return population_list

    def selection(self, method, tendency=None):
        if method == 'roulette':
            return self.selection_roulette()
        elif method == 'by_range':
            return self.selection_by_range(tendency)
        elif method == 'tournament':
            return self.selection_tournament()
        else:
            raise ValueError(f"Invalid selection method: {method}")

    def selection_roulette(self):
        """Calculates the total fitness of the population."""
        # The sum() function with a generator expression is an efficient way to do this.
        total_fitness = sum(ind.fitness for ind in self.individuals)

        # Handle the edge case where all fitnesses are zero to avoid division by zero.
        if total_fitness == 0:
            # If all individuals have the same fitness, select randomly.
            return random.choices(self.individuals, k=self.config.population_size)

        probabilities = [ind.fitness / total_fitness for ind in self.individuals]

        # Use random.choices to select individuals based on their fitness probability.
        # This allows fitter individuals to be selected more often.
        # The 'weights' parameter should be the probabilities, not cumulative probabilities.
        mating_pool = random.choices(self.individuals, weights=probabilities, k=self.config.population_size)
        return mating_pool

    def selection_by_range(self, tendency):
        if tendency == 'max':
            sort_descending = False
        elif tendency == 'min':
            sort_descending = True
        
        # Sort individuals based on fitness
        sorted_individuals = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=sort_descending)
        # Assign selection probabilities based on rank
        probabilities = [i/self.config.population_size for i in range(len(sorted_individuals))]
        # Select individuals based on rank probabilities
        mating_pool = random.choices(sorted_individuals, weights=probabilities, k=self.config.population_size)
        return mating_pool

    def selection_tournament(self, tournament_size=3):
        selected_individuals = []
        for _ in range(self.config.population_size):
            tournament = random.sample(self.individuals, tournament_size)
            winner = max(tournament, key=lambda ind: ind.fitness)
            selected_individuals.append(winner)
        return selected_individuals
    
    def crossover(self, selected_individuals, crossover_func):
        selected_individuals_copy = selected_individuals[:]
        random.shuffle(selected_individuals_copy)
        offspring = []
        for i in range(0, len(selected_individuals_copy), 2):
            parent1 = selected_individuals_copy[i]
            parent2 = selected_individuals_copy[(i + 1) % len(selected_individuals_copy)]
            # Single-point crossover            
            child1_genome, child2_genome = crossover_func(parent1.genome, parent2.genome, self.config)
            offspring.append(Individual(child1_genome, None))
            offspring.append(Individual(child2_genome, None))

        # Ensure offspring population is the same size as original
        return offspring[:self.config.population_size]

    def mutation(self, offspring, mutation_func):
        mutated_offspring = []
        for individual in offspring:
            mutated_genome = mutation_func(individual.genome, self.config)
            mutated_offspring.append(Individual(mutated_genome, None))
        return mutated_offspring

    def evaluate_fitness(self, fitness_func):
        for individual in self.individuals:
            individual.fitness = fitness_func(individual.genome)

    # Evolve population to next generation
    # tendency: 'min' or 'max' to indicate optimization goal
    def evolve_population(self, selection_method, tendency, crossover_func, mutation_func):
        population_next = []
        # Selection
        selected_individuals = self.selection(selection_method, tendency)
        # Crossover
        offspring = self.crossover(selected_individuals, crossover_func)
        # Mutation
        mutated_offspring = self.mutation(offspring, mutation_func)
        return mutated_offspring
    
# Factory function that produces a single, complete Individual
def individual_factory(config:ProblemConfig, create_genome, fitness_func):
    genome = create_genome(config.gene_range, config.gene_length)
    fitness = fitness_func(genome)
    return Individual(genome, fitness)

def genetic_algorithm(config:ProblemConfig, create_genome, fitness_func, stop_condition_func, crossover_func, mutation_func, selection_method='roulette', tendency='max', table_output_name="GA_result"):
    # Create the initial population using the factory
    factory = lambda: individual_factory(config, create_genome, fitness_func)
    population = Population(config, factory)

    # Generation variable (t)
    t = 0
    output_table = PrettyTable()
    output_table.field_names = ["Generation", "Individual", "Genome", "Fitness"]
    
    for i, individual in enumerate(population.individuals):
        output_table.add_row([t, i, individual.genome, f"{individual.fitness:.8f}"])
    # Reset generations without improvement
    config.generation_improvement_count = 0
    while stop_condition_func(t, population):
        population.individuals = population.evolve_population(selection_method, tendency, crossover_func, mutation_func)
        population.evaluate_fitness(fitness_func)
        t += 1
        output_table.add_row(["---", "---", "---", "---"])
        for i, individual in enumerate(population.individuals):
            output_table.add_row([t, i, individual.genome, f"{individual.fitness:.8f}"])

    with open(f"GA_output/{table_output_name}.txt", "w") as text_file:
            text = output_table.get_string()
            text_file.write(text)
            text_file.write("\n")
            text = output_table.get_latex_string()
            text_file.write(text)

    best_individual = max(population.individuals, key=lambda ind: ind.fitness, default=None)
    return best_individual.genome if best_individual else None
