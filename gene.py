import math
import random
import copy

class Gene(object):
    """A Simple Class to Represent a Gene"""
    
    def __init__(self, correct_board, width, height, parent1 = None, parent2 = None):
        self.width = width
        self.height = height
        self.subsquare_width = int(math.sqrt(width))
        self.subsquare_height = int(math.sqrt(height))
        self.correct_board = correct_board
        self.board = []
        self.fitness = 0
        
        if(parent1 != None and parent2 != None):
            self.Crossover_Create(parent1,parent2)
        elif(parent1 != None):
            self.Crossover_Create(parent1)
        else:
            self.Gene_Create()
        return 
        
    def Create_Gene_From_Parent(cls, parent1, parent2 = None):
        if(parent2 == None):
            return Gene(parent1.correct_board, parent1.width, parent1.height, parent1)
        else:
            return Gene(parent1.correct_board, parent1.width, parent1.height, parent1, parent2)
            
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
        
        #Add Random Precentage
        self.fitness += random.random()
        
        #print("Fitness:" + str(self.fitness))
        #print(self)
            
    def Mutate(self, mutation_precentage):
        count = 0
        while(random.randint(0,1000) < 1000*mutation_precentage and count < 30):
            count += 1
            selection = random.randint(0, 100)
            #print("Mutation! " + str(selection))
            if(selection <= 33):
                #Substution
                substute_index = -1
                while(substute_index != -1 and self.correct_board[substute_index] != 'X' ):
                    substute_index = random.randint(0, len(self.board)-1)
                self.board[substute_index] = random.randint(1,self.width)
            elif(selection <= 66):
                #Swap random
                rand_pos1 = -1
                rand_pos2 = -1
                while(rand_pos1 != -1 and self.correct_board[rand_pos1] != 'X' and self.correct_board[rand_pos2] != 'X' ):
                    rand_pos1, rand_pos2  = random.sample(range(len(self.board)), 2)
                
                self.board[rand_pos1], self.board[rand_pos2] = self.board[rand_pos2], self.board[rand_pos1]
            elif(selection <= 100):
                #Shuffle Row
                row_num = random.randint(0, self.height-1)
                row = self.board[self.width*row_num:self.width*(1+row_num)]
                random.shuffle(row)
                self.board[self.width*row_num:self.width*(1+row_num)] = row
                self.replace_Fixed()

#            elif(selection <= 75):
#                #Substute with incorrect check
#                substute_index = -1
#                locations = [x for x in range(len(self.board))]
#                random.shuffle(locations)
#                current_location = 0
#                while(substute_index != -1 and self.correct_board[substute_index] != 'X' and current_location < len(self.board)):
#                    index = locations[current_location]
#                    if(self.index_is_incorect(index) > 0):
#                        substute_index = index
#                        
#                    current_location += 1
#                    
#                self.board[substute_index] = random.randint(1,self.width)
#            elif(selection <= 100):
#                #Swap with incorrect check
#                rand_pos1 = -1
#                rand_pos2 = -1
#                
#                #Find an Incorrect Value for #1
#                locations = [x for x in range(len(self.board))]
#                random.shuffle(locations)
#                current_location = 0
#                while(rand_pos1 != -1 and self.correct_board[rand_pos1] != 'X' and current_location < len(self.board)):
#                    index = locations[current_location]
#                    if(self.index_is_incorect(index) > 0):
#                        rand_pos1 = index
#                    current_location += 1
#            
#                #Find an Incorrect Value for #2
#                locations = [x for x in range(len(self.board))]
#                random.shuffle(locations)
#                current_location = 0
#                while(rand_pos2 != -1 and self.correct_board[rand_pos2] != 'X' and current_location < len(self.board)):
#                    index = locations[current_location]
#                    if(self.index_is_incorect(index) > 0):
#                        rand_pos2 = index
#                    current_location += 1
#
#                #Swap them
#                self.board[rand_pos1], self.board[rand_pos2] = self.board[rand_pos2], self.board[rand_pos1]
            


#            elif(selection <= 100):
#                #Local Search 
#            
#                #Get a random row
#                row_num = random.randint(0, self.height-1)
#                row = self.board[self.width*row_num:self.width*(1+row_num)]
#                row_set = set(row)
#                
#                #If the row does not contain every number
#                if(len(row_set) != self.width):
#                    #Find a number not in the set
#                    number = -1                    
#                    for i in range(1,self.width+1):
#                        if i not in row_set:
#                            number = i
#                            break
#                    
#                    #Find a Duplicate number
#                    new_number = -1                    
#                    for i in range(1,self.width+1):
#                        if i not in row_set:
#                            new_number = i
#                            break
#                        else:
#                            row_set.remove(i)
#                        
#                    #Check spots for fixed spots
#                    check_order = list(range(self.width))
#                    random.shuffle(check_order)
#                    for j in check_order:
#                        if(self.correct_board[self.width*row_num+j] != 'X' and self.board[self.width*row_num+j] == new_number):
#                            row[j] = number
#                                    
#                        break
#                    
#                    #Replace the board 
#                    self.board[self.width*row_num:self.width*(1+row_num)] = row
#                    
#                #Do Nothing
                

        
        self.Update_Fitness()
        
    def Crossover_Create(self, parent1, parent2 = None):
        if(parent2 == None):
            parent2 = Gene(self.correct_board, self.width, self.height)
        self.board = copy.deepcopy(parent1.board)
        
        #Random Crossever
        selection = random.randint(0, 1)
        if(selection == 0):
            self.Column_Crossover(parent2)
        if(selection == 1):
            self.Line_Crossover(parent2)
        else:
            self.Random_Crossover(parent2)

        self.Update_Fitness()
        

    def Random_Crossover(self, parent):
        maxlength = len(self.board)
        limits = sorted([random.randint(0, maxlength) for k in range(2)])
        self.board[limits[0]:limits[1]] = parent.board[limits[0]:limits[1]]

    def Line_Crossover(self,parent):
        line_number = random.randint(0, self.height)
        self.board[self.width*line_number:self.width*(1+line_number)] = parent.board[self.width*line_number:self.width*(1+line_number)]
    
    def Column_Crossover(self,parent):
         column_number = random.randint(0, self.width)
         self.board[column_number::self.width] = parent.board[column_number::self.width]
        
        

    def Get_Fitness(self): 
        return self.fitness
    def __lt__(self, other):
        return (self.fitness) < (other.fitness)
    def __repr__(self):
        return("Fitness:" + str(self.fitness) + "-" + str(self.board))
    def pretty_print(self):
        pretty_board = ""
        current_row = 0
        for x in range(self.width):
            if(current_row % pow(self.height,0.5)) == 0 and (current_row != 0) and (current_row != self.height-1):       
                pretty_board += '\n'
            row = self.board[self.width*x:self.width*(1+x)]
            pretty_board += "["
            for y in range(len(row)):
                if(y % pow(self.width,0.5) == 0 and (y != 0) and (y != self.width-1)):
                    pretty_board += ']['
                
                is_incorrect = self.index_is_incorect(y+current_row*self.width)
                if(is_incorrect == 1):
                    pretty_board += '(' + str(row[y]) + ')'
                elif(is_incorrect == 2):
                    pretty_board += '{' + str(row[y]) + '}'
                elif(is_incorrect == 3):
                    pretty_board += '<' + str(row[y]) + '>'
                else:
                    pretty_board += ' ' + str(row[y]) + ' '
            
            pretty_board += ']\n'
            current_row += 1
        return(pretty_board)        
        
    def index_is_incorect(self,index):
        #Get the value at the index
        value = self.board[index]

        #create a temp booard and replace the value with -1        
        temp_board = self.board.copy()
        temp_board[index] = -1
        
        
        #Get line
        line_num = index // self.width
        line = temp_board[self.width*line_num:self.width*(1+line_num)]
        if(value in set(line) ):
            return 1 
        
        #Get column
        col_num = int(index % self.height)
        col = temp_board[col_num::self.width]
        if(value in set(col)):
            return 2
        
        #Get box
        box = []
        col_subsquare_num = (col_num//self.subsquare_height)*self.subsquare_height
        line_subsquare_num = (line_num//self.subsquare_width)*self.subsquare_width
        #print(str(col_subsquare_num) + " " +  str(line_subsquare_num))
        for offset in range(0,(self.width//self.subsquare_width)):
            off_width = offset*self.width
            box += temp_board[
                        col_subsquare_num+(line_subsquare_num*self.width)+off_width: #start ofset
                        col_subsquare_num+(line_subsquare_num*self.width)+self.subsquare_width+off_width]#End ofset
        #print(box)
        if(value in set(box)):
            return 3
            
        return 0    

        
        
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
 
