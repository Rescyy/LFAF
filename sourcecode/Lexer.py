from string import ascii_letters

DIGITS = '0123456789'
LETTERS = ascii_letters
CHARS = LETTERS + DIGITS + '_'

TT_LBRACKET  = 'LBRACKET'
TT_RBRACKET  = 'RBRACKET'
TT_KEYWORD   = 'KEYWORD'
TT_COMMA     = 'COMMA'
TT_DOT       = 'DOT'
TT_EQUAL     = 'EQUAL'
TT_COLON     = 'COLON'
TT_SEMICOLON = 'SEMICOLON'
TT_DATATYPE  = 'DATATYPE'
TT_VAR       = 'VAR'
TT_NUMBER    = 'NUMBER'
TT_UNDEFINED = 'UNDEFINED'
TT_EOF       = 'EOF'

class Token:
    def __init__(self, type: str, value: str = None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.value:
            return f'{self.type} : {self.value}'
        return f'{self.type}'

TT_DICTIONARY = {
    '{'    : Token(TT_LBRACKET),
    '}'    : Token(TT_RBRACKET),
    ','    : Token(TT_COMMA),
    '.'    : Token(TT_DOT),
    '='    : Token(TT_EQUAL),
    ':'    : Token(TT_COLON),
    ';'    : Token(TT_SEMICOLON),
    'place': Token(TT_DATATYPE, 'place'),
    'tran' : Token(TT_DATATYPE, 'tran'),
    'amm'  : Token(TT_KEYWORD, 'amm'),
    'cap'  : Token(TT_KEYWORD, 'cap'),
    'in'   : Token(TT_KEYWORD, 'in'),
    'out'  : Token(TT_KEYWORD, 'out'),
}

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
        if string[0] not in LETTERS:
            return False
        for char in string:
            if char not in CHARS:
                return False
        return True

    def number_identifier(self, string: str) -> bool:
        if string[0] == '0':
            return False
        for char in string:
            if char not in DIGITS:
                return False
        return True

    def token_switch(self, string) -> Token:
        if string not in TT_DICTIONARY:
            if self.var_identifier(string):
                return Token(TT_VAR, string)
            if self.number_identifier(string):
                return Token(TT_NUMBER, string)
            return Token(TT_UNDEFINED)
        else:
            return TT_DICTIONARY[string]

    def declaration_lexer(self) -> None:
        length = len(self.code_text)
        cursor1, cursor2 = 0, 0
        while cursor2 <= length:
            if cursor1 == length:
                self.tokens.append(Token(TT_EOF))
                break
            elif cursor2 == length:
                self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
                self.tokens.append(Token(TT_EOF))
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