from typing import Optional
import ast
import re
import os
import decimal
from typing import Optional, Union, Any


class OptimizationTransformer(ast.NodeTransformer):

    def visit_ListComp(self, node):
        return ast.GeneratorExp(node.elt, node.generators)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'range':
            node.func.id = 'xrange'
        return node

    def visit_Membership(self, node):
        if isinstance(node.container, (ast.List, ast.Tuple)):
            node.container = ast.Set(node.container.elts)
        return node

    def visit_For(self, node):
        if isinstance(node.body[0], ast.Assign) and isinstance(node.body[0].value, ast.BinOp) and isinstance(node.body[0].value.op, ast.Add):
            return ast.ListComp(ast.BinOp(node.body[0].value.left, node.body[0].value.op, node.body[0].value.right), [ast.comprehension(node.target, node.iter)])
        else:
            return node

    def optimize_varname(self, node):
        if isinstance(node, ast.Name):
            node.id = f'_{hash(node.id) % (10 ** 8)}'
        return node

    def optimize_constant(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            node.value = round(node.value, 2)
        return node

    def optimize_binop(self, node):
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            node.left = self.optimize_constant(node.left)
            node.right = self.optimize_constant(node.right)
        return node

    def optimize_comparison(self, node, decimal_places=2):
        if not isinstance(node, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)):
            return node

        if not hasattr(node, 'left') or not hasattr(node, 'right'):
            return node

        if not isinstance(node.left.value, (int, float, str)) or not isinstance(node.right.value, (int, float, str)):
            return node

        if not isinstance(node.left, ast.Constant) or not isinstance(node.right, ast.Constant):
            return node

        left_value = str(node.left.value) if not isinstance(
            node.left.value, str) else node.left.value
        right_value = str(node.right.value) if not isinstance(
            node.right.value, str) else node.right.value

        context = decimal.Context(precision=decimal_places)
        node.left.value = decimal.Decimal(left_value).quantize(context)
        node.right.value = decimal.Decimal(right_value).quantize(context)

        return node

    def optimize_funcname(self, node, prefix='my_prefix_', suffix=''):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            node.id = f'{prefix}{node.id}{suffix}'
        return node

    def optimize_string(self, node, compress=False):
        if isinstance(node, ast.Str):
            s = node.s.replace('\n', ' ')
            if compress:
                s = s.replace(' ', '')
            node.s = s
        return node

    def optimize_comment(self, node, max_length=80):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            comment = node.value.value.replace('\n', ' ').strip()
            if len(comment) > max_length:
                comment = ' '.join([comment[i:i+max_length]
                                    for i in range(0, len(comment), max_length)])
            node.value.value = comment
        return node

    def optimize_import(self, node):
        if isinstance(node, ast.Import):
            names_set = {alias.name for alias in node.names}
            node.names = [
                alias for alias in node.names if alias.name in names_set]
            if len(node.names) > 0:
                node = ast.ImportFrom(module=node.module,
                                      names=node.names, level=node.level)
        return node

    def generic_visit(self, node):
        node = self.optimize_varname(node)
        node = self.optimize_constant(node)
        node = self.optimize_binop(node)
        node = self.optimize_comparison(node)
        node = self.optimize_funcname(node)
        node = self.optimize_string(node)
        node = self.optimize_comment(node)
        node = self.optimize_import(node)
        super(OptimizationTransformer, self).generic_visit(node)


def condense_code(code: str, write_to_file: str) -> None:
    code = re.sub(r'\s*#.*', '', code)
    code = re.sub(r'\n\s+', '\n', code)
    code = re.sub(r'\s{2,}', ' ', code)
    tree = ast.parse(code)
    tree = OptimizationTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    condensed_code = ast.unparse(tree).encode('utf-8')
    if os.path.exists(write_to_file):
        with open(write_to_file, 'wb') as file:
            file.write(condensed_code)
    else:
        with open(write_to_file, 'xb') as file:
            file.write(condensed_code)


def condense_file(filepath: str) -> None:
    with open(filepath, 'r') as file:
        code = file.read()
    write_to_file = f'{filepath}.condensed'
    condense_code(code, write_to_file=write_to_file)


def condense_script(code_or_file: Union[str, IO], write_to_file: str = "condensed_code.py") -> None:
    if isinstance(code_or_file, str):
        with open(code_or_file, 'r') as file:
            code = file.read()
    else:
        code = code_or_file.read()
    condense_code(code, write_to_file=write_to_file)
