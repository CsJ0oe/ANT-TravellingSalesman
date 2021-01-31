import numpy as np
import random
 
class Config:
    CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)), ("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)), ("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)), ("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)),("Rennes",(48.083333,-1.683333)),("Pau",(43.3,-0.366667)))
    CITIES_LEN = len(CITIES)
    pheromones = {}
 
    def __init__(self, A=1, B=1, Y=0, Q=1, EPS=.1, evaporation=.1):
        self.A = A
        self.B = B
        self.Y = Y
        self.Q = Q
        self.EPS = EPS
        self.evaporation = evaporation
        for i in range(self.CITIES_LEN):
            for j in range(self.CITIES_LEN):
               self.pheromones[(i,j)] = self.Q
 
    def distance(self, a,b):
        (v1,(x1,y1)), (v2,(x2,y2)) = (self.CITIES[a],self.CITIES[b])
        return np.sqrt((x1-x2)**2+(y1-y2)**2)

class Fourmi:
    pathLength = 0
    visited = []

    def __init__(self):
        '''Start at Bordeaux'''
        self.visited = [0]
        self.pathLength = 0

    def constructPath(self):
        global config
        self.visited = [0]
        self.pathLength = 0
        while len(self.visited) < config.CITIES_LEN:
            self.visited.append(self._nextCity())
            self.pathLength += config.distance(self.visited[-2], self.visited[-1])
        self.visited.append(0)
        self.pathLength += config.distance(self.visited[-2], self.visited[-1])

    def deposePheromones(self):
        global config
        for i in range(1, len(self.visited)):
            config.pheromones[(self.visited[i-1],self.visited[i])] += config.Q/self.pathLength

    def _nextCity(self):
        global config
        i = self.visited[-1]
        allowed = []
        proba = []
        for k in range(config.CITIES_LEN):
            if (k in self.visited):
                continue
            allowed.append(k)
        pre_calc = 0
        for k in allowed:
            pre_calc += ((config.pheromones[(i, k)])**config.A) * ((1/config.distance(i, k))**config.B) + config.Y
        for j in allowed:
            proba.append( ( ((config.pheromones[(i, j)])**config.A) * ((1/config.distance(i, j))**config.B) + config.Y ) / pre_calc )
        if np.random.random() < config.EPS:
            return allowed[np.argmax(proba)]
        else:
          return random.choices(allowed, weights=proba)[0]

class Colonie():
    _fourmis = []
    _colonieSize = None

    def __init__(self, colonieSize):
        self._colonieSize = colonieSize
        for i in range(self._colonieSize):
            self._fourmis.append(Fourmi())

    def oneIteration(self):
        global config
        for f in self._fourmis:
            f.constructPath()
        for f in self._fourmis:
            f.deposePheromones()
        # intensify best path (faster convergence)
        m,f = self.bestPath()
        for i in range(1, len(f.visited)):
            config.pheromones[(f.visited[i-1],f.visited[i])] += config.Q
        '''Pheromones evaporation'''
        for r in config.pheromones:
            config.pheromones[r] *= (1 - config.evaporation)

    def bestPath(self):
        minn = None
        f = None
        for i in self._fourmis:
            #print(i.pathLength, " : ", i.visited)
            if (minn is None) or (i.pathLength < minn):
                minn = i.pathLength
                f = i
        return minn, f

import matplotlib.pyplot as plt

config = Config(A=1, B=1, Y=0, Q=2)
colonie = Colonie(10)
Y1 = []
for i in range(60):
    colonie.oneIteration()
    R, _ = colonie.bestPath()
    Y1 += [R]
    print ("Iteration :: ", i, "/ BEST :: ", R)
colonie.bestPath()
plt.plot(range(len(Y1)), Y1, 'b+')
plt.show()
plt.close()

