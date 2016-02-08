import random
import pprint
import copy
import math
import threading
pp = pprint.PrettyPrinter(indent=4)

class Gene:
    """A Simple Class to Represent a Gene"""
    correct_board = []
    board = []
    width = 0
    height = 0
    subsquare_width = 0
    subsquare_height = 0
    fitness = 0
    def __init__(self, correct_board, width, height, parent1 = None, parent2= None):
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
    def Update_Choices(self,board):
        self.board = board
        self.Update_Fitness()
    def Update_Fitness(self):
        self.fitness = 0
        #print("Gene")
        #print("Lines")
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
            
    def Mutate(self):
        mutation_precentage = .9
        while(random.randint(0,1000) < 1000*mutation_precentage):
            selection = random.randint(0, 1)
            #print("Mutation! " + str(selection))
            if(selection == 0):
                #Substution
                self.board[random.randint(0, len(self.board)-1)] = random.randint(1,self.width)
            if(selection == 1):
                #Swap
                rand = random.randint(0, len(self.board)-2)
                self.board[rand], self.board[rand+1] = self.board[rand+1], self.board[rand]
        
        self.replace_Fixed()
        self.Update_Fitness()
        
    def Crossover_Create_Two_Parents(self, parent1, parent2):
        new_board = copy.deepcopy(parent1.board)
        maxlength = len(self.board)
        limits = sorted([random.randint(0, maxlength) for k in range(2)])
        new_board[limits[0]:limits[1]] = parent2.board[limits[0]:limits[1]]
        self.board = new_board
        self.replace_Fixed()
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
        #Fill with Random Nummbers
        for line_num in range(self.height):
            self.board += random.sample(range(1,self.width+1),self.width)
            
        self.replace_Fixed()
        
        self.Update_Fitness()

    def replace_Fixed(self):
        #Replace with correct numbers 
        for num in range(len(self.correct_board)):
            if(self.correct_board[num] != 'X'):
                self.board[num] = int(self.correct_board[num])

def create_and_mutate(population, input_board, width, height, parent1, parent2):
    new_gene = Gene(input_board, width, height, parent1, parent2)
    new_gene.Mutate()
    population.append(new_gene)

def main():
    #Open and Read Data
    file = open('in.txt', 'r')
    width, height = [int(dims) for dims in file.readline().split()]
    input_board = file.readline().strip().split(',')
    
    #Constants
    population_size = 100   
    
    #Create Genes 
    population = []
    for x in range(population_size):
        gene = Gene(input_board, width, height)
        population.append(gene)
    
    population.sort()
    pp.pprint(population)
    print("--------------")
    generation = 0 
    max_fitness = []
    while population[0].Get_Fitness() != 0:
        parent1 = population[0]
        parent2 = population[1]
        population.clear()
        population.append(parent1)
        for i in range(population_size-1):
            #create_and_mutate(population, input_board, width, height, parent1, parent2)
            t = threading.Thread(target=create_and_mutate, args = (population, input_board, width, height, parent1, parent2))
            t.daemon = True
            t.start()

        population.sort()
        generation += 1
        if(generation % 1000 == 0):
            max_fitness.append(population[0].Get_Fitness())
            print("Generation " + str(generation))
            print("Fitness-" +str(population[0].Get_Fitness()))

    print(max_fitness)
    pp.pprint(population)
    
    outfile = open('out.txt', 'a')
    outfile.write("Generations:" + str(generation) + '\n')
    outfile.write(str(input_board) + '\n')
    outfile.write(str(population[0].board)+ '\n')
    outfile.write(str(max_fitness)+ '\n\n')

if __name__ == '__main__':
    main()