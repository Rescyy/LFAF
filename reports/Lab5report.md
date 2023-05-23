# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Crucerescu Vladislav
### Variant: 9

----

## Abstract:

In this laboratory, I implement the Parser used in our DSL that I am working on with my team are for the PBL project. This Parser has been modified for this laboratory work, changed to work with the Lexer implemented in Lab 3. All the information about the lexer is in the lab 3 report, or previous commits of this repository.

## Theory:

The Parser is the software component of a programming language that is responsible for the analysis of the resulting tokens given by the lexer. A parser must be able to convert the tokens into an Abstract Syntax Tree (AST). It does that by obeying certain semantic rules given by the developer. Eventually, the AST will be used by the logic of the given Programming Language.

## Objectives:

1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description

__Declaration Classes__

There are 3 Declaration Type Classes, depending on the specific consecutive configuration of the tokens extracted. There are Instantiations, Placefields and Arcings. The classes made are built based on the following examples.
Instantiations: ```place p1, p2; tran t1, t2;```
Placefields: ```p1.amm = 3; p2.cap = 4;```
Arcings: ```t1.in = {p1:2}; t2.in = {p2};```

__Parser Class__

The Parser Class contains all the logic of the Parsing algorithm, it contains all the self Implemented Helper Functions and certain attributes for the analysis of the tokens, like the list of tokens, a current_token attribute, a cursor representing the position of the current_token, a state attribute that helps identify the correct consecutivity of the tokens and a variable dictionary containing 2 lists of the 2 variables types.

__Parsing Method__

The Parsing works by iterating through the token list and checking whether the token is valid or not, then based on the token received and a Finite Automaton structure implemented through the case() and expect() method, a respective declaration class will be produced and added to a new declaration_list list.

The following block of text, corresponds to the assigning of the corect attributes to an Instantiation Declaration Class depending on the received token. If the first token analyzed is a TT_DATATYPE, then it will be analyzed as an Instantiation. The type of the token is saved on the type variable and a varlist is created. Using a while loop calling the next_token method, multiple cases are presented using if elif method. When a token of type TT_VAR is identified, the value of it is added to a varlist.
The loop is broken when a SEMICOLON token is reached, respectively the varlist will be appended to the var_dict list of the respective type.

```
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
```

The following block of text, corresponds to the assigning of the corect attributes to a Placefield or a Arcing Declaration Class. The first token analyzed must be a TT_VAR type, then a TT_DOT and a TT_KEYWORD is expected with the expect() method. Last token analyzed being a TT_KEYWORD, can have as a value one of the following strings: "amm" and "cap" or "in" and "out", respectively a Placefield or an Arcing Class. 
A swap variable is set to True or False preparing the Arcing Declaration for the AST.

```
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
```

If the self.state attribute is 1, then the tokens are analyzed for a Placefield. Respectively, there should be a TT_NUMBER and a TT_SEMICOLON is expected right after. The token value is assigned to the Placefield class.

```
if self.case(1, token.TT_NUMBER):
    val = int(self.current_token.value)
    self.expect(token.TT_SEMICOLON)
    self.state = 0
    self.declaration_list.append(Placefield(type, temp, val))
```

Else if the self.state attribute is 2, then the tokens are analyzed for a Arcing. Respectively, there should be a TT_LBRACKET right after. Using a while loop, all the variables inside the brackets are analyzed using a Finite Automaton structure having the following rules, after TT_VAR, there can either follow TT_COLON, TT_COMMA or a TT_RBRACKET, after TT_COLON, there must be a TT_NUMBER, after TT_NUMBER there can either be a TT_COMMA or TT_RBRACKET, and so on. The variables are added to the arclist as an Arc object, having the source, destination and weight.

```
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
```

__Building AST__

After organising all the declarations in a list, we can proceed with building an AST out of them. Even though the declaration list can be regarded as an AST itself, we can organise the information in a dictionary structure datatype. The AST consists of a place, tran, arc_in, arc_out, places, trans subdictionaries. The place dictionary contains all the information about places, it being the name of the variable, the ID, the ammount of petri nets tokens it has and the maximum capacity. The tran dictionary contains all the information about transitions, variable name and ID. The arc_in and arc_out dictionaries contain all the declared inbound and outbound arcings, that contains information about the source, destination variables's names and IDs and the arcs' weight.

In the following code we add to the places subdictionary information about place instantiation. A places_amm variable helps to keep track of the variables' ID. Adding information to the tran subdictionary is exactly similar as for the place subdictionary, only has different variables.

```
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
```
```
elif declaration.type == "tran":
    for var in declaration.varlist:
        temp_dict = {
            "var": var,
            "ID": trans_amm
        }
        tran[var] = temp_dict
        trans_amm += 1
```

In case the declaration type is a placefield, it's easy to assign the capacity or ammount to the specified place using the already implemented dictionary.

```
elif type(declaration) == Placefield:
    place[declaration.var][declaration.type] = declaration.val
```

In the following code we add the information about the arcing. An arcing can be inbound or outbound depending on the first variable before the equal sign in the declaration. Using a for loop, we iterate through all Arc objects adding all the information necessary.

```
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
```
```
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
```

__Parsing Self Implemented Helper Functions__

The following method next_token(), iterates to the next token of the list, and assigns the self.current_token variable to the specified token. It then returns the token.

```
self.cursor += 1
self.current_token = self.tokens[self.cursor]
return self.current_token
```

The expect() method takes in as an argument a token, then it calls the next_token() method, and checks if it is equal to the argument. The temp variable saves the previous token type and is used in case of an error that is raised in case of falsity.

```
temp = self.current_token.type
if self.next_token().type in token:
    pass
else:
    error(f"Expected something else after {temp}.")
```

The case() method may take in an integer or a token variable. If given, it will compare the variable to the Parser class attribute, returning the respective boolean value.

```
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
```

The var_exists() and var_not_exist() methods are used to identify whether the current_token.value are in the respective var_dict sublist attribute of the Parser Class. A error is raised respectively in case the variable has been instantiated or was not.

```
if self.current_token.value in self.var_dict['place'] or self.current_token.value in self.var_dict['tran']:
    error(f"Identifier {self.current_token.value} already exists.")
```
```
if self.current_token.value not in self.var_dict['place'] and self.current_token.value not in self.var_dict['tran']:
    error(f"Identifier {self.current_token.value} does not exist.")
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
into a list of tokens
```
Tokens:
[DATATYPE : place][VAR : p1][COMMA][VAR : p2][SEMICOLON][DATATYPE : tran]
[VAR : t1][COMMA][VAR : t2][SEMICOLON][VAR : p1][DOT][KEYWORD : amm]
[EQUAL][NUMBER : 3][SEMICOLON][VAR : p2][DOT][KEYWORD : cap][EQUAL]
[NUMBER : 4][SEMICOLON][VAR : t1][DOT][KEYWORD : out][EQUAL][LBRACKET]
[VAR : p1][COLON][NUMBER : 2][COMMA][VAR : p2][RBRACKET][SEMICOLON]
[VAR : p1][DOT][KEYWORD : out][EQUAL][LBRACKET][VAR : t2][COLON][NUMBER : 5]
[RBRACKET][SEMICOLON][EOF]
```

The Parser will produce the following AST

```
{
   "place": {
      "p1": {
         "var": "p1",
         "ID": 0,
         "amm": 3,
         "cap": Infinity
      },
      "p2": {
         "var": "p2",
         "ID": 1,
         "amm": 0,
         "cap": 4
      }
   },
   "tran": {
      "t1": {
         "var": "t1",
         "ID": 0
      },
      "t2": {
         "var": "t2",
         "ID": 1
      }
   },
   "arc_in": [
      [
         {
            "var": "p1",
            "ID": 0
         },
         {
            "var": "t2",
            "ID": 1
         },
         5
      ]
   ],
   "arc_out": [
      [
         {
            "var": "t1",
            "ID": 0
         },
         {
            "var": "p1",
            "ID": 0
         },
         2
      ],
      [
         {
            "var": "t1",
            "ID": 0
         },
         {
            "var": "p2",
            "ID": 1
         },
         1
      ]
   ]
}
```

## Conclusion

In this laboratory work I implemented a Parser that can produce the AST given the Lexer from the previous laboratory 3. The Parser produces and AST of the form of a json string, or a python dictionary. The Parser has been implemented specifically for the Grammar of our DSL, it cannot be used unniversally with other Grammars. The Parser analyzes each token one after another and checks its validity like a Finite Automaton would, after each step adding corresponding information to the declaration.