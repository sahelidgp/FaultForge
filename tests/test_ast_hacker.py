import ast
from src.core.ast_hacker import OperatorMutator

def test_addition_mutation():
    # 1. Setup: A simple addition string
    source_code = "a + b"
    tree = ast.parse(source_code)
    
    # 2. Execute: Run our mutator
    mutator = OperatorMutator()
    mutated_tree = mutator.visit(tree)
    
    # 3. Assert: Check if it successfully changed to subtraction
    mutated_code = ast.unparse(mutated_tree).strip()
    assert mutated_code == "a - b"
    assert mutator.mutations_made == 1

def test_greater_than_mutation():
    source_code = "if x > 5: pass"
    tree = ast.parse(source_code)
    
    mutator = OperatorMutator()
    mutated_tree = mutator.visit(tree)
    
    mutated_code = ast.unparse(mutated_tree).strip()
    assert "x >= 5" in mutated_code
    assert mutator.mutations_made == 1