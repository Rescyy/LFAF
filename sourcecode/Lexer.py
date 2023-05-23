import token

class Lexer:

    def __init__(self, code_text: str):
        self.code_text = code_text.replace('\n', '')
        self.tokens = list()
        self.declaration_lexer()

    def __str__(self):
        string = ''
        for token in self.tokens:
            string += f"[{token}]"
        return string

    def var_identifier(self, string: str) -> bool:
        if string[0] not in token.LETTERS:
            return False
        for char in string:
            if char not in token.CHARS:
                return False
        return True

    def number_identifier(self, string: str) -> bool:
        if string[0] == '0':
            return False
        for char in string:
            if char not in token.DIGITS:
                return False
        return True

    def token_switch(self, string) -> token.Token:
        if string not in token.TT_DICTIONARY:
            if self.var_identifier(string):
                return token.Token(token.TT_VAR, string)
            if self.number_identifier(string):
                return token.Token(token.TT_NUMBER, string)
            return token.Token(token.TT_UNDEFINED)
        else:
            return token.TT_DICTIONARY[string]

    def declaration_lexer(self) -> None:
        length = len(self.code_text)
        cursor1, cursor2 = 0, 0
        while cursor2 <= length:
            if cursor1 == length:
                self.tokens.append(token.Token(token.TT_EOF))
                break
            elif cursor2 == length:
                self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
                self.tokens.append(token.Token(token.TT_EOF))
                break
            elif self.code_text[cursor1] in '}{,:=.;':
                self.tokens.append(self.token_switch(self.code_text[cursor1]))
                cursor1 += 1
                cursor2 = cursor1
            elif self.code_text[cursor2] in '}{,:=.;':
                self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
                self.tokens.append(self.token_switch(self.code_text[cursor2]))
                cursor1 = cursor2 + 1
                cursor2 = cursor1
            elif self.code_text[cursor1] in ' \t\r':
                cursor1 += 1
                cursor2 += 1
            elif self.code_text[cursor2] in ' \t\r':
                self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
                cursor1 = cursor2
            else:
                cursor2 += 1