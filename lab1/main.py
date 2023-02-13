from grammar import grammar

def yesorno(a):
    if a:
        print("The string belongs to the finite automata")
    else:
        print("The string does not belong to the finite automata")

Vn = ['S', 'B', 'D', 'Q']
Vt = ['a', 'b', 'c', 'd']
P = [
    ['S',  'S',  'B',  'D',  'Q',  'D', 'Q'],
    ['aB', 'bB', 'cD', 'dQ', 'bB', 'a', 'dQ']
]

gr = grammar(Vn,Vt,P)
fa = gr.toFiniteAutomaton()

print(gr)
print(fa)
print("Generated strings:")
for i in range(5):
    str = gr.generateString()
    print(str)
    yesorno(fa.stringBelongToLanguage(str))

print("Stranger strings:")
list = ['abc','efg','adadada','bbbb','adddddaaa']
for i in list:
    print(i)
    yesorno(fa.stringBelongToLanguage(i))
