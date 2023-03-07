#LAB 2 LFAF
#Name: Crucerescu Vladislav
#Group: FAF-212
#Variant: 9

from grammar import Grammar
from convertor import Convertor
from fa import FiniteAutomaton
from matplotlib.pyplot import show as show_graph

Vn = ['S', 'B', 'D', 'Q']
Vt = ['a', 'b', 'c', 'd']
P = [
    ['S', 'aB'],
    ['S', 'bB'],
    ['B', 'cD'],
    ['D', 'dQ'],
    ['Q', 'bB'],
    ['D', 'a'],
    ['Q', 'dQ']
]
grammar = Grammar(Vn, Vt, P)

print("Task 2\n")
print(grammar)
print(f"Chomsky Type of Grammar is: {grammar.chomsky_type()}\n")

Q = ['q0', 'q1', 'q2', 'q3', 'q4']
sigma = ['a', 'b', 'c']
delta = [
    ['q0', 'a', 'q1'],
    ['q1', 'b', 'q2'],
    ['q2', 'c', 'q0'],
    ['q1', 'b', 'q3'],
    ['q3', 'a', 'q4'],
    ['q3', 'b', 'q0']
]
q0 = 'q0'
F = 'q4'
fa = FiniteAutomaton(Q, sigma, delta, q0, F)

convert = Convertor()
print("Task 3\n")
print(fa)
print(f"Converted Finite Automaton to {convert.fa_to_grammar(fa)}")
print(f"This Finite Automaton is deterministic: {fa.is_deterministic()}\n")
dfa = convert.nfa_to_dfa(fa)
print(f"Converted Non-Deterministic Finite Automaton to Deterministic {dfa}")
fa.prepare_graph(1)
dfa.prepare_graph(2)
show_graph()