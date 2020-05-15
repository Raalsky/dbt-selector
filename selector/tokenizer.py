from ply import lex

fqn_prefix = r'((?P<fqn>[a-z]+)\:){0,1}'
identifier = r'(([_a-z0-9]+)|(\*))'
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
        'RPAREN'
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
