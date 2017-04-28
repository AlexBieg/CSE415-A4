'''
Cole Chamberlin 1434297 jessec18
CSE 415, University of Washington
Steven Tanimoto
HW4 Problem Formulation

Diseases.py

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
#<METADATA>
PROBLEM_NAME = "Spread of Diseases"
PROBLEM_AUTHORS = ['Alex Bieg', 'Cole Chamberlin']
PROBLEM_CREATION_DATE = "21-APR-2017"
#</METADATA>

#<COMMON_CODE>
import math

def can_move(s, tile):
    '''Tests whether it's legal to move a disk in state s
         from the From peg to the To peg.'''
    try:
        t0 = s.config.index(0) # empty tile    
        t1 = s.config.index(tile) # tile to move
        # tiles are horizontally adjacent
        if (abs(t0-t1)==1) and (t0//s.size==t1//s.size): return True 
        # tiles are vertically adjacent
        if (t0%s.size==t1%s.size) and (abs(t0//s.size-t1//s.size)==1) : return True 
        return False # move can't be made
    except (Exception) as e:
        print(e)

def move(s, tile):
    '''Assuming it's legal to make the move, this computes
         the new state resulting from moving the topmost disk
         from the From peg to the To peg.'''
    newS = s.__copy__() # start with a deep copy.
    t0 = s.config.index(0) # empty tile
    t1 = s.config.index(tile) # tile to move
    # swap two tiles
    newS.config[t0] = tile
    newS.config[t1] = 0
    newS.cost = s.cost + 1
    return newS # return new state

def goal_test(s):
    '''If the tiles are in order, then s is a goal state.'''
    return s.config == sorted(list(s.config))

def goal_message(s):
    return "The puzzle is solved!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# returns the difference in x and y coordinates between t and i in state s
coords = lambda s, t, i: (abs(t//s-i//s), abs(t%s-i%s))

def compute_distance(state, distance_metric):
    c = state.config
    val = 0
    for i in range(len(c)):
        x, y = coords(state.size, c.index(i), i) 
        val += distance_metric(x, y)
    return val

def h_euclidean(state):
    return compute_distance(state, lambda x, y: math.sqrt(x**2+y**2))

def h_manhattan(state):
    return compute_distance(state, lambda x, y: x + y)

def h_hamming(state):
    return compute_distance(state, lambda x, y: 0 if x == y else 1)

def h_custom(state):
    # implements linear conflict heuristic, where if two tiles are in the
    # correct row/column, but the wrong order relative to each other, one must
    # move out of line for the other to move past it. This adds 2 to the
    # heuristic for every instance of this conflict.
    h = compute_distance(state, lambda x, y: x + y)
    row_coords = [[-1 for x in range(state.size)] for y in range(state.size)]
    col_coords = [[-1 for x in range(state.size)] for y in range(state.size)]
    for i in range(len(state.config)):
        x, y = coords(state.size, state.config.index(i), 0) 
        m, n = coords(state.size, state.config.index(i), i)
        if m == 0:
            row_coords[x][y] = i
        if n == 0:
            col_coords[y][x] = i
    for x in range(state.size):
        for y in range(state.size):
            u = row_coords[x][y]
            v = col_coords[x][y]
            for z in range(y):
                s = row_coords[x][z]
                t = col_coords[x][z]
                if u != -1 and s > u: h += 2
                if v != -1 and t > v: h += 2
    return h
#</COMMON_CODE>

#<COMMON_DATA>
N_tiles = 8

#</COMMON_DATA>


#<STATE>
class State():
    def __init__(self, cities, aid):
        self.cities = cities
        self.aid = aid
        self.heur = heur

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # Produces a brief textual description of a state.
        txt = ''
        for x in range(self.size):
            for y in range(self.size):
                val = self.config[self.size * x + y]
                txt += ' ' + (str(val) if val != 0 else ' ')
            txt += '\n'
        return txt

    def __eq__(self, other):
        if isinstance(other, State):
            return self.config == other.config

    def __lt__(self, other):
        if isinstance(other, State):
            return (self.cost + self.heur) < (other.cost + other.heur)

    def __hash__(self):
        return str(self.config).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        newS = State(list(self.config), self.cost, self.heur)
        return newS

    def getCity(city):
        return cities[city]
#</STATE>

#<CITY>
class City():
    def __init__(self, name, lat, lng, pop, airpts, inf=0.0, susc=0.0,
            recov=0.0, ds=0.0, di=0.0, dr=0.0):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.pop = pop
        self.airpts = airpts
        self.susc = susc
        self.inf = inf
        self.recov = recov
        self.ds = ds
        self.di = di
        self.dr = dr

    def __eq__(self, other):
        if isinstance(other, City):
            return self.name == other.name

    def __hash__(self):
        (self.name + str(self.lat) + str(self.lng)).__hash__()

    def __copy__(self):
        newCity = City(self.name, self.lat, self.lng, self.pop, self.airpts,
                self.infected, self.susc, self.recov)
        return newCity

    def giveAid(amount):
        alpha = 1
        beta = 1
        new_inf = math.exp(-amount*alpha) * self.susc
        new_rec = (1 - math.exp(-amount*beta)) * self.inf
        self.susc -= new_inf
        self.inf += new_inf
        self.inf -= new_rec
        self.rec += new_rec

    def score():
        return self.pop - self.inf
#</CITY>

#<INITIAL_STATE>
INITIAL_STATE = None
def CREATE_INITIAL_STATE():
    with open("cities.tsv", 'r') as cities:
        for i, line in enumerate(cities):
            if i != 0:
                c = line.split('\t')
                name = c[0]

#</INITIAL_STATE>

#<OPERATORS>
def updateCity(s, city, aid):
    newS = s.__copy__()
    city = newS.getCity(city).giveAid(aid)
    return newS

OPERATORS = [Operator("Give aid to city " + s.name,
    # The default value construct is needed
    # here to capture the values of p&q separately
    # in each iteration of the list comp. iteration.
    lambda s,c1=city: s.getCity(c1).needsAid(),
    lambda s,c1=city: updateCity(s, c1, 1)
    for city in cities]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS> (optional)
HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 
        'h_manhattan': h_manhattan, 'h_custom': h_custom}
#</HEURISTICS>
