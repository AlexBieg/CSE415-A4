'''
Cole Chamberlin 1434297 jessec18
CSE 415, University of Washington
Steven Tanimoto
HW3 Working with A* Search

AStar.py
Based on ItrDFS.py, Ver 0.3, April 11, 2017.

A* Search of a problem space.
The Problem should be given in a separate Python
file using the "QUIET" file format.
See the TowerOfHanoi.py example file for details.
Examples of Usage:

python3 AStar.py EightPuzzleWithHeuristics h_manhattan
'''

import sys
from queue import PriorityQueue

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    import Diseases as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_state'](s)
    
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[0](s)

# import initial state from file
try:
    init = importlib.import_module(sys.argv[3].split('.')[0]).CREATE_INITIAL_STATE()
    Problem.CREATE_INITIAL_STATE = lambda: Problem.State(init, 0, 0)
except:
    pass

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    #path, name = AStar(initial_state)
    AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return None, None

# A star search algorithm
def AStar(initial_state):
    global COUNT, BACKLINKS
    OPEN = PriorityQueue()
    OPEN.put(initial_state)
    OPEN_D = {}
    OPEN_D[initial_state] = 0
    CLOSED = []
    BACKLINKS[initial_state] = -1
    
    while not OPEN.empty():
        S = OPEN.get()
        while S in CLOSED:
            S = OPEN.get()
        CLOSED.append(S)
        
        # DO NOT CHANGE THIS SECTION: begining 
        if S.date == 6:
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        COUNT += 1
        for op in Problem.OPERATORS:
            if op.precond(S):
                print(op.name)
                new_state = op.state_transf(S)
                if new_state not in CLOSED:
                    if new_state not in OPEN_D: #or \
                            #OPEN_D[new_state] > new_state.cost:
                        OPEN.put(new_state)
                        OPEN_D[new_state] = 0 #new_state.cost
                        BACKLINKS[new_state] = S
                        print(new_state)

# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Soution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = runAStar()

