""" import math
import random
import time
# Define items with their values and weights
items = [
    {"value": 10, "weight": 5},
    {"value": 8, "weight": 3},
    {"value": 15, "weight": 7},
    {"value": 7, "weight": 4},
    {"value": 6, "weight": 2}
]

def neighbor_function(solution):
  while True:
    index1 = random.randint(0, len(solution) - 1)
    index2 = random.randint(0, len(solution) - 1)
    if index1 != index2:
      break

  new_solution = solution[:]
  new_solution[index1], new_solution[index2] = new_solution[index2], new_solution[index1]

  if solution[index1] == solution[index2]:
    new_solution[index1] = int(not new_solution[index1])

  return new_solution

def objective_function(solution):
    total_value = 0
    total_weight = 0
    selected_items = 0
    for i, item in enumerate(solution):
        if item:
            selected_items += 1
            total_value += items[i]["value"]
            total_weight += items[i]["weight"]

    # Penalize if weight exceeds limit OR if weight is negative
    if total_weight > MAX_WEIGHT or total_weight < 0:
        return -math.inf

    # Reward selecting items (rounded to nearest integer)
    base_value = total_value + int(0.1 * selected_items)

    # Soft penalty for exceeding weight limit (adjust weight_penalty factor)
    weight_penalty = 0
    if total_weight > MAX_WEIGHT:
        excess_weight = total_weight - MAX_WEIGHT
        weight_penalty = excess_weight * 0.1  # Adjust weight_penalty factor

    # Apply penalty to base value
    total_value = base_value - weight_penalty

    return total_value

def acceptance_probability(delta_E, temperature):
    if delta_E < 0:
        return 1
    return math.exp(-delta_E / temperature)

def simulated_annealing(initial_solution, neighbor_function, objective_function, initial_temperature, cooling_rate, max_iterations):
    start_time = time.time()
    current_solution = initial_solution
    current_energy = objective_function(current_solution)
    best_solution = current_solution
    best_energy = current_energy
    temperature = initial_temperature

    for i in range(max_iterations):
        new_solution = neighbor_function(current_solution)
        new_energy = objective_function(new_solution)
        delta_E = new_energy - current_energy

        if acceptance_probability(delta_E, temperature) > random.random():
            current_solution = new_solution
            current_energy = new_energy

        # Check if new solution exceeds weight limit
        if objective_function(current_solution) == -math.inf:
            # If it does, revert to previous solution
            current_solution = new_solution
            current_energy = new_energy

        if current_energy > best_energy:
            best_solution = current_solution
            best_energy = current_energy

        temperature *= cooling_rate

    end_time = time.time()  # End time after running the algorithm
    execution_time = end_time - start_time  # Calculate execution time

    return best_solution, best_energy, execution_time

# Initial solution and parameters
initial_solution = [random.choice([0, 1]) for _ in range(len(items))]  # Randomized initial solution
MAX_WEIGHT = 10  # Maximum weight limit
initial_temperature = 1000.0
cooling_rate = 0.95
max_iterations = 5000

best_solution, best_energy, execution_time = simulated_annealing(initial_solution, neighbor_function, objective_function, initial_temperature, cooling_rate, max_iterations)
print("Best solution:", best_solution)
print("Best total value:", best_energy)
print("Execution time:", execution_time, "seconds") """

""" import random
import math

class Item:
    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso

def valor_total(solucao, itens):
    total = 0
    for i in range(len(solucao)):
        if solucao[i] == 1:
            total += itens[i].valor
    return total

def peso_total(solucao, itens):
    total = 0
    for i in range(len(solucao)):
        if solucao[i] == 1:
            total += itens[i].peso
    return total

def solucao_inicial(itens):
    return [random.choice([0, 1]) for _ in range(len(itens))]

def vizinhanca(solucao):
    viz = solucao[:]
    index = random.randint(0, len(viz) - 1)
    viz[index] = 1 - viz[index]  # Alterna entre 0 e 1
    return viz

def simulated_annealing(itens, capacidade, temperatura_inicial, taxa_resfriamento):
    solucao_atual = solucao_inicial(itens)
    valor_atual = valor_total(solucao_atual, itens)
    melhor_solucao = solucao_atual[:]
    melhor_valor = valor_atual

    temperatura = temperatura_inicial

    while temperatura > 1:
        viz = vizinhanca(solucao_atual)
        if peso_total(viz, itens) <= capacidade:
            valor_viz = valor_total(viz, itens)
            delta = valor_viz - valor_atual
            if delta > 0 or random.random() < math.exp(delta / temperatura):
                solucao_atual = viz[:]
                valor_atual = valor_viz
                if valor_atual > melhor_valor:
                    melhor_solucao = solucao_atual[:]
                    melhor_valor = valor_atual
        temperatura *= taxa_resfriamento

    peso_total_melhor_solucao = peso_total(melhor_solucao, itens)
    return melhor_solucao, melhor_valor, peso_total_melhor_solucao

# Exemplo de uso
items = [
    Item(7, 369),
    Item(10, 346),
    Item(11, 322),
    Item(10, 347),
    Item(12, 348),
    Item(13, 383),
    Item(8, 347),
    Item(11, 364),
    Item(8, 340),
    Item(8, 324),
    Item(13, 365),
    Item(12, 314),
    Item(13, 306),
    Item(13, 394),
    Item(7, 326),
    Item(11, 310),
    Item(9, 400),
    Item(13, 339),
    Item(5, 381),
    Item(14, 353),
    Item(6, 383),
    Item(9, 317),
    Item(6, 349),
    Item(11, 396),
    Item(14, 353),
    Item(9, 322),
    Item(5, 329),
    Item(5, 386),
    Item(5, 382),
    Item(4, 369),
    Item(6, 304),
    Item(10, 392),
    Item(8, 390),
    Item(8, 307),
    Item(10, 318),
    Item(13, 359),
    Item(9, 378),
    Item(8, 376),
    Item(11, 330),
    Item(9, 331)
]
capacidade = 15
temperatura_inicial = 1000
taxa_resfriamento = 0.95

melhor_solucao, melhor_valor, peso_total_melhor_solucao = simulated_annealing(items, capacidade, temperatura_inicial, taxa_resfriamento)

print("Melhor solução:", melhor_solucao)
print("Valor total:", melhor_valor)
print("Peso total:", peso_total_melhor_solucao) """

import random
import math

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
        Item(6, 3),
        #Item(2,30)
    ]
    capacity = 10

    # Parâmetros do Simulated Annealing
    initial_temperature = 1000
    cooling_rate = 0.95
    num_iterations = 1000

    # Chamada para a função que implementa o Simulated Annealing
    solution = simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations)

    # Imprimir a solução encontrada
    print(solution)
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")

def simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations):
    current_solution = generate_random_solution(len(items))
    best_solution = current_solution[:]
    current_cost = cost_function(current_solution, items, capacity)
    best_cost = current_cost
    temperature = initial_temperature

    for _ in range(num_iterations):
        new_solution = generate_neighbor(current_solution)
        new_cost = cost_function(new_solution, items, capacity)

        delta_e = new_cost - current_cost
        max_delta_e_temp = max(abs(delta_e), temperature)
        scaled_delta_e = delta_e / max_delta_e_temp
        
        if delta_e > 0 or random.random() < math.exp(-scaled_delta_e):
            current_solution = new_solution[:]
            current_cost = new_cost

        if current_cost > best_cost:
            best_solution = current_solution[:]
            best_cost = current_cost

        temperature *= cooling_rate

    return best_solution

def generate_random_solution(size):
    return [random.randint(0, 1) for _ in range(size)]

def cost_function(solution, items, capacity):
    total_value = 0
    total_weight = 0
    for i, selected in enumerate(solution):
        if selected == 1:
            total_value += items[i].value
            total_weight += items[i].weight

    # Penalize soluções que excedam a capacidade da mochila
    if total_weight > capacity:
        excess_weight = total_weight - capacity
        # Reduza o valor proporcionalmente ao excesso de peso
        total_value -= total_value * (excess_weight / total_weight)

    return total_value

def generate_neighbor(solution):
    # Escolher aleatoriamente um índice para trocar
    index_to_change = random.randint(0, len(solution) - 1)
    
    # Trocar o valor do índice escolhido
    solution[index_to_change] = 1 if solution[index_to_change] == 0 else 0
    
    return solution

if __name__ == "__main__":
    main()
