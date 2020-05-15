import sys
from ply import yacc
from selector import SelectorTokenizer
from selector.ast import *


class Grammar:
    tokens = SelectorTokenizer.tokens

    precedence = (
        ('left', 'INTERSECTION', 'CONCATENATION'),
        ('left', 'RELATED', 'AT'),
    )

    def p_expression_intersection(self, p):
        'expression : expression INTERSECTION expression'
        p[0] = IntersectionOperator(p[1], p[3])

    def p_expression_concatenation(self, p):
        'expression : expression CONCATENATION expression'
        p[0] = ConcatOperator(p[1], p[3])

    def p_expression_parents(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_parents(self, p):
        'term : RELATED term'
        p[0] = ParentsOp(p[2])

    def p_childrens(self, p):
        'term : term RELATED'
        p[0] = ChildrensOp(p[1])

    def p_expression_at(self, p):
        'term : AT term'
        p[0] = AtOp(p[2])

    def p_term(self, p):
        'term : resource'
        p[0] = p[1]

    def p_resource(self, p):
        'resource : RESOURCE'
        p[0] = Resource(p[1])

    def p_error(self, p):
        print(f"Syntax error in input: {p}")

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer or SelectorTokenizer()
        self.tokenizer.build()
        self.parser = yacc.yacc(module=self, write_tables=False, debug=True)

    def parse(self, data, **kwargs):
        return self.parser.parse(data, lexer=self.tokenizer.lexer, **kwargs)
