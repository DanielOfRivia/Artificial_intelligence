#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import copy

_, input_file, output_file = sys.argv
# input_file = "d:/Uni/5th term/AI/Assignment2/in.txt"
# output_file = "d:/Uni/5th term/AI/Assignment2/out.txt"
# In[3]:


def transform_input(input_file):
    res = []
    k = 0
    with open(input_file) as f:
        line = f.readline()
        while line[-1] == '\n':
#             print(line)
#             print(line.split(''))
            all_fields = [*line[:-1:]]
            res.append(all_fields)
            line = f.readline()
            k+=1
        res.append([*line])
    return res


def utility_f(state):
    k = 0
    for y in range(8):
        for x in range(8):
            ch = state[y][x]
            if ch == 'b':
                if (x == 7) or (x == 0) or (y == 0) or (y == 7):
                    k-=0.1
                k -= 1
            elif ch == 'B':
                k -= 2
            elif ch == 'r':
                if (x == 7) or (x == 0) or (y == 0) or (y == 7):
                    k+=0.1
                k += 1
            elif ch == 'R':
                k += 2
    
    return k



# In[15]:


def generate_capture_simple(current_state, y, x, max_player):#y,x coordinates of red piece
    res = []
    if max_player:
        if y > 1:
            if (x > 1) and ((current_state[y-1][x-1] == 'b') or (current_state[y-1][x-1] == 'B')) and (current_state[y-2][x-2] == '.'):
                new_state = gen_new_state(current_state, y-2, x-2, y, x, max_player)
                new_res = generate_capture_simple(new_state, y-2, x-2, max_player)
                if not new_res:
                    res.append(new_state)
                else:
                    res += new_res

            if (x < 6) and ((current_state[y-1][x+1] == 'b') or (current_state[y-1][x+1] == 'B')) and (current_state[y-2][x+2] == '.'):
                new_state = gen_new_state(current_state, y-2, x+2, y, x, max_player)
                new_res = generate_capture_simple(new_state, y-2, x+2, max_player)
                if not new_res:
                    res.append(new_state)
                else:
                    res += new_res
    else:
        if y < 6:
            if (x > 1) and ((current_state[y+1][x-1] == 'r') or (current_state[y+1][x-1] == 'R')) and (current_state[y+2][x-2] == '.'):
                new_state = gen_new_state(current_state, y+2, x-2, y, x, max_player)
                new_res = generate_capture_simple(new_state, y+2, x-2, max_player)
                if not new_res:
                    res.append(new_state)
                else:
                    res += new_res
            if (x < 6) and ((current_state[y+1][x+1] == 'r') or (current_state[y+1][x+1] == 'R')) and (current_state[y+2][x+2] == '.'):
                new_state = gen_new_state(current_state, y+2, x+2, y, x, max_player)
                new_res = generate_capture_simple(new_state, y+2, x+2, max_player)
                if not new_res:
                    res.append(new_state)
                else:
                    res += new_res
    return res


# In[16]:


def gen_new_state(current_state, y1, x1, y2, x2, max_player, captured=[]): #check this action
    new_state = copy.deepcopy(current_state)
    if max_player:
        if captured:
            new_state[captured[0]][captured[1]] = '.'
        elif y2 - y1 == 2:
            new_state[y1+1][int((x1+x2)/2)] = '.'
        if y1 == 0:
            new_state[y1][x1] = 'R'
        else:
            new_state[y1][x1] = new_state[y2][x2]
    else:
        if captured:
            new_state[captured[0]][captured[1]] = '.'
        elif y1 - y2 == 2:
            new_state[y2+1][int((x1+x2)/2)] = '.'
        if y1 == 7:
            new_state[y1][x1] = 'B'
        else:
            new_state[y1][x1] = new_state[y2][x2]
    new_state[y2][x2] = '.'
    return new_state


# In[17]:


def generate_move_simple(current_state, y, x, max_player):
    res = []
    if max_player:
        if y > 0:
            if (x > 0) and (current_state[y-1][x-1]) == '.':
                res.append(gen_new_state(current_state, y-1, x-1, y, x, max_player))
            if (x < 7) and (current_state[y-1][x+1] == '.'):
                res.append(gen_new_state(current_state, y-1, x+1, y, x, max_player))
    else:
        if y < 6:
            if (x > 0) and (current_state[y+1][x-1]) == '.':
                res.append(gen_new_state(current_state, y+1, x-1, y, x, max_player))
            if (x < 7) and (current_state[y+1][x+1] == '.'):
                res.append(gen_new_state(current_state, y+1, x+1, y, x, max_player))
    return res


# In[18]:


def generate_move_king(current_state, y, x, max_player):
    res = []
    x1 = x+1
    y1 = y-1
    while (x1 <= 7) and (y1 >= 0):
        if current_state[y1][x1] == '.':
            res.append(gen_new_state(current_state, y1, x1, y, x, max_player))
        else: break
        x1 += 1
        y1 -= 1
    
    x1 = x-1
    y1 = y-1
    while (x1 >= 0) and (y1 >= 0):
        if current_state[y1][x1] == '.':
            res.append(gen_new_state(current_state, y1, x1, y, x, max_player))
        else: break
        x1 -= 1
        y1 -= 1
    
    x1 = x-1
    y1 = y+1
    while (x1 >= 0) and (y1 <= 7):
        if current_state[y1][x1] == '.':
            res.append(gen_new_state(current_state, y1, x1, y, x, max_player))
        else: break
        x1 -= 1
        y1 += 1
    
    x1 = x+1
    y1 = y+1
    while (x1 <= 7) and (y1 <= 7):
        if current_state[y1][x1] == '.':
            res.append(gen_new_state(current_state, y1, x1, y, x, max_player))
        else: break
        x1 += 1
        y1 += 1
    return res    


# In[30]:


def generate_capture_king(current_state, y, x, max_player):
    res = []
    if max_player:
        x1 = x+1
        y1 = y-1
        while (x1 <= 6) and (y1 >= 1):
            if (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                x2 = x1+1
                y2 = y1-1
                while (x2 <= 7) and (y2 >= 0) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 += 1
                    y2 -= 1
            elif (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                break
            x1 += 1
            y1 -= 1

        x1 = x-1
        y1 = y-1
        while (x1 >= 1) and (y1 >= 1):
            if (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                x2 = x1-1
                y2 = y1-1
                while (x2 >= 0) and (y2 >= 0) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 -= 1
                    y2 -= 1
            elif (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                break
            x1 -= 1
            y1 -= 1

        x1 = x-1
        y1 = y+1
        while (x1 >= 1) and (y1 <= 6):
            if (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                x2 = x1-1
                y2 = y1+1
                while (x2 >= 0) and (y2 <= 7) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 -= 1
                    y2 += 1
                break
            elif (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                break
            x1 -= 1
            y1 += 1

        x1 = x+1
        y1 = y+1
        while (x1 <= 6) and (y1 <= 6):
            if (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                x2 = x1+1
                y2 = y1+1
                while (x2 <= 7) and (y2 <= 7) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 += 1
                    y2 += 1
            elif (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                break
            x1 += 1
            y1 += 1
    else:
        x1 = x+1
        y1 = y-1
        while (x1 <= 6) and (y1 >= 1):
            if (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                x2 = x1+1
                y2 = y1-1
                while (x2 <= 7) and (y2 >= 0) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 += 1
                    y2 -= 1
            elif (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                break
            x1 += 1
            y1 -= 1

        x1 = x-1
        y1 = y-1
        while (x1 >= 1) and (y1 >= 1):
            if (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                x2 = x1-1
                y2 = y1-1
                while (x2 >= 0) and (y2 >= 0) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 -= 1
                    y2 -= 1
            elif (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                break
            x1 -= 1
            y1 -= 1

        x1 = x-1
        y1 = y+1
        while (x1 >= 1) and (y1 <= 6):
            if (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                x2 = x1-1
                y2 = y1+1
                while (x2 >= 0) and (y2 <= 7) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 -= 1
                    y2 += 1
            elif (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                break
            x1 -= 1
            y1 += 1

        x1 = x+1
        y1 = y+1
        while (x1 <= 6) and (y1 <= 6):
            if (current_state[y1][x1] == 'r') or (current_state[y1][x1] == 'R'):
                x2 = x1+1
                y2 = y1+1
                while (x2 <= 7) and (y2 <= 7) and (current_state[y2][x2] == '.'):
                    new_state = gen_new_state(current_state, y2, x2, y, x, max_player, (y1, x1))
                    new_res = generate_capture_king(new_state, y2, x2, max_player)
                    if not new_res:
                        res.append(new_state)
                    else:
                        res += new_res
                    x2 += 1
                    y2 += 1
            elif (current_state[y1][x1] == 'b') or (current_state[y1][x1] == 'B'):
                break
            x1 += 1
            y1 += 1
    return res    


def actions(current_state, max_player):
    res = []
    if max_player:
        for y in range(8):
            for x in range(8):
                if current_state[y][x] == 'r':
                    res += generate_capture_simple(current_state, y, x, max_player)
                elif current_state[y][x] == 'R':
                    res += generate_capture_king(current_state, y, x, max_player)
        if not res:
            for y in range(8):
                for x in range(8):
                    if current_state[y][x] == 'r':
                        res += generate_move_simple(current_state, y, x, max_player)
                    elif current_state[y][x] == 'R':
                        res += generate_move_king(current_state, y, x, max_player)
    else:
        for y in range(8):
            for x in range(8):
                if current_state[y][x] == 'b':
                    res += generate_capture_simple(current_state, y, x, max_player)
                elif current_state[y][x] == 'B':
                    res += generate_capture_king(current_state, y, x, max_player)
        if not res:
            for y in range(8):
                for x in range(8):
                    if current_state[y][x] == 'b':
                        res += generate_move_simple(current_state, y, x, max_player)
                    elif current_state[y][x] == 'B':
                        res += generate_move_king(current_state, y, x, max_player)
    return res


# In[44]:


def terminal(current_state, max_player):
    black = False
    red = False
    for y in range(8):
        for x in range(8): 
            if (not black) and ((current_state[y][x] == 'b') or (current_state[y][x] == 'B')):
                black = True
            elif (not red) and ((current_state[y][x] == 'r') or (current_state[y][x] == 'R')):
                red = True
    if not red:
        return -1
    elif not black:
        return 1
    if max_player:
        for y in range(8):
            for x in range(8):
                if current_state[y][x] == 'r':
                    if (generate_move_simple(current_state, y, x, max_player)) or (generate_capture_simple(current_state, y, x, max_player)):
                        return 0
                elif current_state[y][x] == 'R':
                    if (generate_move_king(current_state, y, x, max_player)) or (generate_capture_king(current_state, y, x, max_player)):
                        return 0
        return -1
    else:
        for y in range(8):
            for x in range(8):
                if current_state[y][x] == 'b':
                    if (generate_move_simple(current_state, y, x, max_player)) or (generate_capture_simple(current_state, y, x, max_player)):
                        return 0
                elif current_state[y][x] == 'B':
                    if (generate_move_king(current_state, y, x, max_player)) or (generate_capture_king(current_state, y, x, max_player)):
                        return 0
        return 1


# In[48]:


def alpha_beta(current_state, alpha, beta, player_max, depth, explored):
    best_state = current_state
    if depth == 12:
        return utility_f(current_state), best_state
    if terminal(current_state, player_max):
        if terminal(current_state, player_max) == 1:
            return float('inf'), best_state
        else:
            return float('-inf'), best_state
    border = float('-inf') if player_max else float('inf')
    for new_state in actions(current_state, player_max):
        if hash_f(new_state) in explored:#save just utility function
            nxt_border = explored[hash_f(new_state)]
            if nxt_border == float('inf'):
                continue
        else:
            explored[hash_f(new_state)] = float('inf')
            nxt_border, nxt_state = alpha_beta(new_state, alpha, beta, (False if player_max else True), depth+1, explored)
            explored[hash_f(new_state)] = nxt_border
        if player_max:
            if border < nxt_border:
                border, best_state = nxt_border, new_state
            if border >= beta:
                return border, best_state
            alpha = max(alpha, border)
        else:
            if border > nxt_border:
                border, best_state = nxt_border, new_state
            if border <= alpha:
                return border, best_state
            beta = min(beta, border)
    return border, best_state


# In[49]:


def hash_f(current_state):# '.' = 0, 'r' = 1, 'R' = 2, 'b' = 3, 'B' = 4
    even = True
    i = 31
    res = 0
    for y in range(8):
        if even:
            for x in range(1, 8, 2):
                ch = current_state[y][x]
                n = 0
                if ch == 'r': n = 1
                elif ch == 'R': n = 2
                elif ch == 'b': n = 3
                elif ch == 'B': n = 4
                res += n * 10**i
                i -= 1
                even = False
        else:
            for x in range(0,8,2):
                ch = current_state[y][x]
                n = 0
                if ch == 'r': n = 1
                elif ch == 'R': n = 2
                elif ch == 'b': n = 3
                elif ch == 'B': n = 4
                res += n * 10**i
                i -= 1
                even = True
    return res


# In[ ]:
_, best_state = alpha_beta(transform_input(input_file), float('-inf'), float('inf'), True, 0, {})
f = open(output_file, 'w')
for y in range(8):
    f.write(''.join(map(str, best_state[y])))
    f.write('\n')
f.close()

