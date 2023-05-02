from grammar import Grammar

max = 2

def truth_list(a: int):
    if a == 1:
        return [[0]]
    b = a**2
    c = 0
    truth_list = []
    for _ in range(b-1):
        str = bin(c)[2:]
        truth_list.append([int(i) for i in list('0'*(a-len(str)) + str)])
        c += 1
    return truth_list

def id_maker(a):
    a = str(a)
    return (max - len(a)) * '0' + a

class ChomskyNormalFormConvertor:

    def start(self, grammar: Grammar) -> None:
        first = grammar.non_terminal_symbols[0]
        grammar.non_terminal_symbols.insert(0,f"<{first}>")
        grammar.transition_set.append([f"<{first}>", first])

    def remove_null_productions(self, grammar: Grammar, i=0) -> None:
        null_symbols = []
        while i < len(grammar.transition_set):
            if not grammar.transition_set[i][1] and grammar.transition_set[i][0] != grammar.non_terminal_symbols[0]:
                null_symbols.append(grammar.transition_set.pop(i)[0])
            else:
                i += 1
        if not null_symbols:
            return
        new_transitions = []
        for non_terminal in null_symbols:
            for init, result in grammar.transition_set:
                if non_terminal in result:
                    components = result.split(non_terminal)
                    bin_list = truth_list(len(components) - 1)
                    for binary in bin_list:
                        string = components[0]
                        for i in range(len(binary)):
                            if binary[i]:
                                string += non_terminal
                            string += components[i+1]
                        if [init, string] not in new_transitions and init not in null_symbols:
                            new_transitions.append([init, string])
            grammar.transition_set += new_transitions
        self.remove_null_productions(grammar, i)

    def remove_unit_productions(self, grammar: Grammar) -> None:
        i = 0
        while i < len(grammar.transition_set):
            if grammar.transition_set[i][1] in grammar.non_terminal_symbols:
                transition = grammar.transition_set.pop(i)
                for init, result in grammar.transition_set:
                    if transition[1] == init and [transition[0], result] not in grammar.transition_set:
                        grammar.transition_set.append([transition[0], result])
            else:
                i += 1

    def reduce_large_results(self, grammar: Grammar) -> None:
        i = 0
        new_symbols = 0
        while i < len(grammar.transition_set):
            if grammar.no_symbols(grammar.transition_set[i][1]) > 2:
                symbols = grammar.split_string(grammar.transition_set[i][1])
                init = grammar.transition_set.pop(i)[0]
                grammar.transition_set.append([init, f"{symbols[0]}<X{id_maker(new_symbols)}>"])
                grammar.non_terminal_symbols.append(f"<X{id_maker(new_symbols)}>")
                for j in range(1,len(symbols)-2):
                    grammar.transition_set.append([f"<X{id_maker(new_symbols)}>", f"{symbols[j]}<X{id_maker(new_symbols+1)}>"])
                    new_symbols += 1
                    grammar.non_terminal_symbols.append(f"<X{id_maker(new_symbols)}>")
                grammar.transition_set.append([f"<X{id_maker(new_symbols)}>", f"{symbols[-2]}{symbols[-1]}"])
                new_symbols += 1
            else:
                i += 1

    def change_productions(self, grammar: Grammar) -> None:
        new_symbols = 0
        for char in grammar.terminal_symbols:
            grammar.transition_set.append([f"<Y{id_maker(new_symbols)}>", char])
            grammar.non_terminal_symbols.append(f"<Y{id_maker(new_symbols)}>")
            new_symbols += 1
        for i in range(len(grammar.transition_set)):
            if grammar.transition_set[i][0] != grammar.non_terminal_symbols[0] or len(grammar.transition_set[i][1]) != 0:
                if grammar.transition_set[i][1][0] in grammar.terminal_symbols and len(grammar.transition_set[i][1]) != 1:
                    grammar.transition_set[i][1] = f"<Y{id_maker(grammar.terminal_symbols.index(grammar.transition_set[i][1][0]))}>{grammar.transition_set[i][1][1:]}"
                if grammar.transition_set[i][1][-1] in grammar.terminal_symbols and len(grammar.transition_set[i][1]) != 1:
                    grammar.transition_set[i][1] = f"{grammar.transition_set[i][1][:-1]}<Y{id_maker(grammar.terminal_symbols.index(grammar.transition_set[i][1][-1]))}>"

    def remove_questionable_results(self, grammar: Grammar) -> None:
        unreachable_symbols = list(grammar.non_terminal_symbols)[1:]
        for _, result in grammar.transition_set:
            splitted_result = grammar.split_string(result)
            for element in splitted_result:
                if element in grammar.non_terminal_symbols and element in unreachable_symbols:
                    unreachable_symbols.remove(element)
        for state in unreachable_symbols:
            grammar.non_terminal_symbols.remove(state)
        i = 0
        while i < len(grammar.transition_set):
            if grammar.transition_set[i][0] in unreachable_symbols:
                grammar.transition_set.pop(i)
            else:
                i += 1

    def get_chomsky_normal_form(self, grammar: Grammar) -> Grammar:
        new_grammar = Grammar(
            grammar.non_terminal_symbols.copy(),
            grammar.terminal_symbols.copy(),
            [transition.copy() for transition in grammar.transition_set])
        # print("begin\n",new_grammar)
        self.start(new_grammar)
        # print("start\n",new_grammar)
        self.remove_null_productions(new_grammar)
        # print("remove_null_prod\n",new_grammar)
        self.remove_unit_productions(new_grammar)
        # print("remove_unit_prod\n",new_grammar)
        self.reduce_large_results(new_grammar)
        # print("remove_large_results\n",new_grammar)
        self.change_productions(new_grammar)
        # print("change_productions\n",new_grammar)
        self.remove_questionable_results(new_grammar)
        # print("remove_questionable_results\n",new_grammar)
        return new_grammar