#LAB 4 LFAF
#Name: Crucerescu Vladislav
#Group: FAF-212
#Variant: 9

import string
from grammar import Grammar
from chomsky import ChomskyNormalFormConvertor
import unittest

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

grammar = Grammar(Vn, Vt, P)
chomsky = ChomskyNormalFormConvertor()
# print(chomsky.get_chomsky_normal_form(grammar))

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

petri_nets_grammar = Grammar(V_N, V_T, Prod)
# print(petri_nets_grammar)
# normalised_petri_nets_grammar = chomsky.get_chomsky_normal_form(petri_nets_grammar)

class GrammarTests(unittest.TestCase):

    def test_grammar_variant9(self):
        grammar = Grammar(
            Vn = ['S', 'A', 'B', 'C', 'D'],
            Vt = ['a', 'b'],
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
        )
        chomsky.start(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', 'D'],
            "start Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
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
                ['D', 'AB'],
                ['<S>', 'S']
            ]
            ,"start P"
        )
        chomsky.remove_null_productions(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', 'D'],
            "remove_null_productions Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
                ['S', 'bA'],
                ['S', 'BC'],
                ['A', 'a'],
                ['A', 'aS'],
                ['A', 'bAaAb'],
                ['B', 'A'],
                ['B', 'bS'],
                ['B', 'aAa'],
                ['C', 'AB'],
                ['D', 'AB'],
                ['<S>', 'S'],
                ['S', 'B']
            ],
            "remove_null_productions P"
        )
        chomsky.remove_unit_productions(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', 'D'],
            "remove_unit_productions Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
                ['S', 'bA'],
                ['S', 'BC'],
                ['A', 'a'],
                ['A', 'aS'],
                ['A', 'bAaAb'],
                ['B', 'bS'],
                ['B', 'aAa'],
                ['C', 'AB'],
                ['D', 'AB'],
                ['B', 'a'],
                ['B', 'aS'],
                ['B', 'bAaAb'],
                ['<S>', 'bA'],
                ['<S>', 'BC'],
                ['S', 'bS'],
                ['S', 'aAa'],
                ['S', 'a'],
                ['S', 'aS'],
                ['S', 'bAaAb'],
                ['<S>', 'bS'],
                ['<S>', 'aAa'],
                ['<S>', 'a'],
                ['<S>', 'aS'],
                ['<S>', 'bAaAb']
            ],
            "remove_unit_productions P"
        )
        chomsky.reduce_large_results(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', 'D', '<X00>',
             '<X01>', '<X02>', '<X03>', '<X04>', '<X05>',
             '<X06>', '<X07>', '<X08>', '<X09>', '<X10>',
             '<X11>', '<X12>', '<X13>', '<X14>'],
            "reduce_large_results Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
                ['S', 'bA'],
                ['S', 'BC'],
                ['A', 'a'],
                ['A', 'aS'],
                ['B', 'bS'],
                ['C', 'AB'],
                ['D', 'AB'],
                ['B', 'a'],
                ['B', 'aS'],
                ['<S>', 'bA'],
                ['<S>', 'BC'],
                ['S', 'bS'],
                ['S', 'a'],
                ['S', 'aS'],
                ['<S>', 'bS'],
                ['<S>', 'a'],
                ['<S>', 'aS'],
                ['A', 'b<X00>'],
                ['<X00>', 'A<X01>'],
                ['<X01>', 'a<X02>'],
                ['<X02>', 'Ab'],
                ['B', 'a<X03>'],
                ['<X03>', 'Aa'],
                ['B', 'b<X04>'],
                ['<X04>', 'A<X05>'],
                ['<X05>', 'a<X06>'],
                ['<X06>', 'Ab'],
                ['S', 'a<X07>'],
                ['<X07>', 'Aa'],
                ['S', 'b<X08>'],
                ['<X08>', 'A<X09>'],
                ['<X09>', 'a<X10>'],
                ['<X10>', 'Ab'],
                ['<S>', 'a<X11>'],
                ['<X11>', 'Aa'],
                ['<S>', 'b<X12>'],
                ['<X12>', 'A<X13>'],
                ['<X13>', 'a<X14>'],
                ['<X14>', 'Ab']
            ],
            "reduce_large_results P"
        )
        chomsky.change_productions(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', 'D', '<X00>',
             '<X01>', '<X02>', '<X03>', '<X04>', '<X05>',
             '<X06>', '<X07>', '<X08>', '<X09>', '<X10>',
             '<X11>', '<X12>', '<X13>', '<X14>', '<Y00>',
             '<Y01>'],
            "change_productions Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
                ['S', '<Y01>A'],
                ['S', 'BC'],
                ['A', 'a'],
                ['A', '<Y00>S'],
                ['B', '<Y01>S'],
                ['C', 'AB'],
                ['D', 'AB'],
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
                ['<Y01>', 'b']
            ],
            "change_productions P"
        )
        chomsky.remove_questionable_results(grammar)
        self.assertEqual(
            grammar.non_terminal_symbols,
            ['<S>', 'S', 'A', 'B', 'C', '<X00>', '<X01>',
             '<X02>', '<X03>', '<X04>', '<X05>', '<X06>',
             '<X07>', '<X08>', '<X09>', '<X10>', '<X11>',
             '<X12>', '<X13>', '<X14>', '<Y00>', '<Y01>'],
            "remove_questionable_results Vn"
        )
        self.assertEqual(
            grammar.transition_set,
            [
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
                ['<Y01>', 'b']
            ],
            "remove_questionable_results P"
        )

    def test_check_grammar_variant9_normal_form_conversion(self):
        grammar = Grammar(Vn, Vt, P)
        grammar = ChomskyNormalFormConvertor().get_chomsky_normal_form(grammar)
        for init, result in grammar.transition_set:
            self.assertTrue(init in grammar.non_terminal_symbols)
            num = grammar.no_symbols(result)
            self.assertTrue(1 <= num <= 2, f"{[init,result]} Production: {grammar.transition_set.index([init, result])}")
            if num == 1:
                self.assertTrue(result in grammar.terminal_symbols)
            if num == 2:
                elements = grammar.split_string(result)
                self.assertTrue(elements[0] in grammar.non_terminal_symbols and elements[1] in grammar.non_terminal_symbols,
                                f"{[init,result]} Production: {grammar.transition_set.index([init, result])}")

    def test_check_DSL_normal_form_conversion(self):
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

unittest.main()