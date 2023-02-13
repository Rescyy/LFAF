# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Crucerescu Vladislav

----

## Theory

There are two key concepts that had to be studied for this laboratory work: regular grammar and finite automata. These concepts are strongly related to each other, they both can produce the same thing, and they can be derived one from another. The regular grammar is defined as follows:

Let: 
V_N  be the set of non-terminal symbols;
V_T  be the set of terminal symbols;
P be the set of production rules.

In our case, the Chomsky type is left linear type 3, and there is no more than one terminal symbol in each production rule, meaning:

P={A→aB|for some A,B∈V_N∪{ε},a∈V_T}

The finite automaton is defined as follows:

Let:
Q be the finite set of states;
Σ be the alphabet;
δ be the transition function;
q_0  be the initial state;
F be the set of final states.

In order to convert a regular grammar to a finite automaton, we must use the following algorithm:

Q=V_T∪{Final};
Σ=V_N;
δ(q,b)={r}  where q,b,r=A,a,B,∀x∈P where x=A→aB
if B=ε,r=Final;
q_0=S,where S is the starting non-terminal symbol;
F={Final};

This algorithm works for the code written by me, even though it might not be the official definition for converting regular grammar to finite automata. Given a string, we must iterate through it, pass the elements and the current state through the δ function, changing the state and iterating to the next element, until there are no elements in the string left. If the state at the end is in the set of final states, then the string belongs to the finite automaton. If there are no corresponding state to the delta function definition, then the string does not belong to the finite automaton.

## Objectives:

1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

    a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

    b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

    c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it.


## Implementation description

* The grammar is under this format:

```
Grammar:
Vn = ['S', 'B', 'D', 'Q']
Vt = ['a', 'b', 'c', 'd']
P = [['S', 'S', 'B', 'D', 'Q', 'D', 'Q'], ['aB', 'bB', 'cD', 'dQ', 'bB', 'a', 'dQ']]
```

As you can see, the transitions in the set P, are structured in 2 lists where each state has one or more corresponding transitions.

* The finite automaton is under this format:

```
Finite automaton:
Q = ['S', 'B', 'D', 'Q', 'Final']
Sigma = ['a', 'b', 'c', 'd']
Delta = [[['S', 'a'], ['S', 'b'], ['B', 'c'], ['D', 'd'], ['Q', 'b'], ['D', 'a'], ['Q', 'd']], ['B', 'B', 'D', 'Q', 'B', 'Final', 'Q']]
q0 = S
F = ['Final']
```

The delta list contains a list of the arguments it can accept, and the list of the corresponding states it transitions to.

* Here we can see how the grammar generates strings:

```
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
```

The function checks for existing non-terminal states in the string and switches them for the corresponding transition string.

* Here is the function that outputs a finite automaton based on the grammar class it is called from:

```
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
```

Just as described in the theory section, different elements and sets are taken from the grammar and put into the finite automaton through a constructor function.

* Here is function that verifies whether the string belongs to the set automaton.

```
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
```

It iterates through the string and checks if there are corresponding state and string arguments for the delta function. If after the iteration the state is not part of F, then it will return 0. If a certain character does not belong to the alphabet, it will return 0, though I know this line might be redundant since the delta function argument checker rules that out as well, it's just a small optimisation.

* Here are some corresponding generated strings for the grammar:

```
Generated strings:
bcdbca
The string belongs to the finite automata
acddbca
The string belongs to the finite automata
acdbca
The string belongs to the finite automata
aca
The string belongs to the finite automata
bca
The string belongs to the finite automata
```

The finite automaton instantly identifies them as belonging to it.

If we are to input some stranger strings it will do the following:

```
Stranger strings:
abc
The string does not belong to the finite automata
efg
The string does not belong to the finite automata
adadada
The string does not belong to the finite automata
bbbb
The string does not belong to the finite automata
adddddaaa
The string does not belong to the finite automata
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented the concept of regular grammar and finite automaton. I learned how they work and their relationship with each other. I learned to convert a regular grammar to a finite automaton and check the corresponding strings through it. I recognise that the grammar given to me is a simple one to deal with, should the grammar have been more complicated where the finite automaton would have become nondeterminant, some difficulties would arise.