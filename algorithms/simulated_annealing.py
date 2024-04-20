""" import random
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
        Item(6, 3)
    ]
    capacity = 10

    # Parâmetros do Simulated Annealing
    initial_temperature = 1000
    cooling_rate = 0.95
    num_iterations = 1000

    # Chamada para a função que implementa o Simulated Annealing
    solution = simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations)

    # Imprimir a solução encontrada
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

        if new_cost > current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
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
    # Implemente o método de penalização que achar mais adequado
    if total_weight > capacity:
        total_value = 0
    return total_value

def generate_neighbor(solution):
    # Implemente a geração de vizinhos aqui (por exemplo, trocar um item selecionado por um não selecionado)
    # Retorne uma solução válida
    return solution

if __name__ == "__main__":
    main() """

import math
import random
import time

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

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

def simulated_annealing(items, capacity, initial_temperature, cooling_rate, num_iterations):
    start_time = time.time()

    current_solution = generate_random_solution(len(items))
    current_energy = objective_function(current_solution, items, capacity)
    best_solution = current_solution
    best_energy = current_energy
    temperature = initial_temperature

    for i in range(num_iterations):
        new_solution = neighbor_function(current_solution)
        new_energy = objective_function(new_solution, items, capacity)
        delta_E = new_energy - current_energy

        if acceptance_probability(delta_E, temperature) > random.random():
            current_solution = new_solution
            current_energy = new_energy

        # Check if new solution exceeds weight limit
        if new_energy == -math.inf:  # Changed to new_energy
            # If it does, revert to previous solution
            current_solution = best_solution  # Revert to the best solution so far
            current_energy = best_energy

        if current_energy > best_energy:
            best_solution = current_solution
            best_energy = current_energy

        temperature *= cooling_rate

    end_time = time.time()
    execution_time = end_time - start_time

    return best_solution, best_energy, execution_time

def generate_random_solution(size):
    return [random.randint(0, 1) for _ in range(size)]

def objective_function(solution, items, capacity):
    total_value = 0
    total_weight = 0
    selected_items = 0
    for i, item in enumerate(solution):
        if item:
            selected_items += 1
            total_value += items[i].value
            total_weight += items[i].weight

    # Penalize if weight exceeds limit OR if weight is negative
    if total_weight > capacity or total_weight < 0:
        return -math.inf

    # Reward selecting items (rounded to nearest integer)
    base_value = total_value + int(0.1 * selected_items)

    # Soft penalty for exceeding weight limit (adjust weight_penalty factor)
    weight_penalty = 0
    if total_weight > capacity:
        excess_weight = total_weight - capacity
        weight_penalty = excess_weight * 0.1  # Adjust weight_penalty factor

    # Apply penalty to base value
    total_value = base_value - weight_penalty

    return total_value

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

def acceptance_probability(delta_E, temperature):
    if delta_E < 0:
        return 1
    return math.exp(-delta_E / temperature)

# Initial solution and parameters
capacity = 10  # Maximum weight limit
initial_temperature = 1000.0
cooling_rate = 0.95
num_iterations = 1000

best_solution, best_energy, execution_time = simulated_annealing(items, capacity, initial_temperature, cooling_rate, num_iterations)
print("Best solution:", best_solution)
print("Best total value:", best_energy)
print("Execution time:", execution_time, "seconds")