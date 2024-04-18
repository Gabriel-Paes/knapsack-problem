import os
import sys

root = os.getcwd()
sys.path.insert(0, root)

datasetsPath = os.path.join(root,"datasets")

datasets = os.listdir(datasetsPath)

print("Instâncias disponíveis:")
for index, file in enumerate(datasets):
    print(f"{index} - {file}")

selectedInstance = int(input("Escolha uma instância: "))

selectedDataset = datasets[selectedInstance]

with open(os.path.join(datasetsPath, selectedDataset)) as file:
    content = file.read()

print(content)

from algorithms.genetic import function

function()