from grammar import Grammar
from convertor import Convertor
from fa import Finiteautomaton
from matplotlib.pyplot import show as show_graph

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

def yesorno(a):
    if a == 1:
        print("The string belongs to the finite automata")
    elif a == 0:
        print("The string does not belong to the finite automata")

# Vn = ['S', 'B', 'D', 'Q']
# Vt = ['a', 'b', 'c', 'd']
# P = [
#     ['S', 'aB'],
#     ['S', 'bB'],
#     ['B', 'cD'],
#     ['D', 'dQ'],
#     ['Q', 'bB'],
#     ['D', 'a'],
#     ['Q', 'dQ']]

convert = Convertor()
fa = Finiteautomaton(Q, sigma, delta, q0, F)
# gr = Grammar(Vn, Vt, P)
# for i in gr.generate_string(ammount = 100):
#     print(i)
# print(gr.chomsky_type())
# print(fa)
dfa = convert.nfa_to_dfa(fa)
# print(dfa)
# gr = convert.fa_to_grammar(fa)
# print(gr)
# gr1 = convert.fa_to_grammar(dfa)
# print(gr1)
# print(gr.generate_string())
# print(gr1.generate_string(ammount = 10))
fa.prepare_graph(1)
dfa.prepare_graph(2)
show_graph()