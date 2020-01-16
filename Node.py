from Heuristic import *


class Node:
    count = 0
    def __init__(self, lst, id_parent, id, g, h, level):
        self.lst = lst
        self.lst_hash = hash(tuple(lst))
        self.id = id
        self.id_parent = id_parent
        self.f = g + h
        self.g = g
        self.level = level

    def __cmp__(self, other):
        return cmp(self.f, other.f)

    # generate child according to cost :
    # cost == -1 => No Heuristic function (Uniform Cost Search)
    # cost == 0 => No Weight consideration (Greedy Search)

    # ida*2

    def generate_child(self, size, nbr_size, heuristic, cost, goal):
        index = self.lst.index(0)
        x, y = index % size, index / size
        children = []
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        for i in val_list:
            child = self.generate_items(self.lst, x, y, i[0], i[1], size)
            if child is not None:
                Node.count += 1
                g, h = self.g + 1, 0
                if cost != -1:
                    function = Heuristic(goal, child, size)
                    h = function.function[heuristic](nbr_size)
                if cost == 0:
                    g = 0
                children.append(Node(child, self.id, Node.count, g, h, self.level + 1))
        return children

    # generate different possible puzzle according to moves

    def generate_items(self, puz, x1, y1, x2, y2, size):
        if x2 >= 0 and x2 < size and y2 >= 0 and y2 < size:
            temp_puz = puz[:]
            temp_puz[x1 + y1 * size] = temp_puz[x2 + y2 * size]
            temp_puz[x2 + y2 * size] = 0
            return temp_puz
        return None
    
    def __str__(self):
        ret = str(self.id)+ " hash[ " 
        ret = ret + str(self.lst_hash)+ "] elem [" 
        for i in self.lst:
            ret = ret + str(i)+ " "
        ret = ret + "] f = "+ str(self.f) 
        return ret