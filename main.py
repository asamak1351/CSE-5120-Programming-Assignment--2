from cmath import sqrt
import random
import time
import math


class solve_n_queen:
    
    #N_queens= -1
    def __init__(self, N_q):
        self.N_queens = N_q
        #we will assume that every row/col will only have one queen in it.
        # Therefore we will only swap two given rows on the board to preserved this property.
        # Moreover, we can then address a given queen by the row they are in.
        self.queen_locations = []
        #place queens diagonally
        for i in range(0,self.N_queens):
            self.queen_locations.append(i)
        #store the number of conflict for each queen
        self.queens_conflicts = []
        self.max_neighbors = math.factorial(self.N_queens) / (2 * math.factorial(self.N_queens - 2))
        self.all_paths = []
        #computes all paths
        for a in range(0,self.N_queens-1):
            for b in range(a+1,self.N_queens):
                self.all_paths.append([a,b])
    
    
    #calculate the numbers conflicts for a given queen
    def calc_conflicts(self, this_queen, q_locations):
        num_conflicts = -1
        #this queen row
        tq_row = this_queen
        #checking conflicts
        for row in range(0,self.N_queens):
            #checking conflict in diagonals
            if(abs(row - tq_row) == abs(q_locations[row] - q_locations[tq_row])):
                num_conflicts += 1
        return num_conflicts

    #queens_sorted_by_greatest_conflicts
    # returns the indices and number of conflict,
    # and sorted by greatest number of conflicts
    def get_conflicts_per_queen(self, q_locations):
        list_temp = []

        #get the conflict for every queen
        for i in range(0,self.N_queens):
            list_temp.append(self.calc_conflicts(i, q_locations))
        #sorted(list_temp, key=lambda x:x[1], reverse=True)
        return list_temp

    #give new array that where two elements in the array are swapped
    def swap_rows(self, old_q_locations, a, b):
        q_locations = old_q_locations.copy()
        t = q_locations[b]
        q_locations[b] = q_locations[a]
        q_locations[a] = t
        return q_locations

    #checks if the board is solved
    def is_solved(self):
        is_s = True
        self.queens_conflicts = self.get_conflicts_per_queen(self.queen_locations)
        for queen in self.queens_conflicts:
            if(queen > 0):
                is_s = False
                break
        return is_s

    #print the out the board
    def print_board(self):
        for queen in self.queen_locations:
            print("# "*queen+"Q"+ " #"*(self.N_queens - queen - 1))

    #get n path(s) to neighbor(s)
    def get_paths_to_neighbors(self, n_neighnors = None):
        if(n_neighnors == None or n_neighnors == self.max_neighbors):
            return self.get_all_paths_to_neighbors()
        if(n_neighnors > self.max_neighbors):
            print("(get_paths_to_neighbors) Warning: asked for more than neighbors than is possible.")

        return random.sample(self.all_paths,k=n_neighnors)
    
    #converts paths_to_neighbors to a list neighbor_nodes (ie neighbor_node is just q_locations)
    def get_neighbor_nodes(self, n_neighbors):
        neighbor_nodes = []
        for single_path in self.get_paths_to_neighbors(n_neighbors):
            neighbor_nodes.append(self.swap_rows(self.queen_locations, single_path[0], single_path[1]))
        return neighbor_nodes

    def solve_by_greedy_descent(self):
        while(not self.is_solved()):
            # print(sum(self.queens_conflicts))

            # n_neighbors = int(math.sqrt(self.max_neighbors)+2)
            n_neighbors = self.N_queens

            neighbor_nodes = self.get_neighbor_nodes(n_neighbors)

            #sorts neighbors_nodes by the total number of conflicts
            neighbor_nodes.sort(key=lambda x:sum(self.get_conflicts_per_queen(x)), reverse=False)
            
            #Make self whatever the best neighbor_node is
            self.queen_locations = neighbor_nodes[0]
    
    def solve_by_random_neighbor(self):
        while(not self.is_solved()):
            row_pair = self.get_random_neighbor()
            #print(row_pair)
            print(sum(self.queens_conflicts))
            self.queen_locations = self.swap_rows(self.queen_locations,row_pair[0],row_pair[1])
            #print("-----")
            #case.print_board()

#-------------------
N_samples = 1
print("Testing with %d samples" % (N_samples))
#[4,8,16,64,100,1000,10000]
for N_queen in [4,8,16,64,100,1000,10000]:
    start = time.time()
    for sample in range(N_samples):
        case = solve_n_queen(N_queen)
        case.solve_by_greedy_descent()
    end = time.time()
    print("%d queen done in %f; printing solution:" % (N_queen, (end - start)))
    case.print_board()
    
    

