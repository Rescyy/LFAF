# Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Crucerescu Vladislav
### Variant: 9

----

## Theory:
The Chomsky Normal Form is a grammar layout that has the following constraints:
1. __A -> a | BC__, where __a__ is a terminal symbol and __A__,__B__,__C__ are non terminal symbols;
2. __S -> ε__ is possible if and only if __S__ is the start symbol;
3. There are no unreachable symbols in the grammar.

The conversion of a grammar to chomsky normal form requires a number of manipulations of the grammar's transition set and non terminal symbols set. These manipulations will be further explained as steps in the implementation description.

## Objectives:
1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

__Chomsky Conversion Steps__

__Step 1. Adding a new start symbol__
In the following method, we add a new starting symbol derived from the initial one, and a respective unit transition in the transition set.
Having S as starting symbol, the symbol \<S> and the transition \<S> -> S is added.

```
first = grammar.non_terminal_chars[0]
grammar.non_terminal_chars.insert(0,f"<{first}>")
grammar.transition_set.append([f"<{first}>", first])
```

__Step 2. Remove null productions__
In the following method, we identify which non terminal symbol has a null production, and eliminate them from the grammar's transition set. If there are no such symbols, then the method will return.

```
null_symbols = []
while i < len(grammar.transition_set):
    if not grammar.transition_set[i][1] and grammar.transition_set[i][0] != grammar.non_terminal_chars[0]:
        null_symbols.append(grammar.transition_set.pop(i)[0])
    else:
        i += 1
if not null_symbols:
    return
```

Next, for the transitions containing at least one of the null symbols, there will be added all possible configurations of the positioning of the null symbol in the result string. For example, for _n_ occurences of the null symbol in the result string in the transition, there will be _2^n^_ ways of rewriting that result string, given we are able to take out the null symbol. The method truth_list is used to create all possible _2^n^_ configurations of the null symbol in the string, though only _2^n^-1_ are needed since there is already the initial transition. The first for loop iterates through the null_symbols list determined before. The second for loop iterates through the transition set and checks whether there are any null symbols in the result string. If yes, the result is split using the python method split, then using the method truth_list, all possible string configurations are built. Finally, the resulted string is added into a new_transitions list object. In case new null productions were added during the algorithm, it will recursively be called again.

```
for non_terminal in null_symbols:
    for init, result in grammar.transition_set:
        if non_terminal in result:
            results = result.split(non_terminal)
            bin_list = truth_list(len(results) - 1)
            for binary in bin_list:
                string = results[0]
                for i in range(len(binary)):
                    if binary[i]:
                        string += non_terminal
                    string += results[i+1]
                if [init, string] not in new_transitions and init not in null_symbols:
                    new_transitions.append([init, string])
    grammar.transition_set += new_transitions
self.remove_null_productions(grammar, i)
```

The following code is the method truth_list used previously. It creates a list of lists of boolean values. By using the python method bin that converts an integer to a binary string represenation, we easily create all the configurations necessary.
```
if a == 1:
    return [[0]]
b = a**2
c = 0
truth_list = []
for _ in range(b-1):
    str = bin(c)[2:]
    truth_list.append([int(i) for i in list('0'*(a-len(str)) + str)])
    c += 1
```

__Step 3. Remove unit productions__

The following method searches for transitions of the form _A->B_ where _A_,_B_ are non terminal symbols. It deletes the transition and adds new transitions _A->α~1~|...|α~n~_ for all transitions 
_B->α~1~|...|α~n~_, where _α~n~_ is a result string. All new transitions are added to the bottom of the transition set, therefore can be evaluated again in case themselves are unit productions.

```
while i < len(grammar.transition_set):
    if grammar.transition_set[i][1] in grammar.non_terminal_chars:
        transition = grammar.transition_set.pop(i)
        for init, result in grammar.transition_set:
            if transition[1] == init and [transition[0], result] not in grammar.transition_set:
                grammar.transition_set.append([transition[0], result])
    else:
        i += 1
```

__Step 4. Reduce large results__

The following method searches for result strings that have more than 2 characters using the no_symbols method. Once finding one, it appends a multitude of new symbols of the form \<Xn> in the non terminal characters set, where n is an assigned index, and appends transitions mimicking the production. A new_symbols value must be used in order to keep track of the amount of new states added.

```
while i < len(grammar.transition_set):
    if grammar.no_symbols(grammar.transition_set[i][1]) > 2:
        symbols = grammar.split_string(grammar.transition_set[i][1])
        init = grammar.transition_set.pop(i)[0]
        grammar.transition_set.append([init, f"{symbols[0]}<X{id_maker(new_symbols)}>"])
        grammar.non_terminal_chars.append(f"<X{id_maker(new_symbols)}>")
        for j in range(1,len(symbols)-2):
            grammar.transition_set.append([f"<X{id_maker(new_symbols)}>", f"{symbols[j]}<X{id_maker(new_symbols+1)}>"])
            new_symbols += 1
            grammar.non_terminal_chars.append(f"<X{id_maker(new_symbols)}>")
        grammar.transition_set.append([f"<X{id_maker(new_symbols)}>", f"{symbols[-2]}{symbols[-1]}"])
        new_symbols += 1
    else:
        i += 1
```

The grammar no_symbols method counts the ammount of symbols in a string given the grammar it originates from. First it counts each non terminal symbol and removes them, the rest are the terminal characters that will not create ambiguity with the non terminal symbols.

```
for i in self.non_terminal_chars:
    no += string.count(i)
    string = string.replace(i, '')
for i in self.terminal_chars:
    no += string.count(i)
```

The grammar split_string method, splits the result string into a list of symbols. By iterating using 2 cursors, it scans the string for terminal and non terminal characters.

```
i,j = 0,1
symbols = []
while j <= len(string):
    if string[i:j] in self.terminal_chars or string[i:j] in self.non_terminal_chars:
        symbols += [string[i:j]]
        i = j
    j += 1
```

The method id_maker takes in two integers, one being the string it will output and one the length of the string. For example it takes in 45 and 3, the string outputted will be 045, this is to avoid as much ambiguity as possible between states like X1 and X12.

__Step 5. Change productions__

The following method looks for transitions of the form _A->aB_ and _A->Ba_. Once it finds one, it removes it and adds the transitions _A->\<Yn>B_ and _\<Yn>->a_. It converts the terminal part into a transition. It also appends the corresponding symbols for \<Yn> to the non terminal set.

```
for char in grammar.terminal_chars:
    grammar.transition_set.append([f"<Y{id_maker(new_symbols)}>", char])
    grammar.non_terminal_chars.append(f"<Y{id_maker(new_symbols)}>")
    new_symbols += 1
for i in range(len(grammar.transition_set)):
    if grammar.transition_set[i][0] != grammar.non_terminal_chars[0] or len(grammar.transition_set[i][1]) != 0:
        if grammar.transition_set[i][1][0] in grammar.terminal_chars and len(grammar.transition_set[i][1]) != 1:
            grammar.transition_set[i][1] = f"<Y{id_maker(grammar.terminal_chars.index(grammar.transition_set[i][1][0]))}>{grammar.transition_set[i][1][1:]}"
        if grammar.transition_set[i][1][-1] in grammar.terminal_chars and len(grammar.transition_set[i][1]) != 1:
            grammar.transition_set[i][1] = f"{grammar.transition_set[i][1][:-1]}<Y{id_maker(grammar.terminal_chars.index(grammar.transition_set[i][1][-1]))}>"
```

__Step 6. Remove unreachable symbols__

The following method checks which symbols are not reachable and eliminates their corresponding transitions and sets. By iterating through the transition set, it removes all reachable symbols from a copied list of the non terminal set without the start ssymbol. The ones that remain are the unreachable symbols, we therefore remove them.

```
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
```

## Results

The variant 9 grammar is:

```
Vn = ['S', 'A', 'B', 'C', 'D']
Vt = ['a', 'b']
P = [
    ['S', 'bA'],
    ['S', 'BC'],
    ['A', 'a'],
    ['A', 'aS'],
    ['A', 'bAaAb'],
    ['B', 'A'],
    ['B', 'bS'],
    ['B', 'aAa'],
    ['C', ''],
    ['C', 'AB'],
    ['D', 'AB']
]
```

Using my implemented method for chomsky normalization, we obtain the following grammar.

```
    Vn = ['<S>', 'S', 'A', 'B', 'C', '<X00>', '<X01>', '<X02>', '<X03>',
    '<X04>', '<X05>', '<X06>', '<X07>', '<X08>', '<X09>', '<X10>', '<X11>',
    '<X12>', '<X13>', '<X14>', '<Y00>', '<Y01>'],
    Vt = ['a', 'b'],
    P = [
        ['S', '<Y01>A'],
        ['S', 'BC'],
        ['A', 'a'],
        ['A', '<Y00>S'],
        ['B', '<Y01>S'],
        ['C', 'AB'],
        ['B', 'a'],
        ['B', '<Y00>S'],
        ['<S>', '<Y01>A'],
        ['<S>', 'BC'],
        ['S', '<Y01>S'],
        ['S', 'a'],
        ['S', '<Y00>S'],
        ['<S>', '<Y01>S'],
        ['<S>', 'a'],
        ['<S>', '<Y00>S'],
        ['A', '<Y01><X00>'],
        ['<X00>', 'A<X01>'],
        ['<X01>', '<Y00><X02>'],
        ['<X02>', 'A<Y01>'],
        ['B', '<Y00><X03>'],
        ['<X03>', 'A<Y00>'],
        ['B', '<Y01><X04>'],
        ['<X04>', 'A<X05>'],
        ['<X05>', '<Y00><X06>'],
        ['<X06>', 'A<Y01>'],
        ['S', '<Y00><X07>'],
        ['<X07>', 'A<Y00>'],
        ['S', '<Y01><X08>'],
        ['<X08>', 'A<X09>'],
        ['<X09>', '<Y00><X10>'],
        ['<X10>', 'A<Y01>'],
        ['<S>', '<Y00><X11>'],
        ['<X11>', 'A<Y00>'],
        ['<S>', '<Y01><X12>'],
        ['<X12>', 'A<X13>'],
        ['<X13>', '<Y00><X14>'],
        ['<X14>', 'A<Y01>'],
        ['<Y00>', 'a'],
        ['<Y01>', 'b'],
    ]
```

I implemented the unit test to verify whether this grammar is a chomsky normal form, by checking if the grammar follows the chomsky normal form constraints.

```
grammar = Grammar(V_N, V_T, Prod)
grammar = ChomskyNormalFormConvertor().get_chomsky_normal_form(grammar)
for init, result in grammar.transition_set:
    self.assertTrue(init in grammar.non_terminal_symbols)
    num = grammar.no_symbols(result)
    self.assertTrue(0 <= num <= 2, f"{[init,result]} Production: {grammar.transition_set.index([init, result])}")
    if num == 0:
        self.assertTrue(init == grammar.non_terminal_symbols[0])
    if num == 1:
        self.assertTrue(result in grammar.terminal_symbols)
    if num == 2:
        elements = grammar.split_string(result)
        self.assertTrue(elements[0] in grammar.non_terminal_symbols and elements[1] in grammar.non_terminal_symbols,
                        f"{[init,result]} Production: {grammar.transition_set.index([init, result])}")
```

For checking whether the conversion will be succesful for other grammars, I introduced the DSL grammar used for my ELSD project, and normalised it. As expected, it passes all the unit tests written.

```
V_N = [
    "<program>",
    "<declarationlist>",
    "<declaration>",
    "<instantiation>",
    "<placefield>",
    "<connection>",
    "<type>",
    "<varlist>",
    "<var>",
    "<number>",
    "<arcing>",
    "<arclist>",
    "<arc>",
    "<nonzero>",
    "<digits>",
    "<digit>",
    "<alpha>",
    "<string>",
    "<char>"
]
V_T = list(string.ascii_letters + '1234567890_.,:}{=; ')
Prod = [
    ["<program>", "<declarationlist>"],
    ["<declarationlist>","<declaration>;<declarationlist>"],
    ["<declarationlist>",""],
    ["<declaration>","<instantiation>"],
    ["<declaration>","<placefield>"],
    ["<declaration>","<arcing>"],
    ["<instantiation>","<type> <varlist>"],
    ["<type>", "place"],
    ["<type>", "tran"],
    ["<placefield>", "<var>.amm=<number>"],
    ["<placefield>", "<var>.cap=<number>"],
    ["<arcing>", "<var>.in={<arclist>"],
    ["<arcing>", "<var>.out={<arclist>"],
    ["<arclist>", "<arc>, <arclist>"],
    ["<arclist>", "<arc>}"],
    ["<arc>", "<var>:<number>"],
    ["<arc>", "<var>"],
    ["<number>", "<nonzero><digits>"],
    ["<digits>", "<digit><digits>"],
    ["<digits>", ""],
    ["<digit>", "0"],
    ["<digit>", "<nonzero>"]] + [
    ["<nonzero>", str(i)] for i in range(1,10)] + [
    ["<varlist>", "<var>,<varlist>"],
    ["<varlist>", "<var>"],
    ["<var>", "<alpha><string>"],
    ["<string>", "<char><string>"],
    ["<string>", ""],
    ["<char>", "_"],
    ["<char>", "<digit>"],
    ["<char>", "<alpha>"]] + [
    ["<alpha>", i] for i in string.ascii_letters
    ]
```
```
test_check_DSL_normal_form_conversion (__main__.GrammarTests) ... ok
test_check_grammar_variant9_normal_form_conversion (__main__.GrammarTests) ... ok
test_grammar_variant9 (__main__.GrammarTests) ... ok
```

## Conclusion

In this laboratory work I implemented the algorithm for converting a grammar to chomsky normal form. There are several steps to the algorithm and the easiest way to do it was to tackle each step separately. For some steps recursion was used, though I realised later that a better approach could be used. Before adding any new transitions, we must be careful to not create any repeating transitions. Also, using the string as literal strings objects proved to be difficult, because I had to always implement some sort of avoiding ambiguity, count elements, though it was easy to use integrated python functions.