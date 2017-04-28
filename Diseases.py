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


def goal_test(s):
    return False

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


#</COMMON_CODE>

#<COMMON_DATA>
N_tiles = 8

#</COMMON_DATA>


#<STATE>
class State():
    def __init__(self, cities, aid, heur):
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

    def getCity(self, city):
        return self.cities[city]
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

    def giveAid(self, amount):
        alpha = 1
        beta = 1
        new_inf = math.exp(-amount*alpha) * self.susc
        new_rec = (1 - math.exp(-amount*beta)) * self.inf
        self.susc -= new_inf
        self.inf += new_inf
        self.inf -= new_rec
        self.rec += new_rec

    def score(self):
        return self.pop - self.inf
#</CITY>

#<INITIAL_STATE>
INITIAL_STATE = None
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
def updateCity(s, city, aid):
    newS = s.__copy__()
    newS.getCity(city).giveAid(aid)
    return newS

OPERATORS = [Operator("Give aid to city " + city.name,
    # The default value construct is needed
    # here to capture the values of p&q separately
    # in each iteration of the list comp. iteration.
    lambda s,c1=city: s.getCity(c1).needsAid(),
    lambda s,c1=city: updateCity(s, c1, 1))
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
