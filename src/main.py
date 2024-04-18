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
                capacity = line
            elif index == 1:
                amountItems = line
            else:
                values = line.split(",")
                items.append(Item(values[0],values[1],values[2]))

    print("Capacidade:", capacity)
    print("Quantidade de Itens:", amountItems)

    for item in items:
        print(item.name, item.weight, item.value)

    """ from algorithms.genetic import function

    function() """


if __name__ == "__main__":
    main()