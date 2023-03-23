from random import choice

def index_return(list,a):
    temp = []
    for i in range(len(list)):
        if list[i][0] == a:
            temp.append(i)
    return temp

class Grammar:

    def __init__(self, Vn, Vt, P):
        self.non_terminal_chars = Vn
        self.terminal_chars = Vt
        self.transition_set = P

    def __str__(self):
        
        string = ''
        for i in self.transition_set:
            string += f"\n    {i}"
        return f"""Regular Grammar:
    Vn = {self.non_terminal_chars}
    Vt = {self.terminal_chars}
    P = {string}\n"""

    def generate_string(self, ammount = None):

        if ammount == None:
            iterated_string = self.non_terminal_chars[0]
            switch = 1
            while switch:
                switch = 0
                for char in self.non_terminal_chars:
                    if char in iterated_string:
                        choice_index = choice(index_return(self.transition_set,char))
                        iterated_string = iterated_string.replace(char, self.transition_set[choice_index][1])
                        switch = 1
            return iterated_string
        else:
            return [self.generate_string() for i in range(ammount)]

    def no_elements(self, string: str):

        no = 0
        for i in self.non_terminal_chars:
            no += string.count(i)
            string = string.replace(i, '')
        for i in self.terminal_chars:
            no += string.count(i)
        return no

    def chomsky_type(self):

        types = [0, 0, 0, 1]
        left = 0
        right = 0

        for condition, result in self.transition_set:
            no_result = self.no_elements(result)
            no_condition = self.no_elements(condition)
            if condition not in self.non_terminal_chars:
                if no_result < no_condition:
                    return 0
                types[1] = 1

            elif not types[2]:
                count = 0
                for i in self.non_terminal_chars:
                    if i in result:
                        count += 1
                        non_terminal_in_result = i
                if count > 1:
                    types[2] = 1
                elif count and no_result > no_condition:
                    pos = result.find(non_terminal_in_result)
                    if pos == no_result - len(non_terminal_in_result):
                        left = 1
                    elif pos == 0:
                        right = 1
                    else:
                        types[2] = 1
                    if left and right:
                        types[2] = 1
                elif count:
                    types[2] = 1

        for i in range(4):
            if i == 3 and right:
                return (3, 'right')
            if i == 3 and left:
                return (3, 'left')
            if types[i]:
                return i
                    

