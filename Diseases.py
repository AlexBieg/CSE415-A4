'''
Cole Chamberlin 1434297 jessec18, Alex Bieg 1337896 biega
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
    return "Malaria is erradicated"

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
    for n, c in s.cities.items():
       sum += c.score()

    return sum + s.cost

#</COMMON_CODE>

#<COMMON_DATA>
cities = []
#</COMMON_DATA>


#<STATE>
class State():
    def __init__(self, cities, date=0, cost=0):
        self.cities = {}
        self.cities = cities
        self.date = date
        self.cost = cost

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # Produces a brief textual description of a state.
        total_population = 0
        total_infected = 0
        txt = "Date: " + str(self.date) + "\n"
        txt += "City\t\tPopulation\t% Infected\n"
        for name, city in self.cities.items():
            name = name + ("\t" if len(name) < 8 else "")
            pop = int(city.pop)
            inf = int(city.inf)
            total_population += pop
            total_infected += inf
            txt += name+"\t"+"{:,}".format(pop*1000)+"\t"+str(int(100 * inf / city.pop))+"\n"
        txt += "\n"+"Total % Infected: "+str(int(100*total_infected/total_population))
        return txt

    def __eq__(self, other):
        if isinstance(other, State):
            if len(self.cities) != len(other.cities):
                return False
            for name, city in self.cities.items():
                if not other.cities[name].__eq__(city):
                    return False
            return True


    def __lt__(self, other):
        if isinstance(other, State):
            return (h_state(self)) < (h_state(other))

    def __hash__(self):
        h = ""
        for n, c in self.cities.items():
            h += str(c.__hash__())

        return h.__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        newCities = {}
        for name, city in self.cities.items():
            newCities[name] = city.__copy__()
        newS = State(newCities, self.date+1)
        return newS

    def getCity(self, city):
        return self.cities[city]

    # compute the total number of infected individuals in the country
    def getScore(self):
        score = 0
        for n, c in self.cities.items():
            score += c.score()
        return score

#</STATE>

#<CITY>
class City():

    def __init__(self, name, lat, lng, pop, medAge, lifeExp, gdp, airpts, size,
            inf=0.0, susc=0.0, recov=0.0):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.pop = pop
        self.medAge = medAge
        self.lifeExp = lifeExp
        self.gdp = gdp
        self.airpts = airpts
        self.size = size
        self.susc = float(pop) * 0.5
        self.inf = float(pop) * 0.5
        self.recov = recov

    def __eq__(self, other):
        is_same = False
        if isinstance(other, City):
            rec = self.recov == other.recov
            sus = self.susc == other.susc
            inf = self.inf == other.inf
            name = self.name = other.name

            is_same = (rec and sus and inf and name)
        return is_same

    def __hash__(self):
        (self.name + str(self.lat) + str(self.lng) + str(self.susc) + str(self.recov) + str(self.inf)).__hash__()

    def __str__(self):
        return str(self.name) + " infected: " + str(self.inf) + " recovered: " + str(self.recov)

    def __copy__(self):
        newCity = City(self.name, self.lat, self.lng, self.pop, self.medAge,
                self.lifeExp, self.gdp, self.airpts, self.size, self.inf, 
                self.susc, self.recov)
        return newCity

    # update the infection rates of a city based on the amount of aid given
    def giveAid(self, amount):
        try:
            amt_per_person = 10000 * amount / (self.pop - self.recov)
        except(ZeroDivisionError):
            amt_per_person = 0
        # how much effect the aid has on stopping new infections
        self.alpha = self.susc * amt_per_person 
        # how much effect the aid has on curing infected people
        self.beta = self.inf * amt_per_person 
        # delta: how quickly infection spreads with no aid
        # gets set outside of city since it references other cities
        # gamma: how quickly people recover with no aid
        self.gamma = self.gdp / (self.medAge * 1000)
        # repro: how quickly the disease reproduces
        self.repro = 0.2
        new_inf = int(self.repro*math.exp(-max(0, self.alpha-self.delta))*self.susc)
        # update susceptible and infected populations
        self.susc -= new_inf
        self.inf += new_inf
        new_recov = int((1 - math.exp(-max(0, self.beta+self.gamma)))*self.inf)
        # update susceptible and infected populations
        self.inf -= new_recov
        self.recov += new_recov

    # computes distance between each pair of cities, total number of airports
    # and creates a delta value for the model
    def calcDist(self, s):
        for n, c in s.cities.items():
            if self != c:
                dist = math.sqrt((self.lat-c.lat)**2 + (self.lng-c.lng)**2)
                air = self.airpts * c.airpts
                # delta directly proportional to number of infected people,
                # product of number of airports and inversely proportional to
                # the distance between the cities
                self.delta = c.inf * air / (dist * 10000)
         
    # precondition for operator
    def needsAid(self):
        return self.inf > 0

    # score of city is based on total number of infectd people
    def score(self):
        return self.inf
#</CITY>

#<INITIAL_STATE>
def CREATE_INITIAL_STATE():
    cities = {}
    with open("cities.tsv", 'r') as city_data:
        for i, line in enumerate(city_data):
            # read from tsv
            if i != 0:
                c = line.split('\t')
                name = c[0]
                lat = float(c[2])
                lng = float(c[3])
                pop = int(c[5])
                medAge = float(c[6])
                lifeExp = float(c[7])
                gdp = int(c[11])
                airpts = int(c[12])
                size = int(c[13])
                city = City(name, lat, lng, pop, medAge, lifeExp, gdp, airpts,
                        size)
                cities[city.name] = city
    return State(cities)
INITIAL_STATE = CREATE_INITIAL_STATE()
#</INITIAL_STATE>

#<OPERATORS>
def updateCity(s, city, aid):
    newS = s.__copy__()
    # increment aid distributed
    newS.cost += aid
    for n, c in newS.cities.items():
        # compute the distances between each pair of cities
        c.calcDist(newS)
        # give aid to one city
        if n == city:
            c.giveAid(1)
        else:
            c.giveAid(0)
    return newS

OPERATORS = [Operator("Gave aid to " + name,
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
HEURISTICS = [h_state]
#</HEURISTICS>
