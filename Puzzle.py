import sys
from Node import *
import heapq

def ft_atoi(string):
    res = 0
    for i in xrange(len(string)):
        res = res * 10 + (ord(string[i]) - ord('0'))
    return res


class Ft_colors:
    PURPLE = '\x1b[94m'
    OKBLUE = '\x1b[96m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    UNDERLINE = '\x1b[4m'


class Puzzle:
    def __init__(self, size):
        self.n = size
        self.open = []
        self.closed = []
        self.tmp_closed = {}
        self.tmp_opened = {}

    def ft_find(self, child, puzzle_lst):
        index = 0
        for x in puzzle_lst:
            if x.lst_hash == child.lst_hash:
                return x, index
            index += 1
        return 0, index

    def ft_find_parent(self, id, puzzle_lst):
        for x in puzzle_lst:
            if x.id == id:
                return x
        return 0

    def ft_path(self, puzzle_lst):
        graph = []
        cur = puzzle_lst[0]
        while cur.id_parent > -1:
            graph.append(cur)
            cur = self.ft_find_parent(cur.id_parent, puzzle_lst)
        graph.append(cur)
        return graph

    def ft_print(self, graph):
        bcolors = Ft_colors()
        w = len(str(self.n * self.n))
        i, length_graph = 0, len(graph)
        while i < length_graph:
            if i != 0:
                print ""
                print("  | ")
                print("  | ")
                print(" \\\'/ \n")
            for key, x in enumerate(graph[i].lst):
                if x == 0:
                    print bcolors.FAIL + "0".rjust(w) + bcolors.ENDC,
                else:
                    print str(x).rjust(w),
                if (key + 1) % self.n == 0:
                    print ""
            i += 1

    # display different informations of the search   
    def ft_display(self, nb_open, nb_move, args, goal, start, time_exec):
        bcolors = Ft_colors()
        print bcolors.OKBLUE + "Greedy search:" + bcolors.ENDC, bcolors.OKGREEN + "YES" + bcolors.ENDC if args.g else bcolors.FAIL + "NO" + bcolors.ENDC
        print bcolors.OKBLUE + "Uniform cost search:" + bcolors.ENDC, bcolors.OKGREEN + "YES" + bcolors.ENDC if args.u else bcolors.FAIL + "NO" + bcolors.ENDC
        print bcolors.OKBLUE + "Solvable:" + bcolors.ENDC, bcolors.OKGREEN + "YES" + bcolors.ENDC
        print bcolors.WARNING + "Heuristic function:" + bcolors.ENDC, bcolors.UNDERLINE + args.f + bcolors.ENDC
        print bcolors.WARNING + "Puzzle size:" + bcolors.ENDC, bcolors.UNDERLINE + str(self.n) + bcolors.ENDC
        print bcolors.WARNING + "Goal type:" + bcolors.ENDC, bcolors.UNDERLINE + str(args.s) + bcolors.ENDC
        print bcolors.WARNING + "Initial state:" + bcolors.ENDC, bcolors.UNDERLINE + str(start) + bcolors.ENDC
        print bcolors.WARNING + "Goal state:" + bcolors.ENDC, bcolors.UNDERLINE + str(goal) + bcolors.ENDC
        if args.u:
            algo = "Uniform cost search"
        elif args.g:
            algo = "Greedy search"
        elif args.ida:
            algo = "IDA*"
        else:
            algo = 'A*'

        print bcolors.PURPLE + "Search algorithm:" + bcolors.ENDC, algo
        print bcolors.PURPLE + "Search duration:" + bcolors.ENDC, str(time_exec) + " seconds"
        print bcolors.PURPLE + "Evaluated nodes:" + bcolors.ENDC, str(nb_open)
        print bcolors.PURPLE + "Complexity in time:" + bcolors.ENDC,str(time_exec / nb_open) + " second(s) per node"
        print bcolors.PURPLE + "Number of moves:" + bcolors.ENDC, str(nb_move)
        print bcolors.PURPLE + "Space complexity:" + bcolors.ENDC, str(Node.count)
        print bcolors.FAIL + "Graph of solution:" + bcolors.ENDC
        if args.ida:
            # determine the graph from the inverse of open list
            graph = self.ft_path(self.open)[::-1]
        else:
            # determine the graph from the inverse of closed list
            graph = self.ft_path(self.closed)[::-1]
        if args.d:
            self.ft_print(graph)
        else:
            for i in graph:
                print i.lst

    # A* Algorithm
    def ft_astar(self, size, start, goal, heuristic, cost):
        nb_open = 0
        start = Node(start, -1, 0, 0, 0, 0)
        heapq.heappush(self.open, start)
        nb_open += 1
        self.tmp_opened[start.lst_hash] = start

        nbr_index = {}
        for key, element in enumerate(goal):
            nbr_index[element] = key
        while True:
            cur = heapq.heappop(self.open)
            del self.tmp_opened[cur.lst_hash]
            if cur.lst == goal:
                self.closed.insert(0, cur)
                return nb_open, cur.level

            self.closed.insert(0, cur)
            self.tmp_closed[cur.lst_hash] = cur
            children = cur.generate_child(size, nbr_index, heuristic, cost, goal)
            for child in children:
                if child.lst_hash in self.tmp_closed:
                    continue
                if child.lst_hash not in self.tmp_opened:
                    self.tmp_opened[child.lst_hash] = child
                    heapq.heappush(self.open, child)
                    nb_open += 1
                else:
                    actual_node, index = self.ft_find(child, self.open)
                    if actual_node.g > child.g:
                        self.tmp_opened[child.lst_hash] = child
                        del self.open[index]
                        heapq.heappush(self.open, child)
        return 0, 0

    # IDA* Algorithm
    def ft_idastar(self, start, goal, size, heuristic):
        nb_open = 0
        threshold = start.f
        dic = {}
        nbr_index = {}
        for key, element in enumerate(goal):
            nbr_index[element] = key
        self.open.insert(0, start)
        nb_open += 1
        self.tmp_opened[start.lst_hash] = start
        while True:
            temp, nb_open = self.ft_search(threshold, goal, size, dic, nbr_index, nb_open, heuristic)
            if temp == 0:
                return nb_open, self.open[0].level
            threshold = temp
        return 0, 0

    # Recursive function ft_search for IDA* Algorithm 
    def ft_search(self, threshold, goal, size, dic, nbr_index, nb_open, heuristic):
        current = self.open[0]
        f = current.f
        if f > threshold:
            return f, nb_open
        if current.lst_hash == hash(tuple(goal)):
            return 0, nb_open
        min = sys.maxint

        if current.id not in dic:
            dic[current.id] = current.generate_child(size, nbr_index, heuristic, 2, goal)

        for child in dic[current.id]:
            if child.lst_hash not in self.tmp_opened:
                self.open.insert(0, child)
                nb_open += 1
                self.tmp_opened[child.lst_hash] = child
                temp, nb_open = self.ft_search(threshold, goal, size, dic, nbr_index, nb_open, heuristic)
                if temp == 0:
                    return 0, nb_open
                if temp < min:
                    min = temp
                del self.tmp_opened[self.open[0].lst_hash]
                del self.open[0]
        return min, nb_open

    # Goal in snail
    def ft_spiralPrint(self, n):
        k, l = 0, 0
        m, h = n, n
        size, d = 1, n ** 2
        tab = [[0 for i in range(n)] for j in range(n)]

        while (k < m and l < n):
            for i in range(l, n):
                tab[k][i] = size % d
                size += 1

            k += 1
            for i in range(k, m):
                tab[i][n - 1] = size % d
                size += 1

            n -= 1
            if (k < m):

                for i in range(n - 1, (l - 1), -1):
                    tab[m - 1][i] = size % d
                    size += 1
                m -= 1

            if (l < n):
                for i in range(m - 1, k - 1, -1):
                    tab[i][l] = size % d
                    size += 1
                l += 1
        goal = [tab[i][j] for i in range(h) for j in range(h)]
        return goal

    # Goal: zero_last
    def ft_zero_last(self, size):
        goal = [i + 1 for i in range(0, (size ** 2) - 1)]
        goal.append(0)
        return goal

    # Goal : zero_first
    def ft_zero_first(self, size):
        goal = [i for i in range(0, size ** 2)]
        return goal

    # # generate a puzzle from a str 
    # def generate_Puzzle(self, lst_str, size):
    #     i = 0
    #     lst = []
    #     size = size ** 2
    #     while i < size:
    #         lst.append(ft_atoi(lst_str[i]))
    #         i += 1
    #     return lst

    # determine if the puzzle is solvent or not before applying algorithm
    def ft_solvable(self, start, goal, size):
        xstart, ystart = start.index(0) % size, start.index(0) / size
        # array goal
        xgoal, ygoal = goal.index(0) % size, goal.index(0) / size
        # moves
        dep = abs(ystart - ygoal) + abs(xstart - xgoal)
        # calcul nb inverstion
        nb = 0
        i = 0
        size = size ** 2
        while i < size:
            nb = nb + len(list(set(start[i:]) - set(goal[goal.index(start[i]):])))
            i += 1

        sol = False
        if (nb % 2 == 0 and dep % 2 == 0) or (nb % 2 != 0 and dep % 2 != 0):
            sol = True
        return sol