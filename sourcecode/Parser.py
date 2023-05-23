from typing import List
import token
from token import Token

def error(message=None):
    if message:
        raise ValueError(message)
    raise ValueError("Declaration Error")

class Instantiation:

    def __init__(self, type: str, varlist: List[str]):
        self.type = type
        self.varlist = varlist

    def __str__(self):
        return f"Instantiation: {self.type} {self.varlist}"


class Placefield:

    def __init__(self, type: str, var: str, val: int):
        self.type = type
        self.var = var
        self.val = val

    def __str__(self):
        return f"Placefield: {self.type} {self.var} {self.val}"


class Arc:

    def __init__(self, source: str, destination: str, val: int):
        self.source: str = source
        self.destination: str = destination
        self.val: int = val

    def __str__(self):
        return f"Arc: {self.source} {self.destination} {self.val}"


class Arcing:

    def __init__(self, type: str, arcs: List[Arc]):
        self.type: str = type
        self.arcs: list[Arc] = arcs

    def __str__(self):
        string = f"Arcing: {self.type} ["
        for i in self.arcs:
            string += f"{i}, "
        return string[:-2] + "]"

class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token: Token = None
        self.cursor = -1
        self.state = 0
        self.var_dict = {
            'place': list(),
            'tran': list()
        }

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

    def expect(self, token):
        temp = self.current_token.type
        if self.next_token().type in token:
            pass
        else:
            error(f"Expected something else after {temp}.")

    def case(self, state=None, token=None):
        if state != None:
            if self.state == state:
                pass
            else:
                return False
        if token != None:
            if self.current_token.type in token:
                pass
            else:
                return False
        return True

    def var_exists(self):
        if self.current_token.value in self.var_dict['place'] or self.current_token.value in self.var_dict['tran']:
            error(f"Identifier {self.current_token.value} already exists.")

    def var_not_exist(self):
        if self.current_token.value not in self.var_dict['place'] and self.current_token.value not in self.var_dict['tran']:
            error(f"Identifier {self.current_token.value} does not exist.")

    def parsify(self):
        self.declaration_list: list = list()
        self.state = 0
        while self.next_token().type != token.TT_EOF:

            if self.case(0, token.TT_DATATYPE):
                type = self.current_token.value
                varlist = list()

                while self.next_token():

                    if self.case(0, token.TT_VAR):
                        self.state = 1
                        self.var_exists()
                        varlist.append(self.current_token.value)
                    elif self.case(1, token.TT_COMMA):
                        self.state = 0
                    elif self.case(1, token.TT_SEMICOLON):
                        self.state = 0
                        self.declaration_list.append(Instantiation(type, varlist))
                        self.var_dict[type] += varlist
                        break
                    
                    else:
                        error("Instantiation Error")

            elif self.case(0, token.TT_VAR):

                temp = self.current_token.value
                self.var_not_exist()
                self.expect(token.TT_DOT)
                self.expect(token.TT_KEYWORD)


                if self.current_token.value in ["amm", "cap"]:
                    type = self.current_token.value
                    self.state = 1
                elif self.current_token.value == "in" and temp in self.var_dict['place']:
                    type = "outbound"
                    self.state = 2
                    swap = True
                elif self.current_token.value == "out" and temp in self.var_dict['tran']:
                    type = "outbound"
                    self.state = 2
                    swap = False
                elif self.current_token.value == "in" and temp in self.var_dict['tran']:
                    type = "inbound"
                    self.state = 2
                    swap = True
                elif self.current_token.value == "out" and temp in self.var_dict['place']:
                    type = "inbound"
                    self.state = 2
                    swap = False

                else:
                    error(
                        f"Field Declaration Error. Expected something else after {temp} instead of {self.current_token.value}.")

                self.expect(token.TT_EQUAL)
                self.next_token()

                if self.case(1, token.TT_NUMBER):
                    val = int(self.current_token.value)
                    self.expect(token.TT_SEMICOLON)
                    self.state = 0
                    self.declaration_list.append(Placefield(type, temp, val))

                elif self.case(2, token.TT_LBRACKET):
                    self.state = 1
                    arclist = list()

                    while self.next_token():

                        if self.case(1, token.TT_VAR):
                            self.var_not_exist()
                            self.state = 2
                            destination = self.current_token.value
                            val = 1

                        elif self.case(2, token.TT_COLON):
                            self.expect(token.TT_NUMBER)
                            val = int(self.current_token.value)

                        elif self.case(2, [token.TT_COMMA, token.TT_RBRACKET]):
                            self.state = 1
                            if swap:
                                arclist.append(Arc(destination, temp, val))
                            else:
                                arclist.append(Arc(temp, destination, val))
                            if self.case(token=token.TT_RBRACKET):
                                self.state = 0
                                break

                        else:
                            error("Arcing Declaration Error.")

                    self.expect(token.TT_SEMICOLON)
                    self.declaration_list.append(Arcing(type, list(arclist)))

                else:
                    error("Field Declaration Error. Expected something else after '='.")
            else:
                error()
        return self.declaration_list

    def build_AST(self):
        place = dict()
        places_amm = 0
        tran = dict()
        trans_amm = 0
        arc_in = []
        arc_out = []
        for declaration in self.declaration_list:

            if declaration.type == "place":
                for var in declaration.varlist:
                    temp_dict = {
                        "var": var,
                        "ID": places_amm,
                        "amm": 0,
                        "cap": float("inf")
                    }
                    place[var] = temp_dict
                    places_amm += 1

            elif declaration.type == "tran":
                for var in declaration.varlist:
                    temp_dict = {
                        "var": var,
                        "ID": trans_amm
                    }
                    tran[var] = temp_dict
                    trans_amm += 1

            elif type(declaration) == Placefield:
                place[declaration.var][declaration.type] = declaration.val

            elif declaration.type == "inbound":
                for arc in declaration.arcs:
                    temp_source = {
                        "var": arc.source,
                        "ID": place[arc.source]["ID"]
                    }
                    temp_destination = {
                        "var": arc.destination,
                        "ID": tran[arc.destination]["ID"]
                    }
                    arc_in.append([temp_source, temp_destination, arc.val])
            
            elif declaration.type == "outbound":
                for arc in declaration.arcs:
                    temp_source = {
                        "var": arc.source,
                        "ID": tran[arc.source]["ID"]
                    }
                    temp_destination = {
                        "var": arc.destination,
                        "ID": place[arc.destination]["ID"]
                    }
                    arc_out.append([temp_source, temp_destination, arc.val])
        return {
            "place": place,
            "tran": tran,
            "arc_in": arc_in,
            "arc_out": arc_out,
        }