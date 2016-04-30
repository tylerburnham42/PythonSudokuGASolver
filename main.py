import random
import pprint
import threading
import time
import datetime
import os
from multiprocessing import Process
from gene import Gene
import matplotlib.pyplot as plt
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
    #pp.pprint(population)
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

def threading_append_population(new_population,population, tournament_size, mutation_precentage,additional_mutation_constant):
    new_population.append(two_parent_tournament_select(population, tournament_size, mutation_precentage + additional_mutation_constant))


def evolve_until_convergence(population, max_epochs, start_mutation_precentage, mutation_generations_increase, mutation_generations_increase_percentage, generation_wipe_after, tournament_size, elitism, startTime, logFileName, graphsDirectory):
    population_size = len(population)
    
    generation = 0 
    previous_best = 100000
    generations_at_current_best = 1 
    mutation_precentage = start_mutation_precentage
    
    max_fitness = []
    avg_fitness = []
    while (population[0].Get_Fitness() >= 1 and generation <= max_epochs):
        new_population = []
        #print("-----------")
        #pp.pprint(new_population)
        #pp.pprint(population)
        
        #Keep the Top Genes
        for top_gene in range(elitism):
            new_population.append(population[top_gene])
        
        while len(new_population) != population_size:
            new_population.append(two_parent_tournament_select(population, tournament_size, mutation_precentage))
            #new_population.append(one_parent_tournament_select(population, tournament_size, mutation_precentage))

        new_population.sort()
        population = new_population
        
        #Increase mutation constant
        if(round(previous_best) == round(population[0].Get_Fitness())):
            generations_at_current_best += 1
            if(generations_at_current_best % mutation_generations_increase == 0 and mutation_precentage != 1):
                if (mutation_precentage < 1):
                    mutation_precentage += mutation_generations_increase_percentage
                else:
                    mutation_precentage = 1
        else:
            previous_best = population[0].Get_Fitness()
            generations_at_current_best = 1
            mutation_precentage = start_mutation_precentage
        
        if(generations_at_current_best >= generation_wipe_after):
            print("---------Wiping Population-----------")
            population = create_population(population_size, population[0].correct_board, population[0].width, population[0].height)
        
        generation += 1
        
        max_fitness.append(population[0].Get_Fitness())
        avg_fitness.append(sum([x.Get_Fitness() for x in population])/population_size)        
        
        if(generation % 10 == 0):
            print("Generation " + str(generation))
            print("Current Time: " + "%.2f" % (time.clock() - startTime))
            print("Fitness: " + "%.2f" %(max_fitness[-1]))
            print("Avg Fitness: " + "%.2f" %(avg_fitness[-1]))
            print("Current Mutation: " + "%.2f" %(mutation_precentage))
            print("Generations At current Best: " + str(generations_at_current_best))
            print("Best Grid\n" + population[0].pretty_print() + '\n')
            print()
            #pp.pprint(population)
            
        if(generation % 50 == 0):
            outfile = open(logFileName, 'a')
            outfile.write("--------------------------------------" + '\n')
            outfile.write("Generation: " + str(generation) + '\n')
            outfile.write("Current Time: " + "%.2f" % (time.clock() - startTime) + '\n')
            outfile.write("Fitness: " + "%.2f" %(max_fitness[-1]) + '\n')
            outfile.write("Avg Fitness: " + "%.2f" %(avg_fitness[-1]) + '\n')
            outfile.write("Current Mutation: " + "%.2f" % (mutation_precentage) + '\n')
            outfile.write("Generations At current Best: " + "%.2f" % (generations_at_current_best) + '\n\n')
            outfile.write(population[0].pretty_print() + '\n')
            #outfile.write(pp.pformat(population) + '\n\n')
            outfile.close()
        if(generation % 50 == 0):            
            plotResults(graphsDirectory + '/Graph'+str(generation) +'.png', max_fitness, avg_fitness)
            
            
    #print(max_fitness)
    #pp.pprint(population)
    
    return (population,generation,max_fitness, avg_fitness)

def plotResults(fileName, max_fitness, avg_fitness):

    plt.plot(range(len(max_fitness)), max_fitness, label='Max Fitness', color = 'blue', )
    plt.plot(range(len(avg_fitness)), avg_fitness, label='Avg Fitness', color = 'red', )


    plt.title("Fitness vs Generations")
    plt.xlabel('Epoch')
    plt.ylabel('Fitness')
    plt.legend(loc='upper right')
    plt.savefig(fileName) 
    plt.close()  

def main():
    
    #Constants
    population_size = 10000
    max_epochs = 1000000000
    mutation_precentage = .2
    mutation_generations_increase = 1
    mutation_generations_increase_percentage = .1
    generation_wipe_after = 5000000
    tournament_size = 5
    elitism = 0
    
    startTime = time.clock()
    
    mainDirectory = "Runs"
    subDirectory = mainDirectory + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')
    graphsDirectory = subDirectory + '/' + 'graphs'
    logFileName =  subDirectory + '/' +  "log.txt"
    outputFileName = subDirectory + '/' +  "out.txt"
    plotFileName = subDirectory + '/' +  "graph.png"
    runInfoFileName = subDirectory + '/' +  "runInfo.txt"

    if not os.path.exists(mainDirectory):
        os.makedirs(mainDirectory)
    if not os.path.exists(subDirectory):
        os.makedirs(subDirectory)
    if not os.path.exists(graphsDirectory):
        os.makedirs(graphsDirectory)

    outfile = open(runInfoFileName, 'a')
    outfile.write("------------Settings-------------\n")
    outfile.write("population_size = "+str(population_size) + '\n')
    outfile.write("mutation_precentage = "+str(mutation_precentage) + '\n')
    outfile.write("mutation_generations_increase = "+ "%.2f" %(mutation_generations_increase) + '\n')
    outfile.write("mutation_generations_increase_percentage = "+ "%.2f" %(mutation_generations_increase_percentage) + '\n')
    outfile.write("tournament_size = "+str(tournament_size) + '\n')
    outfile.write("elitism = " + str(elitism) + '\n\n')
    outfile.close()

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
                                                                                elitism,
                                                                                startTime,
                                                                                logFileName,
                                                                                graphsDirectory)
    
    outfile = open(outputFileName, 'a')
    outfile.write("------------Settings-------------\n")
    outfile.write("population_size = "+str(population_size) + '\n')
    outfile.write("mutation_precentage = "+str(mutation_precentage) + '\n')
    outfile.write("mutation_generations_increase = "+ "%.2f" %(mutation_generations_increase) + '\n')
    outfile.write("mutation_generations_increase_percentage = "+ "%.2f" %(mutation_generations_increase_percentage) + '\n')
    outfile.write("tournament_size = "+str(tournament_size) + '\n')
    outfile.write("elitism = " + str(elitism) + '\n\n')

    outfile.write("------------Results-------------\n")
    outfile.write("Generations: " + str(generation) + '\n')
    outfile.write("Final Time: " + "%.2f" % (time.clock() - startTime) + '\n')
    outfile.write(str(input_board) + '\n')
    outfile.write(str(population[0].board)+ '\n')
    outfile.write(str(max_fitness)+ '\n')
    outfile.write(str(avg_fitness)+ '\n\n')
    outfile.write(population[0].pretty_print() + '\n')
    
    plotResults(plotFileName, max_fitness, avg_fitness)

if __name__ == '__main__':
    main()