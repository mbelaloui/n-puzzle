#!/usr/bin/env python

import sys
import re
import time
import argparse
from Node import *
from Puzzle import *
from os import system, name




# Goal in snail
def ft_spiralPrint(n):
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
def ft_zero_last(size):
    goal = [i + 1 for i in range(0, (size ** 2) - 1)]
    goal.append(0)
    return goal

# Goal : zero_first
def ft_zero_first(size):
    goal = [i for i in range(0, size ** 2)]
    return goal

def ft_atoi(string):
    res = 0
    for i in xrange(len(string)):
        res = res * 10 + (ord(string[i]) - ord('0'))
    return res

# generate a puzzle from a str 
def generate_Puzzle(lst_str, size):
    i = 0
    lst = []
    size = size ** 2
    while i < size:
        lst.append(ft_atoi(lst_str[i]))
        i += 1
    return lst

# determine if the puzzle is solvent or not before applying algorithm
def ft_solvable(start, goal, size):
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

    sol = 0
    if (nb % 2 == 0 and dep % 2 == 0) or (nb % 2 != 0 and dep % 2 != 0):
        sol = 1
    return sol

# save history of statistics in the file 'N-Puzzle_statistics' 
def ft_save_history(start, goal, size, nb_open, end_time):
    with open('N-Puzzle_statistics', 'ab') as f:
        f.write(str(size) + ';' + str(goal) + ';' + str(start) + ';' + str(Node.count) + ';' + str(nb_open) + ';' + str(end_time) + '\n')

# display history of statistics saved in the file 'N-Puzzle_statistics'
def ft_display_history():
    try:
        print "\x1b[91m" + "\nList of History" + "\x1b[0m"
        with open('N-Puzzle_statistics') as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        for i in range(0, 30):
            print '-',
        print ""

        for k, elem in enumerate(content):
            line = content[k].split(';')
            size = ft_atoi(line[0])
            goal = list(filter(None, re.split(r',| |\[|\]', line[1])))
            start = list(filter(None, re.split(r',| |\[|\]', line[2])))
            level = line[4]
            end_time = round(float(line[5]), 3)

            bcolors = Ft_colors()
            w = len(str(size * size))
            i, j = 0, 0
            for key, x in enumerate(start):
                print str(x).rjust(w),
                if (key + 1) % size == 0:
                    print '\t\t',
                    index = key - (size - 1)
                    while index < size ** 2:
                        print str(goal[index]).rjust(w),
                        if (index + 1) % size == 0:
                            if j == 0: print bcolors.OKBLUE + "\t\tPuzzle size:" + bcolors.ENDC, bcolors.OKGREEN + str(size) + bcolors.ENDC
                            if j == 1: print bcolors.OKBLUE + "\t\tNumber of moves:" + bcolors.ENDC, bcolors.OKGREEN + str(level) + bcolors.ENDC
                            if j == 2: print bcolors.OKBLUE + "\t\tSearch duration:" + bcolors.ENDC, bcolors.OKGREEN + str(end_time) + bcolors.ENDC
                            j += 1
                            break
                        index += 1
                    if j > 3:
                        print ""
            if size != 3:
                print ""
            for i in range(0, size*2 + 30):
                print '-',
            print ""
    except:
        print 'No History'

# clear the terminal every time we display final results 
def ft_clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Main Function
if __name__ == "__main__":

    # Parser
    parser = argparse.ArgumentParser(description='N-puzzle help')
    parser.add_argument("-d", default=False, action='store_true', help="Display graph")
    parser.add_argument("-f", choices=['hamming', 'manhattan', 'conflicts', 'Euclidean_distance',
                                       'out_of_row_and_column'], default='manhattan', help="Heuristic function")
    parser.add_argument("-g", default=False, action='store_true', help="Greedy search")
    parser.add_argument("-u", default=False, action='store_true', help="Uniform-cost search")
    parser.add_argument("-s", choices=['zero_first', 'zero_last', 'snail'], default='snail', help="Solved state : 'zero_first', 'zero_last', 'snail'")
    parser.add_argument("-v", default=False, action='store_true', help="Display per-puzzle statistics")
    parser.add_argument("-ida", default=False, action='store_true', help="IdA-Star search or A-Star")
    parser.add_argument("input", help="input start")

    parser.parse_args()
    args = parser.parse_args()
      
    # start list
    start = list(filter(None, re.split(r'# This puzzle is solvable|# This puzzle is unsolvable|\n|,| |', args.input)))
    
    # size
    size = len(start) ** 0.5
    if int(size) != size:
        size = ft_atoi(start[0])
        start = start[1:]
        if size ** 2 != len(start):
            print("ERROR : Puzzle size")
            exit()
   # size = int(size)
    # generate puzzle
    start = generate_Puzzle(start, size)
    # goals
    if args.s == 'zero_first':
        goal = ft_zero_first(size)
    elif args.s == 'zero_last':
        goal = ft_zero_last(size)
    else:
        goal = ft_spiralPrint(size)
    sol = ft_solvable(start, goal, size)
    if sol == 1:
        cur = Puzzle(size)
        start_time = time.time()
        print "Wait please..."
        # apply the right algorithm according to flags
        if args.ida:
            root = Node(start, -1, 0, 0, 0, 0)
            nb_open, level = cur.ft_idastar(root, goal, size, args.f)
        else:
            if args.u:
                nb_open, level = cur.ft_astar(size, start, goal, args.f, -1) (uniform)
            elif args.g:
                nb_open, level = cur.ft_astar(size, start, goal, args.f, 0) (gradi)
            else:
                nb_open, level = cur.ft_astar(size, start, goal, args.f, 2) 
        end_time = time.time() - start_time
        ft_clear()
        ft_save_history(start, goal, size, level, end_time)
        cur.ft_display(nb_open, level, args, goal, start, end_time)
        if args.v:
            ft_display_history()
    else:
        print "\x1b[91m" + "This puzzle is unsolvable" + "\x1b[0m"