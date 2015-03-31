import pickle
import sys
import traceback
import csv
from network import Graph
from antcolonies import AntColony

def main(argv):
    numNodes = 10
    with open('output.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(('Iteration', 'Best Path', 'Minimum Path Cost', 'Average Path Cost'))
        f.close()

    if len(argv) >= 3 and argv[0]:
        numNodes = int(argv[0])

    if numNodes <= 10:
        numAnts = 20
        numIters = 12
        numReps = 1
    else:
        numAnts = 28
        numIters = 20
        numReps = 1

    tempNetworkInput = pickle.load(open('citiesAndDistances.pickled', "r")) #argv[1]
    Nodes = tempNetworkInput[0]
    ArcCosts = tempNetworkInput[1]
    numNodes = len(ArcCosts)
    # why are we doing this?
    if numNodes < len(ArcCosts):
        ArcCosts = ArcCosts[0:numNodes]
        for i in range(0, numNodes):
            ArcCosts[i] = ArcCosts[i][0:numNodes]



    try:
        graph = Graph(numNodes, ArcCosts)
        LowerBoundPath = None
        LowerBoundCost = sys.maxint
        for i in range(0, numReps):
            print "Repetition %s" % i
            graph.reset_tau()
            antcolony = AntColony(graph, numAnts, numIters)
            print "Colony Started"
            antcolony.start()
            if antcolony.LowerBoundCost < LowerBoundCost:
                # print "Colony Path"
                LowerBoundPath = antcolony.LowerBoundPath
                LowerBoundCost = antcolony.LowerBoundCost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (LowerBoundPath,)
        OptimalPath = []
        for node in LowerBoundPath:
            print Nodes[node] + " ",
            OptimalPath.append(Nodes[node])
        print "\nBest path cost = %s\n" % (LowerBoundCost,)
        results = [LowerBoundPath, OptimalPath, LowerBoundCost]
        pickle.dump(results, open('output.pickled', 'w+')) #argv[2]
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])    

