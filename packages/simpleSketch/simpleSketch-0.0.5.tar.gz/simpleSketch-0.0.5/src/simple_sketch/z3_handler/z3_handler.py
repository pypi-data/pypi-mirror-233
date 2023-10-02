"""
file: z3_handler.py
This module contains the Z3Handler class, which is responsible for handling the interaction with Z3.
"""


from typing import Callable, Dict, List, Set, Any, Tuple
import z3


from simple_sketch.utilities import Colors, cprint

#TODO: Add to Log file



Z3_TYPE = {
    'int': lambda name: z3.Int(name),
    'bool': lambda name:z3.Bool(name),
    'float': lambda name:z3.Real(name),
    'int_val': lambda val:z3.IntVal(val),
    'float_val': lambda val:z3.RealVal(val),
    'bool_val': lambda val: z3.BoolVal(val),
    'Array int': lambda name: z3.Array(name, z3.IntSort(), z3.IntSort()),
    'Array bool': lambda name: z3.Array(name, z3.BoolSort(), z3.BoolSort())
}


"""Map from type to the function that creates a z3 value of that type."""
Z3_VAL = {
    'int': lambda val: z3.IntVal(val),
    'int_val': lambda val: z3.IntVal(val),
    'float': lambda val: z3.RealVal(val),
    'float_val': lambda val: z3.RealVal(val),
    'bool': lambda val: z3.BoolVal(val),
    'bool_val': lambda val: z3.BoolVal(val),
    'Array int': lambda val: z3.K(z3.IntSort(), val),
    'Array int_val': lambda val: z3.K(z3.IntSort(), val),
    'Array bool': lambda val: z3.K(z3.BoolSort(), val),
    'Array bool_val': lambda val: z3.K(z3.BoolSort(), val),
}



def print_z3(formula, name:str | None = None):
    if name is not None:
        print(Colors.BLUE,f">>> {name}",Colors.RESET)
    import html
    z3.set_html_mode(True)
    print(Colors.BLUE,f">>> {html.unescape(str(formula))}",Colors.RESET)
    z3.set_html_mode(False)
    
def substitute_z3(formula, subs: List):
    """
        substitute_z3
        -------------
        Substitute the variables in the formula with the values in the list of tuples.
        For example, if the formula is `x == y`, and the list of tuples is `[(x, 1), (y, 2)]`, then the result is `1 == 2`.

        Args:
            formula (z3.BoolRef): A Z3 formula.
            subs (List): A list of tuples. Each tuple is a variable and its value.

        Returns:
            z3.BoolRef: A Z3 formula with the variables substituted.
    """
    #TODO: check if this is enough
    #z3.substitute_vars()

    # fix the subs when we have a substitution of the form (x, 1), we need to convert `1` to `z3.IntVal(1)`
    for i, (x, y) in enumerate(subs):
        # TODO: check if this is should be `int` or `float`
        if isinstance(y, int):
            # subs[i] = (x, z3.IntVal(y))
            subs[i] = (x, z3.IntVal(y))
    new_formula = z3.substitute(formula, *subs) # z3.substitute_vars()?
    return new_formula


def solve_z3(
    formulas: List[z3.BoolRef],
    timeout: int = 1000,
    simplify=False,
    name: str | None = None
    ) -> z3.ModelRef | None:
    """
    solve_z3
    ---------
    Solve a list of z3 constraints. If the constraints are satisfiable, then return a model that satisfies them. Otherwise, return None.

    Args:
        * `formulas` (List[z3.BoolRef]): A list of z3 formulas.
        * `timeout` (int): The timeout for the solver in milliseconds. Defaults to 1000.
        * `simplify` (bool, optional):  If `True`, then simplify the formula before solving it. Defaults to False.
        * `name` (str | None, optional): The name of the formula. Defaults to None.

    Returns:
        * z3.ModelRef | None: A Z3 model if the formula is satisfiable (the solver found a solution), `None` otherwise (the solver didn't find a solution).
    """
    if name is not None: print(Colors.BLUE,f">>> {name}",Colors.RESET)
    if simplify: formulas = [z3.simplify(formula) for formula in formulas]
    
    print_z3(formulas)
    
    s = z3.Solver()
    for formula in formulas:
        s.add(formula)
        
    # Add timeout to the solver
    s.set(timeout=timeout)
    
    status = s.check()
    # Check for a solution
    if status == z3.sat:
        m = s.model()
        print("Solution:", m)
        return m
    else:
        print("No solution")
        return None


def get_all_z3_vars(formulas : List[z3.BoolRef]) -> Set[str]:
    """
    Get all variables names (as z3 variables) in a z3 formula.
    
    ### Try to avoid it.
    """
    # TODO: Change it to get also other types, not only `z3.ArithRef`
    vars = set()
    for formula in formulas:
        vars.update(__get_all_z3_vars(formula))
    return vars  

def __get_all_z3_vars(formula) -> Set[str]:
    #TODO: need testing
    """Get all variables names (z3.ArithRef) in a z3 formula."""
    # TODO: Change it to get also other types, not only `z3.ArithRef`
    vars = set()
    for child in formula.children():
        if  len(child.children()) > 0:
            vars.update(__get_all_z3_vars(child))
        elif len(child.children()) == 0 and type(child) is z3.ArithRef:
            vars.add(str(child))
    return vars 
