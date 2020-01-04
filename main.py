#!/usr/bin/env python

from os import system, name
import re
import time
import argparse
from Node import *
from Puzzle import *


# save history of statistics in the file 'N-Puzzle_statistics' 
def ft_save_history(start, goal, size, nb_open, end_time, args):
    with open('N-Puzzle_statistics', 'a') as f:
        if args.g :
            format_search = "Greedy search"
        elif args.u :
            format_search = "Uniform-cost search"
        elif args.ida :
            format_search = "IDA-star search"
        else :# !args.g and !args.h and !args.ida :
            format_search = "A-star search"
        f.write(str(size) + ';' + str(goal) + ';' + str(start) + ';' + str(Node.count) + ';' + str(nb_open) + ';' + str(end_time) + ";" + str(format_search)+'\n')

# display history of statistics saved in the file 'N-Puzzle_statistics'
def ft_display_history():
    try:
        print "\x1b[91m" + "\nHistory" + "\x1b[0m"
        with open('N-Puzzle_statistics') as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        for i in range(0, 42):
            print '-',
        print ""

        for k, elem in enumerate(content):
            line = content[k].split(';')
            print(line[len(line) - 1])
            size = ft_atoi(line[0])
            goal = list(filter(None, re.split(r',| |\[|\]', line[1])))
            start = list(filter(None, re.split(r',| |\[|\]', line[2])))
            level = line[4]
            end_time = round(float(line[5]), 4)

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
    # generate puzzle
    p = Puzzle(0)
    start = p.generate_Puzzle(start, size)
    # goals
    if args.s == 'zero_first':
        goal = p.ft_zero_first(size)
    elif args.s == 'zero_last':
        goal = p.ft_zero_last(size)
    else:
        goal = p.ft_spiralPrint(size)
    sol = p.ft_solvable(start, goal, size)
    if sol :
        cur = Puzzle(size)
        start_time = time.time()
        print "Wait please..."
        # apply the right algorithm according to flags
        if args.ida:
            root = Node(start, -1, 0, 0, 0, 0)
            nb_open, level = cur.ft_idastar(root, goal, size, args.f)
        else:
            if args.u:
                if args.g:
                    print "NB: this will only do the Uniform-cost search" 
                nb_open, level = cur.ft_astar(size, start, goal, args.f, -1) #(uniform)
            elif args.g:
                nb_open, level = cur.ft_astar(size, start, goal, args.f, 0) #(gradi)
            else:
                nb_open, level = cur.ft_astar(size, start, goal, args.f, 2) 
        end_time = time.time() - start_time
   #     ft_clear()
        ft_save_history(start, goal, size, level, end_time, args)
        cur.ft_display(nb_open, level, args, goal, start, end_time)
    else:
        print "\x1b[91m" + "This puzzle is unsolvable" + "\x1b[0m"
    if args.v:
            ft_display_history()