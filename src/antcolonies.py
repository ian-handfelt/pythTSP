import random
import sys
import csv
from ants import Ant

class AntColony:
    def __init__(self, graph, numAnts, numIters):
        self.graph = graph
        self.numAnts = numAnts
        self.numIters = numIters
        self.Alpha = 0.1
        self.reset()

    def reset(self):
        self.LowerBoundCost = sys.maxint
        self.LowerBoundPath = None
        self.LowerBoundMatrix = None
        self.PriorLowerBoundPath = 0

    def start(self):
        self.ants = self.GenerateAnts()
        self.iter_counter = 0

        while self.iter_counter < self.numIters:
            self.iteration()
            # Note that this will help refine the results future iterations.
            self.global_updating_rule()

    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()

    def numAnts(self):
        return len(self.ants)

    def numIters(self):
        return self.numIters

    def iteration_counter(self):
        return self.iter_counter

    def update(self, ant):
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.LowerBoundCost:
            self.LowerBoundCost = ant.path_cost
            self.LowerBoundMatrix = ant.path_mat
            self.LowerBoundPath = ant.path_vec
            self.PriorLowerBoundPath = self.iter_counter
        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print "Best: %s, %s, %s, %s" % (
                self.LowerBoundPath, self.LowerBoundCost, self.iter_counter, self.avg_path_cost,)
            with open('output.csv', 'ab') as f:
                writer = csv.writer(f)
                writer.writerow((self.iter_counter, self.LowerBoundPath, self.LowerBoundCost, self.avg_path_cost))
        
    def done(self):
        return self.iter_counter == self.numIters

    def GenerateAnts(self):
        self.reset()
        ants = []
        for i in range(0, self.numAnts):
            ant = Ant(i, random.randint(0, self.graph.numNodes - 1), self)
            ants.append(ant)

        return ants
 
    def global_updating_rule(self):
        #updates the desirability of nodes for future colonies of ants when building each ant's path.
        #evaporation is the fixed rate of reduction to the pheromone where the pheromone is one of two components every time an ant must choose the next node in its path
        #deposition is a function of the ant's completed path total cost and the number of ants who chose that path
        evaporation = 0
        deposition = 0
        for r in range(0, self.graph.numNodes):
            for s in range(0, self.graph.numNodes):
                if r != s:
                    delt_tau = self.LowerBoundMatrix[r][s] / self.LowerBoundCost
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau
                    self.graph.update_tau(r, s, evaporation + deposition)

