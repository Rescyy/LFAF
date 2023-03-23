from fa import FiniteAutomaton
from grammar import Grammar

def get_transitions(delta_function, state):
    transitions = []
    if type(state) == list:
        for component_state in state:
            for init_state, char, result_state in delta_function:
                if component_state == init_state:
                    transitions.append([state, char, result_state])
    for init_state, char, result_state in delta_function:
        if state == init_state:
            transitions.append([state, char, result_state])
    return transitions

def reduce_list(list):
    if len(list) == 1:
        return list[0]
    else:
        return list

class Convertor:

    def grammar_to_fa(self, grammar: Grammar):

        chomsky = grammar.chomsky_type()
        if type(chomsky) == int:
            raise ValueError(f"Can't convert grammar of type {chomsky} to finite automaton.")

        delta_function = []
        for non_terminal, result in grammar.transition_set:
            if len(result) > 1:
                delta_function.append([non_terminal, result[0], result[1:]])
            else:
                delta_function.append([non_terminal, result[0], 'Final'])

        return FiniteAutomaton(
            grammar.non_terminal_chars + ['Final'],
            grammar.terminal_chars,
            delta_function,
            grammar.non_terminal_chars[0],
            'Final'
        )
    
    def fa_to_grammar(self, fa: FiniteAutomaton):

        newtransition = []
        newnon_terminal = []

        for init_state, char, result_state in fa.delta_function:
            if str(result_state) in str(fa.final_states):
                newtransition.append([str(init_state), char])
            else:
                newtransition.append([str(init_state), char + str(result_state)])
            if str(init_state) not in newnon_terminal:
                newnon_terminal.append(str(init_state))

        return Grammar(
            newnon_terminal,
            fa.alphabet,
            newtransition
        )

    def nfa_to_dfa(self, fa: FiniteAutomaton):
        
        if fa.is_deterministic():
            print("This Finite Automaton is already deterministic")
            return fa
            
        current_states = [fa.initial_state]
        newtransition = []
        newstates = []
        newfinal = []

        while len(current_states) > 0:
            current_state = current_states.pop(0)
            temp1 = get_transitions(fa.delta_function, current_state)
            temp2 = [[current_state, i, []] for i in fa.alphabet]
            for __, char1, result_state1 in temp1:
                for __, char2, result_state2 in temp2:
                    if char1 == char2 and result_state1 not in result_state2:
                        result_state2.append(result_state1)
            newstates.append(current_state)
            for init_state, char, result_state in temp2:
                if len(result_state) != 0:
                    reduced_final_state = reduce_list(result_state)
                    newtransition.append([init_state, char, reduced_final_state])
                    if reduced_final_state not in current_states and reduced_final_state not in newstates: 
                        current_states.append(reduced_final_state)

        if type(fa.final_states) == list:
            for state in newstates:
                for final in fa.final_states:
                    if final in state:
                        newfinal.append(state)
        else:
            for state in newstates:
                if fa.final_states in state:
                    newfinal.append(state)

        return FiniteAutomaton(
            newstates,
            fa.alphabet,
            newtransition,
            fa.initial_state,
            reduce_list(newfinal)
        )