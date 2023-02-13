from finiteautomaton import finiteautomaton
import random as r

def indexReturn(list,a):
    temp = []
    for i in range(len(list)):
        if list[i] == a:
            temp.append(i)
    return temp

class grammar:

    def __init__(self, Vn, Vt, P):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P

    def __str__(self) -> str:
        return f"Grammar:\nVn = {self.Vn}\nVt = {self.Vt}\nP = {self.P}\n"

    def generateString(self):
        string = 'S'
        switch = 1
        while switch:
            switch = 0
            for i in range(len(string)):
                if string[i] in self.Vn:
                    a = r.choice(indexReturn(self.P[0], string[i]))
                    string = string[:i] + self.P[1][a] + string[i+1:]
                    switch = 1
        return string

    def toFiniteAutomaton(self):
        delta = [[],[]]
        for i in range(len(self.P[0])):
            a = self.P[0][i]
            b = self.P[1][i]
            delta[0].append([a,b[0]])
            if len(b) == 2:
                delta[1].append(b[1])
            else:
                delta[1].append('Final')
        fa = finiteautomaton(list(self.Vn), self.Vt, delta, 'S', ['Final'])
        fa.Q.append('Final')
        return fa