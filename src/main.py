import os
import sys

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

def main():
    root = os.getcwd()
    sys.path.insert(0, root)

    datasetsPath = os.path.join(root,"datasets")

    datasets = os.listdir(datasetsPath)

    print("Instâncias disponíveis:")
    for index, file in enumerate(datasets):
        print(f"{index} - {file}")

    #selectedInstance = int(input("Escolha uma instância: "))

    selectedDataset = datasets[5]

    capacity = None
    amountItems = None
    items = []

    with open(os.path.join(datasetsPath, selectedDataset)) as file:
        for index, line in enumerate(file):
            line = line.strip()

            if index == 0:
                capacity = int(line)
            elif index == 1:
                amountItems = int(line)
            else:
                values = line.split(",")
                items.append(Item(values[0],int(values[1]),int(values[2])))

    print("Capacidade:", capacity)
    print("Quantidade de Itens:", amountItems)

    """ for item in items:
        print(item.name, item.weight, item.value) """

    from algorithms.simulated_annealing import simulated_annealing_knapsack

    initial_temperature = 1000.0
    cooling_rate = 0.95
    num_iterations = 10000

    best_solution = simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations)
    #best_solution, best_energy, execution_time = simulated_annealing(items, capacity, initial_temperature, cooling_rate, num_iterations)
    
    print("Melhor solução:", best_solution)
    #print("Soma de valores:", best_energy)
    #print("Tempo de execução:", execution_time, "segundos")

    print("Itens selecionados:")
    for i, item in enumerate(items):
        if best_solution[i] == 1:
            print(f"Item {item.name}: Peso = {item.weight}, Valor = {item.value}")

if __name__ == "__main__":
    main()