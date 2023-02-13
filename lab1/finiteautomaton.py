def indexReturn(list,a):
    for i in range(len(list)):
        if list[i] == a:
            return i
    return -1

class finiteautomaton:

    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def __str__(self):
        return f"Finite automaton:\nQ = {self.Q}\nSigma = {self.sigma}\nDelta = {self.delta}\nq0 = {self.q0}\nF = {self.F}\n"

    def stringBelongToLanguage(self,string):
        q = self.q0
        for i in string:
            if i in self.sigma:
                a = indexReturn(self.delta[0], [q, i])
                if a == -1:
                    return 0
                q = self.delta[1][a]
            else:
                return 0
        if q in self.F:  
            return 1
        return 0