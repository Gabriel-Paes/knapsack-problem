import random

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def main():
    # Exemplo de itens e capacidade da mochila
    items = [
        Item(2, 10),
        Item(3, 7),
        Item(4, 14),
        Item(5, 5),
        Item(6, 3)
    ]
    capacity = 10

    # Parâmetros do algoritmo genético
    population_size = 50
    crossover_rate = 0.8
    mutation_rate = 0.1
    num_generations = 500

    # Chamada para a função que implementa o algoritmo genético
    solution = genetic_algorithm(items, capacity, population_size, crossover_rate, mutation_rate, num_generations)

    # Imprimir a solução encontrada
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")

# Função para implementar o algoritmo genético para o Problema da Mochila
def genetic_algorithm(items, capacity, population_size, crossover_rate, mutation_rate, num_generations):
    population = generate_initial_population(len(items), population_size)

    for gen in range(num_generations):
        next_generation = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, items, capacity)
            parent2 = roulette_selection(population, items, capacity)
            offspring = crossover(parent1, parent2, crossover_rate)
            mutate(offspring, mutation_rate)
            next_generation.append(offspring)
        population = next_generation

    # Encontrar a melhor solução na última geração
    best_solution = max(population, key=lambda x: fitness_function(x, items, capacity))
    return best_solution

# Função para gerar uma população inicial aleatória
def generate_initial_population(size, population_size):
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(size)]  # 0 ou 1 (selecionado ou não selecionado)
        population.append(individual)
    return population

# Função de fitness para calcular o valor total da mochila
def fitness_function(solution, items, capacity):
    total_value = sum(item.value for item, selected in zip(items, solution) if selected == 1)
    total_weight = sum(item.weight for item, selected in zip(items, solution) if selected == 1)
    # Penalize soluções que excedam a capacidade da mochila
    if total_weight > capacity:
        total_value = 0
    return total_value

# Função para realizar a seleção por torneio
def tournament_selection(population, items, capacity):
    tournament_size = 5  # Tamanho do torneio
    tournament = random.sample(population, tournament_size)
    best_solution = max(tournament, key=lambda x: fitness_function(x, items, capacity))
    return best_solution

# Função para realizar a seleção por roleta
def roulette_selection(population, items, capacity):
    total_fitness = sum(fitness_function(individual, items, capacity) for individual in population)
    random_fitness = random.uniform(0, total_fitness)
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += fitness_function(individual, items, capacity)
        if cumulative_fitness >= random_fitness:
            return individual

# Função para realizar o cruzamento (crossover)
def crossover(parent1, parent2, crossover_rate):
    if parent1 == parent2:
        return parent1, parent2
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

# Função para realizar a mutação
def mutate(solution, mutation_rate):
    print(solution)
    if random.random() < mutation_rate:
        solution_mutate = solution[:]
        index_random = random.randint(0, len(solution) -1)
        solution_mutate[index_random] = int(not solution_mutate[index_random])
        return solution_mutate

if __name__ == "__main__":
    main()