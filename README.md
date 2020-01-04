# usage: main.py [-h] [-d]
#               [-f {hamming,manhattan,conflicts,Euclidean_distance,out_of_row_and_column}]
#               [-g] [-u] [-s {zero_first,zero_last,snail}] [-v] [-ida]
#               input

#N-puzzle help

positional arguments:
  input                 input start

optional arguments:
  -h, --help            show this help message and exit
  -d                    Display graph
  -f {hamming,manhattan,conflicts,Euclidean_distance,out_of_row_and_column}
                        Heuristic function
  -g                    Greedy search
  -u                    Uniform-cost search
  -s {zero_first,zero_last,snail}
                        Solved state : 'zero_first', 'zero_last', 'snail'
  -v                    Display per-puzzle statistics
  -ida                  IdA-Star search or A-Star
