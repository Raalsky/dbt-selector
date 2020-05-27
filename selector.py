import sys
from ply import yacc, lex


fqn_prefix = r'((?P<fqn>[a-z]+)\:){0,1}'
identifier = r'(([a-z][_a-z0-9]*)|(\*))'
dotted = r'((' + identifier + ')(\.){0,1})*(' + identifier + r')'
resource_spec = r'(?P<resource>(' + dotted + r'))'
resource = r'(' + fqn_prefix + resource_spec + r')'

class SelectorTokenizer:
    tokens = (
        'RESOURCE',
        'RELATED',
        'INTERSECTION',
        'CONCATENATION',
        'AT',
        'LPAREN',
        'RPAREN',
        'NUMBER'
    )

    t_RELATED = r'\+'
    t_INTERSECTION = r'\,'
    t_CONCATENATION = r'\ '
    t_AT = r'\@'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    @lex.TOKEN(resource)
    def t_RESOURCE(self, token):
        token.value = (
            self.lexer.lexmatch.group('fqn'),
            self.lexer.lexmatch.group('resource')
            )
        return token

    def t_NUMBER(self, token):
        r'[0-9]+'
        token.value = int(token.value)
        return token

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore  = '\t'

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self,data):
        self.lexer.input(data)

        for token in self.lexer:
            yield token


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

    def p_parents_number(self, p):
        'term : NUMBER RELATED term'
        p[0] = ParentsOp(p[3], p[1])

    def p_childrens(self, p):
        'term : term RELATED'
        p[0] = ChildrensOp(p[1])

    def p_childrens_number(self, p):
        'term : term RELATED NUMBER'
        p[0] = ChildrensOp(p[1], p[3])

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
        self.parser = yacc.yacc(module=self, write_tables=False, debug=False)

    def parse(self, data, **kwargs):
        return self.parser.parse(data, lexer=self.tokenizer.lexer, **kwargs)


class Expression:
    pass


class Resource(Expression):
    def __init__(self, resource):
        self.type = 'resource'
        self.fqn = resource[0] or 'model'
        self.value = resource[1]

    def __repr__(self):
        return f"<{self.fqn}>:{self.value}"


class UnaryOperator(Expression):
    def __init__(self, type, inner):
        self.type = type
        self.inner = inner

    def __repr__(self):
        return f"{self.type}({self.inner})"


class ParentsOp(UnaryOperator):
    def __init__(self, inner, max_edges: int = -1):
        super(ParentsOp, self).__init__('parents', inner)
        self.max_edges = max_edges

    def __repr__(self):
        return f"{self.type}[{self.max_edges}]({self.inner})"


class ChildrensOp(UnaryOperator):
    def __init__(self, inner, max_edges: int = -1):
        super(ChildrensOp, self).__init__('childrens', inner)
        self.max_edges = max_edges

    def __repr__(self):
        return f"{self.type}[{self.max_edges}]({self.inner})"


class AtOp(UnaryOperator):
    def __init__(self, inner):
        super(AtOp, self).__init__('at', inner)


class SetBinaryOperator(Expression):
    def __init__(self, left, operator, right):
        self.type = 'set_binary_operator'
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"{self.operator}({self.left}, {self.right})"

class ConcatOperator(SetBinaryOperator):
    def __init__(self, left, right):
        super(ConcatOperator, self).__init__(left, 'concat', right)
        self.type = 'concat'

class IntersectionOperator(SetBinaryOperator):
    def __init__(self, left, right):
        super(IntersectionOperator, self).__init__(left, 'intersection', right)
        self.type = 'intersection'
