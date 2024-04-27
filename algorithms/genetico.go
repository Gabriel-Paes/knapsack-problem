package main

import (
	"fmt"
	"math/rand"
	"time"

	"bufio"
    "os"
    "strconv"
    "strings"
	//"math"
)

// Item represents an item with weight and value
type Item struct {
	Weight int
	Value  int
}

// GeneticAlgorithm represents the genetic algorithm for solving the knapsack problem
type GeneticAlgorithm struct {
	Capacity       int
	PopulationSize int
	CrossoverRate  float64
	MutationRate   float64
	NumGenerations int
	Population     [][]int
	TournamentSize int
	SolutionList   []int
}

// NewGeneticAlgorithm initializes a new genetic algorithm instance
func NewGeneticAlgorithm(capacity, populationSize int, crossoverRate, mutationRate float64, numGenerations int) *GeneticAlgorithm {
	return &GeneticAlgorithm{
		Capacity:       capacity,
		PopulationSize: populationSize,
		CrossoverRate:  crossoverRate,
		MutationRate:   mutationRate,
		NumGenerations: numGenerations,
		TournamentSize: 5,
	}
}

// GenerateInitialPopulation generates the initial population of individuals
func (ga *GeneticAlgorithm) GenerateInitialPopulation(size int) {
	rand.Seed(time.Now().UnixNano())

	for i := 0; i < ga.PopulationSize; i++ {
		individual := make([]int, size)
		for j := 0; j < size; j++ {
			individual[j] = rand.Intn(2)
		}
		ga.Population = append(ga.Population, individual)
	}
}

// TournamentSelection performs selection by tournament
func (ga *GeneticAlgorithm) TournamentSelection(items []*Item) []int {
	bestSolution := make([]int, len(items))
	bestFitness := 0

	for i := 0; i < ga.TournamentSize; i++ {
		index := rand.Intn(len(ga.Population))
		solution := ga.Population[index]
		fitness := ga.FitnessFunction(solution, items)
		if fitness > bestFitness {
			copy(bestSolution, solution)
			bestFitness = fitness
		}
	}

	return bestSolution
}

// RouletteSelection performs selection by roulette
func (ga *GeneticAlgorithm) RouletteSelection(items []*Item) []int {
	totalFitness := 0.0
	for _, individual := range ga.Population {
		totalFitness += float64(ga.FitnessFunction(individual, items))
	}
	randomFitness := rand.Float64() * totalFitness

	cumulativeFitness := 0.0
	for _, individual := range ga.Population {
		fitness := float64(ga.FitnessFunction(individual, items))
		cumulativeFitness += fitness
		if cumulativeFitness >= randomFitness {
			return individual
		}
	}

	return nil
}

// Crossover performs crossover operation
func (ga *GeneticAlgorithm) Crossover(parent1, parent2 []int) ([]int, []int) {
	son1 := make([]int, len(parent1))
	son2 := make([]int, len(parent2))

	if rand.Float64() < ga.CrossoverRate {
		cut := rand.Intn(len(parent1))
		son1 = append(parent1[:cut], parent2[cut:]...)
		son2 = append(parent2[:cut], parent1[cut:]...)
	} else {
		copy(son1, parent1)
		copy(son2, parent2)
	}

	return son1, son2
}

// Mutate performs mutation operation
func (ga *GeneticAlgorithm) Mutate(offspring [][]int) [][]int {
	for _, son := range offspring {
		for i := range son {
			if rand.Float64() < ga.MutationRate {
				if son[i] == 1 {
					son[i] = 0
				} else {
					son[i] = 1
				}
			}
		}
	}
	return offspring
}

// FitnessFunction calculates the fitness value of a solution
func (ga *GeneticAlgorithm) FitnessFunction(solution []int, items []*Item) int {
	fitness := 0
	custo := 0

	for i, selected := range solution {
		if selected == 1 {
			fitness += items[i].Value
			custo += items[i].Weight
		}
	}

	if custo > ga.Capacity {
		p_exced := custo - ga.Capacity
		fmt.Printf("custo = %d, fitness = %d, p_exced = %d\n", custo, fitness, p_exced)
		sum_peso := 0
		c_penal := 0

		for i := 0; i < len(solution) && sum_peso < ga.Capacity; i++ {
			if solution[i] == 1 {
				sum_peso += items[i].Weight
				c_penal += items[i].Value
			}
		}
		fmt.Printf("sum_peso = %d, c_penal = %d\n", sum_peso, c_penal)
		penalty := c_penal * p_exced
		penalty2 := c_penal * sum_peso

		fitness -= penalty
		fmt.Printf("fitness = %d, penalty = %d, penalty2 = %d\n", fitness, penalty, penalty2)


		//excessRatio := float64(excessWeight) /float64(ga.Capacity)
		
		//fmt.Printf("excessWeight = %d, excessRatio = %f\n", excessWeight, excessRatio)
		

		//penaltyFraction := float64(excessRatio - 1)// Valor acima de 1 indica o quanto a capacidade foi excedida
		

		//total = 10700 - ex = 4 --- 2675
		//
		
		//penalty := int(float64(totalValue) / float64(excessRatio))
		//penalty2 := int(float64(totalValue) / float64(penaltyFraction))
		//penalty := math.Exp(float64(excessWeight))
		//penalty := math.Log(float64(excessWeight) + 1)
		//penalty := math.Pow(2, float64(excessWeight))


		//fmt.Printf("excessWeight = %d, penalty = %f\n", excessWeight, penalty)
		// penalty = min(penalty, totalValue)
// 
		// fmt.Printf("penalty = %d\n", penalty)
		//totalValue = int(float64(totalValue) / float64(penalty))
		if fitness <= 0{
			fitness = 1
		}
		//fmt.Printf("totalValue = %d\n", totalValue)
	}

	return fitness
}

// Função auxiliar para retornar o mínimo entre dois inteiros
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// GetValueForItems calculates the total value for selected items in the solution
func (ga *GeneticAlgorithm) GetValueForItems(solution []int, items []*Item) int {
	totalValue := 0
	for i, selected := range solution {
		if selected == 1 {
			totalValue += items[i].Value
		}
	}
	return totalValue
}

// GeneticAlgorithmKnapsack implements the genetic algorithm for the knapsack problem
func (ga *GeneticAlgorithm) GeneticAlgorithmKnapsack(items []*Item) []int {
	ga.GenerateInitialPopulation(len(items))

	for gen := 0; gen < ga.NumGenerations; gen++ {
		nextGeneration := make([][]int, 0)

		for i := 0; i < ga.PopulationSize; i += 2 {
			parent1 := ga.RouletteSelection(items)
			parent2 := ga.RouletteSelection(items)

			offspring1, offspring2 := ga.Crossover(parent1, parent2)
			offspring := [][]int{offspring1, offspring2}

			offspring = ga.Mutate(offspring)
			nextGeneration = append(nextGeneration, offspring[0], offspring[1])
		}

		ga.Population = nextGeneration

		bestLocal := make([]int, len(items))
		bestFitness := 0

		for _, individual := range ga.Population {
			fitness := ga.FitnessFunction(individual, items)
			if fitness > bestFitness {
				copy(bestLocal, individual)
				bestFitness = fitness
			}
		}

		value := ga.GetValueForItems(bestLocal, items)
		ga.SolutionList = append(ga.SolutionList, value)
	}

	// Find the best solution in the last generation
	bestSolution := make([]int, len(items))
	bestFitness := 0

	for _, individual := range ga.Population {
		fitness := ga.FitnessFunction(individual, items)
		if fitness > bestFitness {//&& ga.IsValidSolution(individual, items) {
			copy(bestSolution, individual)
			bestFitness = fitness
		}
	}

	return bestSolution
}

// IsValidSolution verifica se uma solução é válida (ou seja, não excede a capacidade da mochila)
func (ga *GeneticAlgorithm) IsValidSolution(solution []int, items []*Item) bool {
	totalWeight := 0
	for i, selected := range solution {
		if selected == 1 {
			totalWeight += items[i].Weight
			if totalWeight > ga.Capacity {
				return false
			}
		}
	}
	return true
}

func createItemsListFromTxtFile(path string) ([]*Item, int, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, 0, err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var population []*Item
    var capacity int

    for i := 0; scanner.Scan(); i++ {
        line := scanner.Text()
        if i == 0 {
            capacity, err = strconv.Atoi(line)
            if err != nil {
                return nil, 0, err
            }
            continue
        }
        split := strings.Split(line, ",")
        if len(split) != 3 {
            continue
        }
        weight, err := strconv.Atoi(split[1])
        if err != nil {
            return nil, 0, err
        }
        value, err := strconv.Atoi(split[2])
        if err != nil {
            return nil, 0, err
        }
        population = append(population, &Item{Weight: weight, Value: value})
    }

    if err := scanner.Err(); err != nil {
        return nil, 0, err
    }

    return population, capacity, nil
}

func main() {
	// Example of items and knapsack capacity
	
	//items := []*Item{
	//	{Weight: 1, Value: 200},
	//	{Weight: 1, Value: 210},
	//	{Weight: 1, Value: 280},
	//	{Weight: 2, Value: 200},
	//	{Weight: 3, Value: 700},
	//	{Weight: 3, Value: 750},
	//	{Weight: 3, Value: 720},
	//	{Weight: 4, Value: 140},
	//	{Weight: 4, Value: 340},
	//	{Weight: 4, Value: 240},
	//	{Weight: 5, Value: 500},
	//	{Weight: 6, Value: 300},
	//	{Weight: 7, Value: 600},
	//	{Weight: 8, Value: 300},
	//	{Weight: 9, Value: 300},
	//	{Weight: 1, Value: 800},
	//	{Weight: 1, Value: 800},
	//	{Weight: 1, Value: 600},
	//	{Weight: 2, Value: 300},
	//	{Weight: 2, Value: 310},
	//	{Weight: 2, Value: 390},
	//	{Weight: 5, Value: 300},
	//	{Weight: 10, Value: 800},
	//	{Weight: 10, Value: 900},
	//	{Weight: 10, Value: 2000},
	//	{Weight: 15, Value: 3000},
	//}
	//capacity := 15

	items, capacity, err := createItemsListFromTxtFile("/home/igorcr/Downloads/esboco_python-20240416T111551Z-001/esboco_python/instancias-mochila/KNAPDATA40.txt")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

	// Genetic algorithm parameters
	populationSize := 200
	crossoverRate := 0.85
	mutationRate := 0.15
	numGenerations := 1000

	ga := NewGeneticAlgorithm(capacity, populationSize, crossoverRate, mutationRate, numGenerations)
	solution := ga.GeneticAlgorithmKnapsack(items)

	// Print the solution
	fmt.Println("Selected items:")
	totalWeight := 0
	totalValue := 0
	for i, item := range items {
		if solution[i] == 1 {
			fmt.Printf("Item %d: Weight = %d, Value = %d\n", i+1, item.Weight, item.Value)
			totalWeight += item.Weight
			totalValue += item.Value
		}
	}
	fmt.Printf("Total weight = %d, Total value = %d\n", totalWeight, totalValue)
}