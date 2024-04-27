import random
import math

# Definição da função Simulated Annealing
def simulated_annealing(items, capacity, initial_temperature, cooling_rate, num_iterations):
    current_solution = [0] * len(items)
    best_solution = current_solution[:]
    current_cost = 0
    best_cost = current_cost

    # Soma o total dos valores dos items da solução
    def get_total_value(solution):
        total_value = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                total_value += items[i].value
        return total_value

    # Soma o total dos pesos dos items da solução
    def get_total_weight(solution):
        total_weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                total_weight += items[i].weight
        return total_weight

    # Analisa o delta e retorna a divisão pela temperatura ou 1
    def acceptance_probability(delta, temperature):
        if delta > 0:
            return math.exp(-delta / temperature)
        else:
            return 1
        
    # Loop com o número de interações
    for _ in range(num_iterations):
        temperature = initial_temperature
        while temperature >= 0.2:
            neighbor_solution = generate_neighbor(current_solution)
            neighbor_weight = get_total_weight(neighbor_solution)
            
            if neighbor_weight <= capacity:
                neighbor_value = get_total_value(neighbor_solution)
                delta = neighbor_value - current_cost

                if delta > 0 or random.random() < acceptance_probability(delta, temperature):
                    current_solution = neighbor_solution
                    current_cost = neighbor_value

                    if current_cost > best_cost:
                        best_solution = current_solution
                        best_cost = current_cost

            temperature *= cooling_rate

    return best_solution

# Geração de uma solução vizinha a solução
def generate_neighbor(solution):
    neighbor = solution[:]
    idx = random.randint(0, len(neighbor) - 1)
    neighbor[idx] = 1 - neighbor[idx] # flip 0 pra 1 ou 1 pra 0
    return neighbor
