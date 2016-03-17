import random
import pprint
import copy
import math
import threading
pp = pprint.PrettyPrinter(indent=4)

class Gene(object):
    """A Simple Class to Represent a Gene"""
    correct_board = []
    board = []
    width = 0
    height = 0
    subsquare_width = 0
    subsquare_height = 0
    fitness = 0
    def __init__(self, correct_board, width, height, parent1 = None, parent2 = None):
        self.width = width
        self.height = height
        self.subsquare_width = int(math.sqrt(width))
        self.subsquare_height = int(math.sqrt(height))
        self.correct_board = correct_board
        
        if(parent1 != None and parent2 != None):
            self.Crossover_Create_Two_Parents(parent1,parent2)
        elif(parent1 != None):
            self.Crossover_Create_One_Parent(parent1)
        else:
            self.Gene_Create()  
        return 
        
    def Create_Gene_From_Parent(cls, parent1, parent2= None):
        if(parent2 != None):
            return Gene(parent1.correct_board, parent1.width, parent1.height, parent1, parent2)
        else:
            return Gene(parent1.correct_board, parent1.width, parent1.height, parent1)


    def Update_Choices(self,board):
        self.board = board
        self.Update_Fitness()
    def Update_Fitness(self):
        self.fitness = 0

        #Get Line Incorrect Values
        for y in range(self.height):
            #print(self.board[self.width*y:self.width*(1+y)])
            line = self.board[self.width*y:self.width*(1+y)]
            self.fitness += self.width - len(set(line))

        #print("Columns")
        for x in range(self.height):
            #print(set(self.board[x::self.width]))
            col = self.board[x::self.width]
            self.fitness += self.height - len(set(col))
            
        #print("Squares")
        for y in range(0,self.height,self.subsquare_height):
            #print("Y=" + str(y))
            for x in range(0,self.width,self.subsquare_width):
                #print("X=" + str(x))
                line = []
                for offset in range(0,(self.width//self.subsquare_width)):
                    off_width = offset*self.width
                    line += self.board[
                    x+y*self.width+off_width: #start ofset
                    x+y*self.width+self.subsquare_width+off_width]#End ofset
                    
                #print(line)
                self.fitness += self.height - len(set(line))
            
        #print("Fitness:" + str(self.fitness))
        #print(self)
            
    def Mutate(self, mutation_precentage):
        while(random.randint(0,1000) < 1000*mutation_precentage):
            selection = random.randint(0, 2)
            #print("Mutation! " + str(selection))
            if(selection == 0):
                #Substution
                substute_index = -1
                while(substute_index == -1 or self.correct_board[substute_index] != 'X' ):
                    substute_index = random.randint(0, len(self.board)-1)
                self.board[substute_index] = random.randint(1,self.width)
            if(selection == 1):
                #Swap
                rand_pos1 = -1
                rand_pos2 = -1
                while(rand_pos1 == -1 or self.correct_board[rand_pos1] != 'X' or self.correct_board[rand_pos2] != 'X' ):
                    rand_pos1, rand_pos2  = random.sample(range(len(self.board)), 2)
                self.board[rand_pos1], self.board[rand_pos2] = self.board[rand_pos2], self.board[rand_pos1]
            if(selection == 2):
                #Local Search 
            
                row_num = random.randint(0, self.height-1)
                row = self.board[self.width*row_num:self.width*(1+row_num)]
                row_set = set(row)
                
                if(len(row_set) != self.width):
                    for i in range(1,self.width+1):
                        if i not in row_set:
                            check_order = list(range(self.width))
                            random.shuffle(check_order)
                            for j in check_order:
                                #print("J={}, Width ={} Row Num={}".format(j,self.width,row_num))
                                if(self.correct_board[self.width*row_num+j] != 'X'):
                                    row[j] = i
                                    break
                        break
                                
                self.board[self.width*row_num:self.width*(1+row_num)] = row            
                

        
        self.Update_Fitness()
        
    def Crossover_Create_Two_Parents(self, parent1, parent2):
        new_board = copy.deepcopy(parent1.board)
        maxlength = len(self.board)
        limits = sorted([random.randint(0, maxlength) for k in range(2)])
        new_board[limits[0]:limits[1]] = parent2.board[limits[0]:limits[1]]
        self.board = new_board
        self.Update_Fitness()
        
    def Crossover_Create_One_Parent(self, parent1):
        self.Gene_Create()
        maxlength = len(self.board)
        limits = sorted([random.randint(0, maxlength) for k in range(2)])
        self.board[limits[0]:limits[1]] = parent1.board[limits[0]:limits[1]]
        self.replace_Fixed()
        self.Update_Fitness()
        
    def Get_Fitness(self): 
        return self.fitness
    def __lt__(self, other):
        return (self.fitness) < (other.fitness)
    def __repr__(self):
        return("Fitness:" + str(self.fitness) + "-" + str(self.board))
    def Gene_Create(self):
        self.board = []
        
        count = 0
        #Fill with Random Nummbers
        for line_num in range(self.height):
            self.board += random.sample(range(1,self.width+1),self.width)
            if(self.correct_board[count] != 'X'):
                self.board[num] = int(self.correct_board[num])
            
        self.replace_Fixed()
        
        self.Update_Fitness()

    def replace_Fixed(self):
        #Replace with correct numbers 
        for num in range(len(self.correct_board)):
            if(self.correct_board[num] != 'X'):
                self.board[num] = int(self.correct_board[num])
            

















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

def evolve_until_convergence(population, mutation_precentage, tournament_size, elitism):
    population_size = len(population)
    generation = 0 
    max_fitness = []
    avg_fitness = []
    while population[0].Get_Fitness() != 0:
        new_population = []
        #print("-----------")
        #pp.pprint(new_population)
        #pp.pprint(population)
        
        #Keep the Top Genes
        for top_gene in range(elitism):
            new_population.append(population[top_gene])
        
        
        for i in range(population_size-1):
            tournament = sorted(random.sample(population, tournament_size))
            new_gene = Gene.Create_Gene_From_Parent(tournament[0], tournament[1])
            new_gene.Mutate(mutation_precentage)
            new_population.append(new_gene) 

        new_population.sort()
        population = new_population
        generation += 1
        if(generation % 10 == 0):
            max_fitness.append(population[0].Get_Fitness())
            avg_fitness.append(sum([x.Get_Fitness() for x in population])/population_size)
            print("Generation " + str(generation))
            print("Fitness-" +str(max_fitness[-1]))
            print("Avg Fitness=" + str(avg_fitness[-1]))
            print()
            #pp.pprint(population)
            
    print(max_fitness)
    pp.pprint(population)
    
    return (population,generation,max_fitness,avg_fitness)

def main():
    
    #Constants
    population_size = 100
    mutation_precentage = .1
    tournament_size = 5
    elitism = 5

    #Read in Board
    input_board, width, height = create_input_board('in.txt')
    
    #Create Population
    population = create_population(population_size, input_board, width, height)
    
    
    population, generation, max_fitness, avg_fitness = evolve_until_convergence(population, mutation_precentage, tournament_size, elitism)
    



    
    outfile = open('out.txt', 'a')
    outfile.write("Generations:" + str(generation) + '\n')
    outfile.write(str(input_board) + '\n')
    outfile.write(str(population[0].board)+ '\n')
    outfile.write(str(max_fitness)+ '\n\n')

if __name__ == '__main__':
    main()