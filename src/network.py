class Graph:
    def __init__(self, numNodes, delta_mat, tau_mat=None):
        print len(delta_mat)
        if len(delta_mat) != numNodes:
            raise Exception("len(delta) != numNodes")
        self.numNodes = numNodes
        self.delta_mat = delta_mat 
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, numNodes):
                self.tau_mat.append([0] * numNodes)

    def delta(self, r, s):
        return self.delta_mat[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    def update_tau(self, r, s, val):
        self.tau_mat[r][s] = val

    def reset_tau(self):
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.numNodes * 0.5 * avg)
        print "Average = %s" % (avg,)
        print "Tau0 = %s" % (self.tau0)
        for r in range(0, self.numNodes):
            for s in range(0, self.numNodes):
                self.tau_mat[r][s] = self.tau0


    def average_delta(self):
        return self.average(self.delta_mat)


    def average_tau(self):
        return self.average(self.tau_mat)

    def average(self, matrix):
        sum = 0
        for r in range(0, self.numNodes):
            for s in range(0, self.numNodes):
                sum += matrix[r][s]

        avg = sum / (self.numNodes * self.numNodes)
        return avg
