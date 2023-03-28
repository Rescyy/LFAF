# Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Crucerescu Vladislav
### Variant: 9

----

## Abstract:

In this laboratory, I implemented implement a prototype lexer done for the DSL I am working on with my team for the PBL project. Our syntax is very similar to the syntax used in C/C++. This was the initial implementation for our lexer, though it has been modified for this laboratory work. Ultimately we chose to go with a different Lexer design.

## Theory:

The Lexer is the software component of a programming language that is responsible for the analysis of the code text. A lexer must be able to convert the code text into basic components called Tokens. It does that by obeying certain syntactic rules given by the developer. The Tokens will be analyzed by a Parser that builds the Abstract Syntax Tree from which a certain semantic meaning can be extracted.

## Objectives:

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description

__Tokens__

Tokens are implemented as an object class Token which have an attribute type and value. All tokens must have a type, but not all have an assigned value. For example a token of type VAR, must have a value that represents the given variable, but a token of type COLON does not need such a value.

In the following list are the implemented token types. Each type is assigned to a certain string constant.

```
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
```

__Lexer__

The Lexer uses two cursors and a while loop to iterate through the code text. The two cursors isolate parts of the code and analyze them through certain conditions. The second cursor is always equal or greater than the first cursor. Depending on what these cursors see, there are certain cases that may take place.

The following conditions state:

If cursor1 is equal to the length of the code text, then the lexer has scanned the whole text, it will append an End of File token to the token list and end the while loop.
```
if cursor2 == length:
    self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
    self.tokens.append(Token(TT_EOF))
    break
```

If cursor2 is equal to the length of the code text, then the lexer has scanned the whole text, though it must append the final sequence between cursor1 and cursor2, it will append an End of File token and end the while loop.

```
elif cursor2 == length:
    self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
    self.tokens.append(Token(TT_EOF))
    break
```

If cursor1 is either of the following characters, then the lexer will append the respective token of the character, cursor1 will iterate to the next character and cursor2 will be equal to cursor1. The reason why cursor2 is equal to cursor1, is because there might be cases where a character is skipped and an UNDEFINED token is produced.

```
elif self.code_text[cursor1] in '}{,:=.;':
    self.tokens.append(self.token_switch(self.code_text[cursor1]))
    cursor1 += 1
    cursor2 = cursor1
```

If cursor2 is either of the following characters, then the lexer will append the respective token of the character and of the character string between cursor1 and cursor2, cursor2 will be equal to the next character and cursor1 will be equal to cursor2.

```
elif self.code_text[cursor2] in '}{,:=.;':
    self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
    self.tokens.append(self.token_switch(self.code_text[cursor2]))
    cursor1 = cursor2 + 1
    cursor2 = cursor1
```

If cursor1 points to any kind of empty space, then cursor1 and cursor2 will point to their next respective character.

```
elif self.code_text[cursor1] in ' \t\r':
    cursor1 += 1
    cursor2 += 1
```

If cursor2 points to any kind of empty space, then the lexer will append the respective token of the character strings between cursor1 and cursor2, and cursor1 will be equal to cursor2.

```
elif self.code_text[cursor2] in ' \t\r':
    self.tokens.append(self.token_switch(self.code_text[cursor1:cursor2]))
    cursor1 = cursor2
```

If any of these conditions are not met, then cursor2 will point to the next character.

In the next method, the string is evaluated to its matching token. If the string is not contained in the token type dictionary, then it will be evaluated if it is a variable or a number, else it will be an UNDEFINED token.

```
if string not in TT_DICTIONARY:
    if self.var_identifier(string):
        return Token(TT_VAR, string)
    if self.number_identifier(string):
        return Token(TT_NUMBER, string)
    return Token(TT_UNDEFINED)
else:
    return TT_DICTIONARY[string]
```

The token type dictionary contains keywords and characters specific for the DSL. Given a valid key, it will return a Token specific for the key.

```
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
```

The variable identifier method checks if the first character is an alphabet letter (LETTERS), and then checks if the rest are valid characters (CHAR).

```
if string[0] not in LETTERS:
    return False
for char in string:
    if char not in CHARS:
        return False
return True
```

The number identifer method checks if the first character is not '0', and then checks if the rest are digits (DIGITS).

```
if string[0] == '0':
    return False
for char in string:
    if char not in DIGITS:
        return False
return True
```

The constants LETTERS, CHARS and DIGITS are defined as the following.

```  
DIGITS = '0123456789'
LETTERS = ascii_letters
CHARS = LETTERS + DIGITS + '_'
```

## Results

The Lexer will tokenize the following text code

```
place p1, p2;
tran t1, t2;
p1.amm= 3;
p2.cap = 4;
t1.out =   { p1 :  2, p2  }  ;
p1.out = {t2 : 5   }   ;
```
into an array of tokens
```
Tokens:
[DATATYPE : place][VAR : p1][COMMA][VAR : p2][SEMICOLON][DATATYPE : tran][VAR : t1][COMMA][VAR : t2][SEMICOLON][VAR : p1][DOT][KEYWORD : amm][EQUAL][NUMBER : 3][SEMICOLON][VAR : p2][DOT][KEYWORD : cap][EQUAL][NUMBER : 4][SEMICOLON][VAR : t1][DOT][KEYWORD : out][EQUAL][LBRACKET][VAR : p1][COLON][NUMBER : 2][COMMA][VAR : p2][RBRACKET][SEMICOLON][VAR : p1][DOT][KEYWORD : out][EQUAL][LBRACKET][VAR : t2][COLON][NUMBER : 5][RBRACKET][SEMICOLON][EOF]
```

## Conclusions

In this laboratory work, I implemented a Lexer for my PBL team's DSL. By using examples of the syntax, I had recognised what characters are being used, how do variables and numbers look and certain reoccuring keywords. I had to provide a method for classifying strings to their respective tokens, and correctly iterate through the code text to extract all the information necessary without any errors.