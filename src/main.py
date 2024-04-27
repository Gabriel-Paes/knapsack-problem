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

    selectedInstance = int(input("Escolha uma instância: "))

    selectedDataset = datasets[selectedInstance]

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

    from algorithms.simulated_annealing import simulated_annealing

    initial_temperature = 1000
    cooling_rate = 0.95
    num_iterations = 1000

    best_solution = simulated_annealing(items, capacity, initial_temperature, cooling_rate, num_iterations)

    # Recomendo comentar o print abaixo em instancias acima de 10000
    #print("Melhor solução:", best_solution)

    total_weight = 0
    total_value = 0
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if best_solution[i] == 1:
            total_value += item.value
            total_weight += item.weight
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")

    print(f"Total Peso: {total_weight} | Total Valor: {total_value}")
    print("Capacidade:", capacity)
    print("Quantidade de Itens:", amountItems)

if __name__ == "__main__":
    main()