import math
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
print("Execution time:", execution_time, "seconds")