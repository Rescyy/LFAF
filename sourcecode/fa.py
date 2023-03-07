from networkx import DiGraph, circular_layout, kamada_kawai_layout, draw, draw_networkx_edge_labels, planar_layout, spectral_layout
from matplotlib.pyplot import figure

def index_return(a,b,list):
    for i in range(len(list)):
        if a == list[i][0] and b == list[i][1]:
            return i
    return -1

class Finiteautomaton:

    def __init__(self, Q, sigma, delta_function, q0, F):

        self.all_states = Q
        self.alphabet = sigma
        self.delta_function = delta_function
        self.initial_state = q0
        self.final_states = F
        self.determinism = False
        self.is_deterministic()

    def __str__(self):

        string = ''
        for i in self.delta_function:
            string += f"\n    {i}"
        return f"""Finite Automaton:
    Q = {self.all_states}
    Sigma = {self.alphabet}
    Delta = {string}
    q0 = {self.initial_state}
    F = {self.final_states}\n"""

    def contains(self,string):

        if self.is_deterministic():
            if type(string) == list:
                return []
            else:
                current_state = self.initial_state
                for i in string:
                    a = index_return(current_state, i, self.delta_function)
                    if a == -1:
                        return False
                    current_state = self.delta_function[a][2]
                if current_state == self.final_states:  
                    return True
                return False
        else:
            print("This is a nondeterministic finite automaton.\nPlease convert it to a deterministic finite automaton first.")
            return -1

    def is_deterministic(self):

        if self.determinism:
            return True
        count = 0
        for init_state1, char1, __ in self.delta_function:
            for init_state2, char2, __ in self.delta_function:
                if init_state1 == init_state2 and char1 == char2:
                    count += 1
        if count > len(self.delta_function):
            return False
        self.determinism = True
        return True

    def prepare_graph(self,fig):

        figure(fig)
        G = DiGraph()
        node_sizes = list()
        node_colors = list()
        for state in self.all_states:
            newstate = str(state).replace('[', '{').replace(']', '}').replace('\'','').replace('\"','')
            G.add_node(newstate)
            node_sizes.append(100 * (len(newstate)**(1.618033988749894) + 1))
            if type(self.final_states) == list:
                if state in self.final_states:
                    node_colors.append('r')
                elif state == self.initial_state:
                    node_colors.append('b')
                else:
                    node_colors.append('w')
            else:
                if state == self.final_states:
                    node_colors.append('r')
                elif state == self.initial_state:
                    node_colors.append('b')
                else:
                    node_colors.append('w')
        edge_labels = dict()
        for init_state, char, result_state in self.delta_function:
            source_state = str(init_state).replace('[', '{').replace(']', '}').replace('\'','').replace('\"','')
            destination_state = str(result_state).replace('[', '{').replace(']', '}').replace('\'','').replace('\"','')
            G.add_edge(source_state, destination_state)
            if (source_state, destination_state) in edge_labels:
                edge_labels[source_state, destination_state] += ',' + char
            else:
                edge_labels[source_state, destination_state] = char
        #pos = kamada_kawai_layout(G)
        #pos = planar_layout(G)
        pos = circular_layout(G)
        draw(G, pos, node_color = node_colors, edgecolors = 'k', width = 2.0, with_labels = True, node_size = node_sizes)
        draw_networkx_edge_labels(G, pos, edge_labels)