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


def h_state(s):
    sum = 0
    for city in s.cities:
       sum += city.score()

    return sum

#</COMMON_CODE>

#<COMMON_DATA>
cities = []
#</COMMON_DATA>


#<STATE>
class State():
    def __init__(self, cities):
        self.cities = {}
        for city in cities:
            self.cities[city.name] = city

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # Produces a brief textual description of a state.
        total_population = 0
        total_infected = 0
        txt = "City\t\tPopulation\t% Infected\n"
        for name, city in self.cities.items():
            name = name + ("\t" if len(name) < 8 else "")
            pop = int(city.pop)
            inf = int(city.inf)
            total_population += pop
            total_infected += inf
            txt += name + "\t" + "{:,}".format(pop * 1000) + "\t" + str(inf/pop) + "\n" 
        txt += "\n" + "Total % Infected: " + str(total_infected/total_population)
        return txt

    def __eq__(self, other):
        if isinstance(other, State):
            if len(self.cities) != len(other.cities): return False
            for name, city in self.cities.items():
                if not other.cities[name].__eq__(city): return False
            return True

    def __lt__(self, other):
        if isinstance(other, State):
            return (self.getScore()) < (other.getScore())

    def __hash__(self):
        h = ""
        for n, c in self.cities.items():
            h += str(c.inf)
        return h.__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        newCities = []
        for name, city in self.cities.items():
            newCities.append(city.__copy__())
        newS = State(newCities)
        return newS

    def getCity(self, city):
        return self.cities[city]

    def getScore(self):
        score = 0
        for c in self.cities:
            score += c.score()
        return score

#</STATE>

#<CITY>
class City():
    def __init__(self, name, lat, lng, pop, medAge, lifeExp, gdp, airpts, inf=0.0, susc=0.0,
            recov=0.0, ds=0.0, di=0.0, dr=0.0):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.pop = pop
        self.medAge = medAge
        self.lifeExp = lifeExp
        self.gdp = gdp
        self.airpts = airpts
        self.susc = float(pop) * 0.7
        self.inf = float(pop) * 0.3
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
        newCity = City(self.name, self.lat, self.lng, self.pop, self.medAge,
                self.lifeExp, self.gdp, self.airpts, self.inf, self.susc,
                self.recov)
        return newCity

    def giveAid(self, amount):
        alpha = 1
        beta = 1
        new_inf = math.exp(-amount*alpha) * self.susc
        new_recov = (1 - math.exp(-amount*beta)) * self.inf
        self.susc -= new_inf
        self.inf += new_inf
        self.inf -= new_recov
        self.recov += new_recov

    def needsAid(self):
        return self.inf > 0

    def score(self):
        return self.pop - self.inf
#</CITY>

#<INITIAL_STATE>
def CREATE_INITIAL_STATE():
    cities = []
    with open("cities.tsv", 'r') as city_data:
        for i, line in enumerate(city_data):
            if i != 0:
                c = line.split('\t')
                name = c[0]
                lat = c[2]
                lng = c[3]
                pop = c[5]
                medAge = c[6]
                lifeExp = c[7]
                gdp = c[10]
                airpts = c[11]
                cities.append(City(name, lat, lng, pop, medAge, lifeExp, gdp, airpts))
    return State(cities)
INITIAL_STATE = CREATE_INITIAL_STATE()
#</INITIAL_STATE>

#<OPERATORS>
def updateCity(s, city, aid):
    newS = s.__copy__()
    newS.getCity(city).giveAid(aid)
    return newS

OPERATORS = [Operator("Gave aid to " + name,
    # The default value construct is needed
    # here to capture the values of p&q separately
    # in each iteration of the list comp. iteration.
    lambda s,n=name: s.getCity(n).needsAid(),
    lambda s,n=name: updateCity(s, n, 1))
    for name in INITIAL_STATE.cities]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS> (optional)
HEURISTICS = {'h_state': h_state}
#</HEURISTICS>
