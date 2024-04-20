import random
import copy

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def main():
    # Exemplo de itens e capacidade da mochila
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
    capacity = 15

    # Parâmetros da Busca Tabu
    tabu_size = 5
    max_iterations = 1000

    # Chamada para a função que implementa a Busca Tabu
    solution, total_value, total_weight = tabu_search_knapsack(items, capacity, tabu_size, max_iterations)

    # Imprimir a solução encontrada
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")

    print(f"Peso total: {total_weight}")
    print(f"Valor total: {total_value}")

def tabu_search_knapsack(items, capacity, tabu_size, max_iterations):
    current_solution = generate_random_solution(len(items))
    best_solution = copy.deepcopy(current_solution)
    current_cost = cost_function(current_solution, items, capacity)
    best_cost = current_cost
    tabu_list = []

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_solution)
        next_solution = None
        next_cost = float('-inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_cost = cost_function(neighbor, items, capacity)
                if neighbor_cost > next_cost:
                    next_solution = neighbor
                    next_cost = neighbor_cost

        if next_solution is None:
            break

        current_solution = next_solution
        current_cost = next_cost

        if current_cost > best_cost:
            best_solution = copy.deepcopy(current_solution)
            best_cost = current_cost

        tabu_list.append(next_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    total_value = sum(item.value for item, selected in zip(items, best_solution) if selected == 1)
    total_weight = sum(item.weight for item, selected in zip(items, best_solution) if selected == 1)
    return best_solution, total_value, total_weight

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
        total_value = 0
    return total_value

def generate_neighbors(solution):
    # Implemente a geração de vizinhos aqui (por exemplo, trocar um item selecionado por um não selecionado)
    # Retorne uma lista de vizinhos válidos
    
    neighbors = []
    for i in range(len(solution)):  
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]  # Troca o valor do item i
        neighbors.append(neighbor)
    return neighbors

if __name__ == "__main__":
    main()
