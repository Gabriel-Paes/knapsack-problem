import random
import math

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
        #print(new_solution)
        new_cost = cost_function(new_solution, items, capacity)

        #print(current_cost)
        #print(new_cost)
        #print(temperature)

        """         max_value = max(abs(current_cost - new_cost), abs(temperature))
        numerador -= max_value
        result
        denominador -= max_value """

        if(temperature < 1):
            temperature = 1
        
        if new_cost > current_cost or random.random() < math.exp((current_cost - new_cost) / round(temperature, 2)):
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
    print(total_weight)
    if total_weight > capacity:
        total_value = 0
    return total_value

def generate_neighbor(solution):
    #se o custo for maior eu posso remover, menor add (validar o que tenho para gerar um novo vizinho)
    vizinho = solution[:]
    idx = random.randint(0, len(vizinho)-1) # Escolhe aleatoriamente um item para alterar
    vizinho[idx] = int(not vizinho[idx])
    return vizinho

if __name__ == "__main__":
    main()