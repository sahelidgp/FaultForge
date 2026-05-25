import ast

class MutationDiscoverer(ast.NodeVisitor):
    def __init__(self):
        self.total_targets = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            self.total_targets += 1

    def visit_Compare(self, node):
        self.generic_visit(node)
        if node.ops and isinstance(node.ops[0], ast.Gt):
            self.total_targets += 1


class OperatorMutator(ast.NodeTransformer):
    def __init__(self, target_index):
        self.target_index = target_index
        self.current_index = 0
        self.mutated = False
        self.mutation_name = ""

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            if self.current_index == self.target_index:
                node.op = ast.Sub()
                self.mutated = True
                self.mutation_name = "Arithmetic: '+' to '-'"
            self.current_index += 1
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if node.ops and isinstance(node.ops[0], ast.Gt):
            if self.current_index == self.target_index:
                node.ops[0] = ast.GtE()
                self.mutated = True
                self.mutation_name = "Boundary: '>' to '>='"
            self.current_index += 1
        return node