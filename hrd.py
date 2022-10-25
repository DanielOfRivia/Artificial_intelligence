#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import copy


# In[57]:


_, input_file, output_file1, output_file2 = sys.argv
# input_file = "d:\\Uni\\5th term\\AI\\Assignment1\\hrd_validate\\hrd_input2.txt"
# output_file1 = "d:\\Uni\\5th term\\AI\\Assignment1\\hrd_validate\\dfs.txt"
# output_file2 = "d:\\Uni\\5th term\\AI\\Assignment1\\hrd_validate\\hrd_outpu2.txt"
# In[3]:



# In[4]:


def transform_input(input_file):
    default_matrix = []
    width = 4
    height = 5
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            default_matrix.append([int(x) for x in line[:-1:]])
    check_matrix = [[1, 1, 1, 1] for i in range(height)]
    new_matrix = [[1, 1, 1, 1] for i in range(height)]
    for i in range(len(check_matrix)):
        for ii in range(len(check_matrix[0])):
            if check_matrix[i][ii] == 1:
                previous = default_matrix[i][ii]
                if previous == 1:
                    check_matrix[i][ii] = 0
                    check_matrix[i+1][ii] = 0
                    check_matrix[i][ii+1] = 0
                    check_matrix[i+1][ii+1] = 0
                    continue
                if previous == 7:
                    new_matrix[i][ii] = 4
                    check_matrix[i][ii] = 0
                    continue
                if previous == 0:
                    new_matrix[i][ii] = 0
                    check_matrix[i][ii] = 0
                    continue
                if i+1 == height:
                    new_matrix[i][ii] = 2
                    new_matrix[i][ii+1] = 2
                    check_matrix[i][ii] = 0
                    check_matrix[i][ii+1] = 0
                    continue
                if ii+1 == width:
                    new_matrix[i][ii] = 3
                    new_matrix[i+1][ii] = 3
                    check_matrix[i][ii] = 0
                    check_matrix[i+1][ii] = 0
                    continue 
                if previous == default_matrix[i][ii+1]:
                    new_matrix[i][ii] = 2
                    new_matrix[i][ii+1] = 2
                    check_matrix[i][ii] = 0
                    check_matrix[i][ii+1] = 0
                    continue
                else:
                    new_matrix[i][ii] = 3
                    new_matrix[i+1][ii] = 3
                    check_matrix[i][ii] = 0
                    check_matrix[i+1][ii] = 0
    return new_matrix


# In[5]:


def get_gap_corrdinates(matrix):
    found = False
    for i in range(len(matrix)):
        for ii in range(len(matrix[0])):
            if matrix[i][ii] == 0:
                if found:
                    p2 = (i, ii)
                    return (p1, p2)
                else:
                    p1 = (i, ii)
                    found = True
                


def is_previous_new(explored, current_state):
    st = current_state.state
    for i in range(len(explored)):
        if explored[-(i+1)].state == st:
            return True
    return False


# In[8]:


def is_win(state):
    if (state[4][1] == 1) and (state[4][2] == 1):
        # print("WIN!!!")
        return True
    return False


# In[9]:


def dfs (frontier, explored):
    current_state = frontier.pop() 
    if not (is_previous_new(explored, current_state)):
        if is_win(current_state.state):
            return current_state
        explored.append(current_state)
        add_moves_new(current_state, frontier) 
    return 
    


# In[10]:


def run_DFS(initial):
    explored = []
    res = []
    frontier = [Path_State_A_Search(initial, [])]
    current_state = frontier.pop() #???
    explored.append(current_state)
    add_moves_new(current_state, frontier) #do first move
    while not res:
        res = dfs(frontier, explored)
    return res

            
def calculate_f(state, cost):
    for i in range(5):
        for ii in range(4):
            if state[i][ii] == 1:
                h = abs(3-i) + abs(1-ii)
                return h + cost

def calculate_my_f(state,cost):
    for i in range(5):
        for ii in range(4):
            if state[i][ii] == 1:
                h = abs(3-i) + abs(1-ii) + (int((state[4][1] == 2) or (state[4][1] == 3)) + int((state[4][2] == 2) or (state[4][2] == 3)))*0.5
                return h + cost


# In[15]:


def add_moves_new(current_state, frontier):
    gap1 = current_state.gap1
    gap2 = current_state.gap2
    check_gap_simple_moves_new(current_state, frontier, gap1)
    check_gap_simple_moves_new(current_state, frontier, gap2)
    check_hard_moves_new(current_state, frontier, gap1, gap2)


# In[16]:


def check_gap_simple_moves_new(current_state, frontier, gap1):
    #check left
    if gap1[1] != 0:
        if current_state.state[gap1[0]][gap1[1]-1] == 4:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]][gap1[1]-1] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 4
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        elif current_state.state[gap1[0]][gap1[1]-1] == 2:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]][gap1[1]-2] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 2
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
    #check right
    if gap1[1] != 3:
        if current_state.state[gap1[0]][gap1[1]+1] == 4:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]][gap1[1]+1] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 4
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        elif current_state.state[gap1[0]][gap1[1]+1] == 2:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]][gap1[1]+2] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 2
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
    #check up
    if gap1[0] != 0:
        if current_state.state[gap1[0]-1][gap1[1]] == 4:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]-1][gap1[1]] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 4
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        elif current_state.state[gap1[0]-1][gap1[1]] == 3:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]-2][gap1[1]] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 3
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
    #check down
    if gap1[0] != 4:
        if current_state.state[gap1[0]+1][gap1[1]] == 4:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]+1][gap1[1]] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 4
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        elif current_state.state[gap1[0]+1][gap1[1]] == 3:
            changed_state_matrix = copy.deepcopy(current_state.state)
            changed_state_matrix[gap1[0]+2][gap1[1]] = 0
            changed_state_matrix[gap1[0]][gap1[1]] = 3
            frontier.append(Path_State_A_Search(changed_state_matrix, current_state))


# In[17]:


def check_hard_moves_new(current_state, frontier, gap1, gap2):
    #check horizontal
    if (gap1[0] == gap2[0]) and (abs(gap1[1] - gap2[1]) == 1):
        #check up
        if gap1[0] != 0:
            if(current_state.state[gap1[0] - 1][gap1[1]] == 2) and (current_state.state[gap2[0] - 1][gap2[1]] == 2) and (
                (gap1[1] % 3 == 0) or (gap2[1] % 3 == 0) or (current_state.state[gap1[0] - 1][gap1[1]-1] != 2) or (current_state.state[gap1[0] - 1][gap1[1] + 1] != 2)
            ):
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]-1][gap1[1]] = 0
                changed_state_matrix[gap2[0]-1][gap2[1]] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 2
                changed_state_matrix[gap2[0]][gap2[1]] = 2
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
            elif current_state.state[gap1[0] - 1][gap1[1]] == current_state.state[gap2[0] - 1][gap2[1]] == 1:
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]-2][gap1[1]] = 0
                changed_state_matrix[gap2[0]-2][gap2[1]] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 1
                changed_state_matrix[gap2[0]][gap2[1]] = 1
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        #check down
        if gap1[0] != 4:
            if(current_state.state[gap1[0] + 1][gap1[1]] == 2) and (current_state.state[gap2[0] + 1][gap2[1]] == 2) and (
                (gap1[1] % 3 == 0) or (gap2[1] % 3 == 0) or (current_state.state[gap1[0] + 1][gap1[1]-1] != 2) or (current_state.state[gap1[0] + 1][gap1[1] + 1] != 2)
            ):
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]+1][gap1[1]] = 0
                changed_state_matrix[gap2[0]+1][gap2[1]] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 2
                changed_state_matrix[gap2[0]][gap2[1]] = 2
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
            elif current_state.state[gap1[0] + 1][gap1[1]] == current_state.state[gap2[0] + 1][gap2[1]] == 1:
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]+2][gap1[1]] = 0
                changed_state_matrix[gap2[0]+2][gap2[1]] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 1
                changed_state_matrix[gap2[0]][gap2[1]] = 1
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))    
    #check vertical
    if (gap1[1] == gap2[1]) and (abs(gap1[0] - gap2[0]) == 1):
        #check left
        if gap1[1] != 0:
            if(current_state.state[gap1[0]][gap1[1] - 1] == 3) and (current_state.state[gap2[0]][gap2[1] - 1] == 3) and (
                (gap1[0] % 4 == 0) or (gap2[0] % 4 == 0) or (current_state.state[gap1[0] - 1][gap1[1]-1] != 3) or (current_state.state[gap1[0] + 1][gap1[1] - 1] != 3)
            ):
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]][gap1[1]-1] = 0
                changed_state_matrix[gap2[0]][gap2[1]-1] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 3
                changed_state_matrix[gap2[0]][gap2[1]] = 3
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
            elif current_state.state[gap1[0]][gap1[1] - 1] == current_state.state[gap2[0]][gap2[1] - 1] == 1:
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]][gap1[1] - 2] = 0
                changed_state_matrix[gap2[0]][gap2[1] - 2] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 1
                changed_state_matrix[gap2[0]][gap2[1]] = 1
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
        #check right
        if gap1[1] != 3:
            if(current_state.state[gap1[0]][gap1[1] + 1] == 3) and (current_state.state[gap2[0]][gap2[1] + 1] == 3) and (
                (gap1[0] % 4 == 0) or (gap2[0] % 4 == 0) or (current_state.state[gap1[0] - 1][gap1[1]+1] != 3) or (current_state.state[gap1[0] + 1][gap1[1] + 1] != 3)
            ):
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]][gap1[1]+1] = 0
                changed_state_matrix[gap2[0]][gap2[1]+1] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 3
                changed_state_matrix[gap2[0]][gap2[1]] = 3
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))
            elif current_state.state[gap1[0]][gap1[1] + 1] == current_state.state[gap2[0]][gap2[1] + 1] == 1:
                changed_state_matrix = copy.deepcopy(current_state.state)
                changed_state_matrix[gap1[0]][gap1[1] + 2] = 0
                changed_state_matrix[gap2[0]][gap2[1] + 2] = 0
                changed_state_matrix[gap1[0]][gap1[1]] = 1
                changed_state_matrix[gap2[0]][gap2[1]] = 1
                frontier.append(Path_State_A_Search(changed_state_matrix, current_state))


# In[55]:


def print_path_new(path, file_name):
    f = open(file_name, "w")
    new_path = reverse_path(path)
    f.write("Cost of the solution: " + str(len(new_path) - 1))
    while new_path:
        current_element = new_path.pop()
        f.write('\n')
        for i in range(len(current_element)):
            f.write(''.join(map(str, current_element[i])))
            f.write('\n')
    f.close()


# In[46]:


class Path_State_A_Search():
    def __init__(self, state, previous, manhattan_h = True):
        self.state = state
        self.previous = previous
        if previous:
            self.cost = previous.cost+1
            self.manhattan_h = previous.manhattan_h
        else:
            self.cost = 0
            self.manhattan_h = manhattan_h
        self.f_n = calculate_f(self.state, self.cost) if manhattan_h else calculate_my_f(self.state, self.cost)
        self.gap1, self.gap2 = get_gap_corrdinates(self.state)


# In[21]:


def reverse_path(path):
    new_path = [path.state]
    while path.previous:
        path = path.previous
        new_path.append(path.state)
    return new_path


# In[22]:
#if slow then frontier should be ordered from highest to lowest f 
def choose_successor(frontier):
    min_f = frontier[0].f_n
    chosen = 0
    for i in range(len(frontier)):
        if frontier[i].f_n < min_f:
            min_f = frontier[i].f_n
            chosen = i
    return frontier.pop(chosen)


# In[23]:
def a_search (frontier, explored):
    while True:
        current_state = choose_successor(frontier)
        hashed = hash_func(current_state.state)
        if hashed not in explored:
            if is_win(current_state.state):
                return current_state
            explored[hashed] = current_state
            add_moves_new(current_state, frontier) 


# In[24]:


def run_a_search(initial):
    explored = {} # dictionary containing number->State
    res = []
    frontier = []
    current_state = Path_State_A_Search(initial, [])
    explored[hash_func(initial)] = current_state
    add_moves_new(current_state, frontier) #do first move
    return a_search(frontier,explored)


# In[44]:


def run_my_search(initial):
    explored = {} # dictionary containing number->State
    res = []
    frontier = []
    current_state = Path_State_A_Search(initial, [], False)
    explored[hash_func(initial)] = current_state
    add_moves_new(current_state, frontier) #do first move
    while True:
        current_state = choose_successor(frontier)
        if current_state.cost == 43:
            print()
        hashed = hash_func(current_state.state)
        if hashed not in explored:
            if is_win(current_state.state):
                return current_state
            explored[hashed] = current_state
            add_moves_new(current_state, frontier) 


# In[26]:


def hash_func(matrix):
    res = 0
    for i in range(20):
        res += matrix[i//4][i%4] * 10**(i)
    return res


# In[27]:
# def transform_file(file_path): #to hashed
#     res_l = []
#     with open(file_path) as f:
#         lines = f.readlines()
#         lines.pop(0)
#         res = 0
#         i = 0
#         for line in lines:
#             if line[0] == '\n':
#                 res_l.append(res)
#                 res = 0
#                 i = 0
#             else:
#                 for n in line[:-1]:
#                     res += int(n) * 10**i
#                     i += 1
#     return res_l

# def check_correctness(current_state, list_of_correct):
#     hashed = hash_func(current_state.state)
#     if hashed in list_of_correct:
#         if hashed != list_of_correct.pop(0):
#             raise Exception(str(current_state.cost))

# In[39]:

initial = transform_input(input_file)
print_path_new(run_DFS(initial), output_file1)
print_path_new(run_a_search(initial), output_file2)
