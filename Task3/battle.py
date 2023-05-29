# %%
import copy
import sys
_, input_file, output_file = sys.argv

# %%
class tile:
    # def __init__(self, processed, is_ship, horizontal_line, vertical_line):
    def __init__(self, processed, is_ship, x, y):
        self.processed = processed
        self.is_ship = is_ship
        # self.horizontal_line = horizontal_line
        # self.vertical_line = vertical_line
        self.x = x
        self.y = y
    
    def __repr__(self):
        if self.processed:
            if self.is_ship:
                return "S"
            else:
                return "W"
        else:
            return "0"

    
class line:
    def calc_capacity(self, default_capacity = -1): #from 0 to 4
        if default_capacity >= 0:
            return default_capacity
        max_c = 0
        current_c = 0
        sum_capacity = self.sum_constraint
        for t in self.list_of_tiles:
            if not t.processed:
                current_c += 1
            else:
                max_c = current_c if current_c > max_c else max_c
                current_c = 0
                if t.is_ship:
                    sum_capacity -= 1
        max_c = current_c if current_c > max_c else max_c
        max_c = sum_capacity if max_c > sum_capacity else max_c
        return max_c if max_c <= 4 else 4
    
    def __init__(self, list_of_tiles, sum_constraint, prv_line, nxt_line, capacity = -1):
        self.list_of_tiles = list_of_tiles
        self.sum_constraint = sum_constraint
        #if change capacity, change place in capacity list as well
        self.capacity = self.calc_capacity(capacity)
        self.prv_line = prv_line
        self.nxt_line = nxt_line
    #the biggest ship that may be placed here 
    #if no ship fits with specified capacity
    
    def __repr__(self):
        res = "("
        for i in self.list_of_tiles:
            res += f"{str(i)}, "
        res += f"[{str(self.sum_constraint)}])"
        return res
    
    def reduce_places_line(self):
        self.capacity = self.calc_capacity()
        if self.capacity == 0:
            indx = 0
            ship = False
            for t in self.list_of_tiles:
                if (not t.processed) or (not t.is_ship):
                    t.processed = True
                    t.is_ship = False
                    if ship:
                        if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx].processed):
                            self.nxt_line.list_of_tiles[indx].processed = True
                            self.nxt_line.list_of_tiles[indx].is_ship = False
                        if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx].processed):
                            self.prv_line.list_of_tiles[indx].processed = True
                            self.prv_line.list_of_tiles[indx].is_ship = False
                        ship = False
                elif t.is_ship:
                    if not ship:
                        if indx > 0:
                            if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx-1].processed):
                                self.nxt_line.list_of_tiles[indx-1].processed = True
                                self.nxt_line.list_of_tiles[indx-1].is_ship = False
                            if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx-1].processed):
                                self.prv_line.list_of_tiles[indx-1].processed = True
                                self.prv_line.list_of_tiles[indx-1].is_ship = False
                        ship = True
                    if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx].processed):
                        self.nxt_line.list_of_tiles[indx].processed = True
                        self.nxt_line.list_of_tiles[indx].is_ship = False
                    if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx].processed):
                        self.prv_line.list_of_tiles[indx].processed = True
                        self.prv_line.list_of_tiles[indx].is_ship = False
                indx += 1
        else:
            ship = False
            indx = 0
            for t in self.list_of_tiles:
                if ship:
                    if (not t.processed) or (not t.is_ship):
                        ship = False
                        self.list_of_tiles[indx].processed = True
                        self.list_of_tiles[indx].is_ship = False
                    if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx].processed):
                        self.nxt_line.list_of_tiles[indx].processed = True
                        self.nxt_line.list_of_tiles[indx].is_ship = False
                    if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx].processed):
                        self.prv_line.list_of_tiles[indx].processed = True
                        self.prv_line.list_of_tiles[indx].is_ship = False
                    
                else:
                    #add w for current indx
                    if t.processed and t.is_ship:
                        if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx].processed):
                            self.nxt_line.list_of_tiles[indx].processed = True
                            self.nxt_line.list_of_tiles[indx].is_ship = False
                        if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx].processed):
                            self.prv_line.list_of_tiles[indx].processed = True
                            self.prv_line.list_of_tiles[indx].is_ship = False
                        ship = True
                        if (indx > 0):
                            self.list_of_tiles[indx-1].processed = True
                            self.list_of_tiles[indx-1].is_ship = False
                            if bool(self.nxt_line) and (not self.nxt_line.list_of_tiles[indx-1].processed):
                                self.nxt_line.list_of_tiles[indx-1].processed = True
                                self.nxt_line.list_of_tiles[indx-1].is_ship = False
                            if bool(self.prv_line) and (not self.prv_line.list_of_tiles[indx-1].processed):
                                self.prv_line.list_of_tiles[indx-1].processed = True
                                self.prv_line.list_of_tiles[indx-1].is_ship = False
                indx += 1
            
    def check_sum(self):
        self.capacity = self.calc_capacity()
        min_ships = 0
        max_ships = 0
        for t in self.list_of_tiles:
            if not t.processed: 
                max_ships += 1
            elif t.is_ship:
                min_ships += 1
                max_ships += 1
        if (max_ships < self.sum_constraint) or (min_ships > self.sum_constraint):
            return False
        return True

    #shows places to place the ship
    def places(self, size):
        res = []
        empty_counter = 0
        length = len(self.list_of_tiles)
        for i in range(length):
            if not self.list_of_tiles[i].processed:
                empty_counter += 1
            else:
                if bool(empty_counter):
                    res.append((i-empty_counter, i-1))
                    empty_counter = 0
        if bool(empty_counter):
            res.append((length-empty_counter, length-1))
        res0 = []
        for x,y in res:
            for k in range(x, y-size+2):
                res0.append(k)
        return res0
                
    def place_ship(self, x, size):
        for i in range(x, x+size):
            self.list_of_tiles[i].processed = True
            self.list_of_tiles[i].is_ship = True

# %%
def reduce_ships(ships, vertical_field):
    ship_counter = 0
    length = len(vertical_field)
    checked = [[False for _ in range(length)] for _ in range(length)]
    y = 0
    x = 0
    for l in vertical_field:
        while x < length:
            if (not checked[y][x]) and l[x].processed and l[x].is_ship:
                ship_counter += 1
                checked[y][x] = True
                if (x+1 < length) and l[x+1].processed and l[x+1].is_ship:
                    x+=1
                    while(x < length) and l[x].processed and l[x].is_ship:
                        checked[y][x] = True
                        ship_counter += 1
                        x+=1
                    ships[ship_counter-1] -= 1
                    ship_counter = 0
                else:
                    ny = y + 1
                    while(ny < length) and vertical_field[ny][x].processed and vertical_field[ny][x].is_ship:
                        checked[ny][x] = True
                        ship_counter += 1
                        ny+=1
                    ships[ship_counter-1] -= 1
                    ship_counter = 0
            x+=1
        x = 0
        y+=1


# %%
def translate_field(line, y):
#     set_all = {'S', 'W', 'L', 'R', 'T', 'B', 'M'}
    res_line = []
    x = 0
    for ch in [*line]:
        if ch == '0': 
            res_line.append(tile(False, True, x, y)) 
                        # res_line.append(tile(False, True, 0, 0)) 

        elif ch == 'W':
            res_line.append(tile(True, False, x, y)) 
                        # res_line.append(tile(True, False, 0, 0)) 

        else:
            res_line.append(tile(True, True, x, y))
                        # res_line.append(tile(True, True, 0, 0))
        x += 1
    return res_line

# %%
def translate_input(file_name):#check_queue [[first priority], [second priority],...]
    with open(file_name) as f:
        ln = f.readline()
        sum_row = [int(i) for i in [*ln[:-1:]]]
        ln = f.readline()
        sum_column = [int(i) for i in [*ln[:-1:]]]
        ln = f.readline()
        ships = ([int(i) for i in [*ln[:-1:]]] + [0]) if (len(ln) < 5) else [int(i) for i in [*ln[:-1:]]]
        ln = f.readline()
        field = []
        y = 0
        while ln[-1] == '\n':
            field.append(translate_field(ln[:-1:], y))
            ln = f.readline()
            y+=1
        field.append(translate_field(ln, y))
    length = len(field)
    horizontal_list = []
    vertical_list = []
    vertical_field = [[] for _ in range(length)]
    y = 0
    for l in field:
        new_line = line(l, sum_row[y], 0, 0)
        horizontal_list.append(new_line)
        for x in range(length):
            vertical_field[x].append(l[x])
        y += 1
    y = 0
    for l in vertical_field:
        new_line = line(l, sum_column[y], 0, 0)
        vertical_list.append(new_line)
        y+=1

    reduce_ships(ships, vertical_field)
    
    prev = 0
    current = 0
    next = 0
    for h in horizontal_list:
        # for t in h.list_of_tiles:
        #     t.horizontal_line = h
        prev = current
        current = next
        next = h
        if bool(current):
            current.prv_line = prev
            current.nxt_line = next
    next.prv_line = current
    next.nxt_line = 0

    prev = 0
    current = 0
    next = 0
    for v in vertical_list:
        # for t in v.list_of_tiles:
        #     t.vertical_line = v
        prev = current
        current = next
        next = v
        if bool(current):
            current.prv_line = prev
            current.nxt_line = next
    next.prv_line = current
    next.nxt_line = 0

        

    return ships, horizontal_list, vertical_list

# %%
def choose_ship(ships):
    for i in range(3, -1, -1):
        if ships[i] > 0:
            return i
    return -1

# %%
def copy_lists(ships_old, horizontal_list_old, vertical_list_old):
    # horizontal_list = copy.deepcopy(horizontal_list_old)
    ships = copy.copy(ships_old)
    horizontal_list = []
    capacity_list = [[] for _ in range(5)]
    vertical_list = []
    vertical_field = [[] for _ in range(len(horizontal_list_old))]
    current = 0
    next = 0
    for h in horizontal_list_old:
        current = next
        next = line(copy.deepcopy(h.list_of_tiles), h.sum_constraint, current, 0)
        if bool(current):
            current.nxt_line = next
            horizontal_list.append(current)
            capacity_list[current.capacity].append(current)
            for x in range(len(vertical_field)):
                vertical_field[x].append(current.list_of_tiles[x])
    horizontal_list.append(next)
    capacity_list[next.capacity].append(next)
    for x in range(len(vertical_field)):
        vertical_field[x].append(next.list_of_tiles[x])

    y = 0
    current = 0
    next = 0
    for l in vertical_field:
        current = next
        next = line(l, vertical_list_old[y].sum_constraint, current, 0)
        if bool(current):
            current.nxt_line = next
            vertical_list.append(current)
            capacity_list[current.capacity].append(current)
        y+=1
    vertical_list.append(next)
    capacity_list[next.capacity].append(next)
    return ships, capacity_list, horizontal_list, vertical_list
    # return horizontal_list

# %%
#TO DO
def check_constraints(horizontal_list, vertical_list):
        list_prev = []
        next_indexes = []
        for h in horizontal_list:
                h.reduce_places_line()
                ship = False
                i = 0
                for t in h.list_of_tiles:
                        if t.processed and t.is_ship:
                                if not ship:
                                        if not bool(i):
                                                list_prev[i-1]
                        i+=1
        for v in vertical_list:
                h.reduce_places_line()
        #plus check corners

# %%
#returns new capacity list
def apply_constraints(ships, horizontal_list, vertical_list):
    n_capacity_list = [[] for _ in range(5)]
    for h in horizontal_list:
        h.reduce_places_line()
    for v in vertical_list:
        v.reduce_places_line()
    
    max_capacity = 0
    for h in horizontal_list:
        if not h.check_sum():
            return []
        n_capacity_list[h.capacity].append(h)
        if h.capacity > max_capacity:
            max_capacity = h.capacity
    for v in vertical_list:
        if not v.check_sum():
            return []
        n_capacity_list[v.capacity].append(v)
        if v.capacity > max_capacity:
            max_capacity = v.capacity
    if choose_ship(ships) > max_capacity:
        return []
    return n_capacity_list

# %%
def f_s(ships, capacity_list, horizontal_list, vertical_list):
    #add list of wrong ships
    #list of previous add to list only if one of other variants on this field succedes
    ship_size = choose_ship(ships)+1
    if ship_size == 0:
        return horizontal_list
    else:
        for i in range(4, ship_size-1, -1):
            while bool(capacity_list[i]):
                l = capacity_list[i].pop()
                x1 = l.list_of_tiles[0].x
                y1 = l.list_of_tiles[0].y
                x2 = l.list_of_tiles[1].x
                # y2 = l.list_of_tiles[1].y
                if x1 == x2:
                    horizontal = False
                    y = x1
                else:
                    horizontal = True
                    y = y1
                for x in l.places(ship_size):
                    n_ships, n_capacity_list, n_horizontal_list, n_vertical_list = copy_lists(ships, horizontal_list, vertical_list)
                    n_ships[ship_size-1] -= 1
                    if horizontal:
                        n_horizontal_list[y].place_ship(x, ship_size)
                    else:
                        n_vertical_list[y].place_ship(x, ship_size)
                    n_capacity_list = apply_constraints(n_ships, n_horizontal_list, n_vertical_list)#if empty than dead end here
                    if bool(n_capacity_list):
                        res = f_s(n_ships, n_capacity_list, n_horizontal_list, n_vertical_list)
                        if bool(res):
                            return res
        return []
            

# %%


# %%


# %%
def output(horizontal_list):
    ls = [l.list_of_tiles for l in horizontal_list]
    length = len(ls)
    res = [ [ 'W' for _ in range(length)] for _ in range(length)]
    check = [ [ False for _ in range(length)] for _ in range(length)]
    for y in range(length):
        for x in range(length):
            if not check[y][x]:
                if ls[y][x].is_ship:
                    if (x+1 < length) and (ls[y][x+1].is_ship):
                        res[y][x] = 'L'
                        check[y][x] = True
                        if (x+2 < length) and (ls[y][x+2].is_ship):
                            res[y][x+1] = 'M'
                            check[y][x+1] = True
                            if (x+3 < length) and (ls[y][x+3].is_ship):
                                res[y][x+2] = 'M'
                                res[y][x+3] = 'R'
                                check[y][x+2] = True
                                check[y][x+3] = True
                            else:
                                res[y][x+2] = 'R'
                                check[y][x+2] = True
                        else:
                            res[y][x+1] = 'R'
                            check[y][x+1] = True
                    elif (y+1 < length) and (ls[y+1][x].is_ship):
                        res[y][x] = 'T'
                        check[y][x] = True
                        if (y+2 < length) and (ls[y+2][x].is_ship):
                            res[y+1][x] = 'M'
                            check[y+1][x] = True
                            if (y+3 < length) and (ls[y+3][x].is_ship):
                                res[y+2][x] = 'M'
                                res[y+3][x] = 'B'
                                check[y+2][x] = True
                                check[y+3][x] = True
                            else:
                                res[y+2][x] = 'B'
                                check[y+2][x] = True
                        else:
                            res[y+1][x] = 'B'
                            check[y+1][x] = True
                    else:
                        res[y][x] = 'S'
                        check[y][x] = True
                else:
                    check[y][x] = True
    return res

# %%
def run_s(input_name, output_name):
    ships, horizontal_list, vertical_list = translate_input(input_name)
    capacity_list = apply_constraints(ships, horizontal_list, vertical_list)
    res = output(f_s(ships, capacity_list, horizontal_list, vertical_list))
    f = open(output_name, 'w')
    for l in res:
        f.write(''.join(map(str, l)))
        f.write('\n')
    f.close()

# %%
# def change_tile(t, horizontal_list, vertical_list):
#     horizontal_list[t.y].calc_capacity()
#     vertical_list[t.x].calc_capacity()

# %%
# ships, horizontal_list, vertical_list = translate_input("test.txt")
# apply_constraints(ships, horizontal_list, vertical_list)
# vertical_list[1].place_ship(2, 3)
# ships[2] -= 1
# apply_constraints(ships, horizontal_list, vertical_list)
# horizontal_list

# %%
# horizontal_list[2].places(3)

# %%
run_s(input_file, output_file)


# %%
# horizontal_list, [v.sum_constraint for v in vertical_list]

# %%


# %%
# s, c, h, v = copy_lists(ships ,horizontal_list, vertical_list)
# v = copy.deepcopy(vertical_list)

# %%
# t = horizontal_list[2].list_of_tiles[1]
# t.processed = True

# %%
# apply_constraints(ships, horizontal_list, vertical_list)
# apply_constraints(s, h, v)

# %%
# ships, capacity_list, horizontal_list, vertical_list

# %%
# s, c, h, v

# %%
# horizontal_list, [v.sum_constraint for v in vertical_list]

# %%
# apply_constraints(ships, horizontal_list, vertical_list)

# %%
# for i in range(1, 1+3):
#     print(i)

# %%



