from Lexer import Lexer

example = """
place p1, p2;
tran t1, t2;
p1.amm= 3;
p2.cap = 4;
t1.out =   { p1 :  2, p2  }  ;
p1.out = {t2 : 5   }   ;
"""
lexer = Lexer(example)
print(lexer)