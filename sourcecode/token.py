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