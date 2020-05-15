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
