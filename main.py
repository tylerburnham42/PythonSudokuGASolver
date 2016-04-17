import random
import pprint
import threading
from gene import Gene
pp = pprint.PrettyPrinter(indent=4)


def create_input_board(filename):
    file = open(filename, 'r')
    width, height = [int(dims) for dims in file.readline().split()]
    input_board = file.readline().strip().split(',')
    return (input_board, width, height)

def create_population(population_size, input_board, width, height):
    population = []
    for x in range(population_size):
        gene = Gene(input_board, width, height)
        population.append(gene)
    
    population.sort()
    pp.pprint(population)
    return population

def two_parent_tournament_select(population, tournament_size, mutation_precentage):
    tournament = sorted(random.sample(population, tournament_size))
    new_gene = Gene.Create_Gene_From_Parent(Gene, tournament[0], tournament[1])
    new_gene.Mutate(mutation_precentage)
    return new_gene 
    
def one_parent_tournament_select(population, tournament_size, mutation_precentage):
    tournament = sorted(random.sample(population, tournament_size))
    new_gene = Gene.Create_Gene_From_Parent(Gene,tournament[0])
    new_gene.Mutate(mutation_precentage)
    return new_gene 

def evolve_until_convergence(population, max_epochs, mutation_precentage, mutation_generations_increase, mutation_generations_increase_percentage, generation_wipe_after, tournament_size, elitism):
    population_size = len(population)
    generation = 0 
    previous_best = 100000
    generations_at_current_best = 1 
    additional_mutation_constant = 0
    
    max_fitness = []
    avg_fitness = []
    while (population[0].Get_Fitness() != 0 and generation <= max_epochs):
        new_population = []
        #print("-----------")
        #pp.pprint(new_population)
        #pp.pprint(population)
        
        #Keep the Top Genes
        for top_gene in range(elitism):
            new_population.append(population[top_gene])
        
        while len(new_population) != population_size:
            new_population.append(two_parent_tournament_select(population, tournament_size, mutation_precentage + additional_mutation_constant))
            #new_population.append(one_parent_tournament_select(population, tournament_size, mutation_precentage))

        new_population.sort()
        population = new_population
        
        #Increase mutation constant
        if(previous_best == population[0].Get_Fitness()):
            generations_at_current_best += 1
            if(generations_at_current_best % mutation_generations_increase == 0 and mutation_precentage + additional_mutation_constant <= .8):
                additional_mutation_constant += mutation_generations_increase_percentage
        else:
            previous_best = population[0].Get_Fitness()
            generations_at_current_best = 1
            additional_mutation_constant = 0
        
        if(generations_at_current_best >= generation_wipe_after):
            print("---------Wiping Population-----------")
            population = create_population(population_size, population[0].correct_board, population[0].width, population[0].height)
        
        generation += 1
        
        if(generation % 100 == 0):
            max_fitness.append(population[0].Get_Fitness())
            avg_fitness.append(sum([x.Get_Fitness() for x in population])/population_size)
            print("Generation " + str(generation))
            print("Fitness-" +str(max_fitness[-1]))
            print("Avg Fitness=" + str(avg_fitness[-1]))
            print("Current Mutation=" + str(mutation_precentage + additional_mutation_constant))
            print("Generations At current Best=" + str(generations_at_current_best))
            print()
            #pp.pprint(population)
            
        if(generation % 10000 == 0):
            outfile = open('log.txt', 'a')
            outfile.write("--------------------------------------" + '\n')
            outfile.write("Generation " + str(generation) + '\n')
            outfile.write("Fitness-" +str(max_fitness[-1]) + '\n')
            outfile.write("Avg Fitness=" + str(avg_fitness[-1]) + '\n')
            outfile.write("Current Mutation=" + str(mutation_precentage + additional_mutation_constant) + '\n')
            outfile.write("Generations At current Best=" + str(generations_at_current_best) + '\n\n')
            outfile.write(population[0].pretty_print() + '\n')
            #outfile.write(pp.pformat(population) + '\n\n')
            outfile.close()
            
            
    print(max_fitness)
    pp.pprint(population)
    
    return (population,generation,max_fitness,avg_fitness)

def main():
    
    #Constants
    population_size = 10
    max_epochs = 1000000000
    mutation_precentage = .1
    mutation_generations_increase = 10000
    mutation_generations_increase_percentage = .05
    generation_wipe_after = 500000
    tournament_size = 2
    elitism = 5

    #Read in Board
    input_board, width, height = create_input_board('in.txt')

    
    
    #Create Population
    population = create_population(population_size, input_board, width, height)
    
    
    population, generation, max_fitness, avg_fitness = evolve_until_convergence(population, 
                                                                                max_epochs,
                                                                                mutation_precentage,
                                                                                mutation_generations_increase,
                                                                                mutation_generations_increase_percentage,
                                                                                generation_wipe_after,
                                                                                tournament_size, 
                                                                                elitism)
    
    outfile = open('out.txt', 'a')
    outfile.write("Generations:" + str(generation) + '\n')
    outfile.write(str(input_board) + '\n')
    outfile.write(str(population[0].board)+ '\n')
    outfile.write(str(max_fitness)+ '\n')
    outfile.write(str(avg_fitness)+ '\n\n')

if __name__ == '__main__':
    main()