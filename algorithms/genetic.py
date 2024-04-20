import os
import sys
import math
import random

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

def knapsack_simulated_annealing(items, capacity, initial_temperature, cooling_rate, stopping_temperature, iterations):
    def calculate_value(combination):
        total_value = 0
        total_weight = 0
        for i in range(len(combination)):
            if combination[i] == 1:
                total_value += items[i].value
                total_weight += items[i].weight
        return total_value, total_weight
    
    current_solution = [0] * len(items)
    current_weight = 0
    current_value = 0
    
    for i in range(len(items)):
        if random.random() < 0.5:
            current_solution[i] = 1
            current_weight += items[i].weight
            current_value += items[i].value
    
    best_solution = current_solution[:]
    best_value = current_value
    
    temperature = initial_temperature
    
    while temperature > stopping_temperature:
        for _ in range(iterations):
            index_to_change = random.randint(0, len(items) - 1)
            new_solution = current_solution[:]
            new_solution[index_to_change] = 1 - new_solution[index_to_change]
            new_value, new_weight = calculate_value(new_solution)
            
            if new_weight <= capacity:
                if new_value > current_value:
                    current_solution = new_solution
                    current_value = new_value
                    current_weight = new_weight

                    if current_value > best_value:
                        best_solution = current_solution[:]
                        best_value = current_value
                else:
                    probability = math.exp((new_value - current_value) / temperature)
                    if random.random() < probability:
                        current_solution = new_solution
                        current_value = new_value
                        current_weight = new_weight
            else:
                # Penalizar soluções que excedam o peso da mochila suavemente
                current_value *= 0.95  # Reduzir o valor total em 5%
        
        temperature *= cooling_rate
    
    return best_solution, best_value

# Capacidade máxima da mochila
capacity = 15

# Parâmetros do Simulated Annealing
initial_temperature = 1000
cooling_rate = 0.99
stopping_temperature = 0.1
iterations = 1000

# Encontrar a melhor combinação de itens usando Simulated Annealing
best_solution, best_value = knapsack_simulated_annealing(items, capacity, initial_temperature, cooling_rate, stopping_temperature, iterations)

# Imprimir a melhor combinação
print("Melhor combinação de itens:")
for i, item in enumerate(best_solution):
    print("Item", i+1, "- Peso:", items[i].weight, "Valor:", items[i].value)
print("Valor total:", best_value)
