# import sys
# from pathlib import Path

# # Add  the following paths to sys.path:
# sys.path.extend([
#     str(p)
#     for p in [
#         Path(__file__).parent.parent.parent # /simple_sketch
#     ]
#     if p not in sys.path]
# )

from typing import Callable, Dict, List, Optional, Set, Tuple, Union, Any
import z3
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat, ArithRef, BoolRef

import operator


from simple_sketch.while_lang.while_language import WhileLang, Env, Env_Key, Env_Val, Linv_t

from simple_sketch.z3_handler import Z3_TYPE
# from simple_sketch.lib.adt.tree import Tree
from simple_sketch.lib.adt import Tree
# For the debugging and the log file
from simple_sketch.utilities import Colors, cprint






# TODO: Add log file


OP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv, # FIXME: operator.truediv
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "=": operator.eq,
    "**": operator.pow, # TODO: check if this works
    # FIXME: add`modulus` operator `%`
}

# FIXME: Check if this is correct
OP["/"] = operator.truediv


def get_pvars_and_holes(ast: Tree) -> Set[str]:
    # TODO: check if the added "v.root == 'hole'" is correct
    return {
        v.subtrees[0].root
        for v in ast.nodes
        if len(v.subtrees) == 1 and (v.root == "id" or v.root == "hole")
    }


def get_updated_pvars(ast: Tree) -> Set[Tuple[str, str]]:
    """
    Get the set of variables that are updated in the given AST, i.e., the set of variables that appear in an assignment statement

    Return
    ------
    Set[Tuple[str, str]]: A set of tuples, where each tuple is a pair of the variable name and its type.
    """
    updated_pvars = set()
    for v in ast.nodes:
        if len(v.subtrees) >= 1 and v.root == ":=":
            var_id = v.subtrees[0].subtrees[1].root
            var_type = v.subtrees[0].subtrees[0].subtrees[0].root
            updated_pvars.add((var_id, var_type))
    return updated_pvars


def get_holes(ast: Tree) -> Set[z3.ArithRef]:
    """
    Extracts the holes as z3 variables from the given AST.
    """
    # FIXME: add it to `WhileLang` class
    holes = set()
    for node in ast.nodes:
        # TODO: maybe we don't need to convert it to `z3.Int(v.subtrees[0].root)`?
        if len(node.subtrees) == 2 and node.root == "hole":
            hole_id = node.subtrees[1].root
            hole_type = node.subtrees[0].subtrees[0].root
            holes.add(Z3_TYPE[hole_type](hole_id))
    return holes


def make_env(pvars: Set[Tuple[str, str]]) -> Dict[Env_Key, Env_Val]:
    """
    Creates a dictionary of variables and their corresponding z3 variables.
    
    The same as `WhileLang().make_env()`
    
    Args
    ----
        * pvars (Set[Tuple[str, str]]): A set of tuples, where each tuple is a pair of the variable name and its type.
    """
    return WhileLang().make_env(pvars)
    
def upd(d: Dict[Env_Key, Env_Val], k: Env_Key, v: Env_Val):
    d = d.copy()
    d[k] = v
    return d


def eval_expr(expr: Tree, env: Dict[Env_Key, Env_Val]):
    if expr.root == "id":
        var_id = expr.subtrees[1].root
        var_type = expr.subtrees[0].subtrees[0].root
        # In case the variable is not in the environment, we add it. This is needed for the while rule
        if var_id not in env.keys():
            env[var_id] = Z3_TYPE[var_type](var_id) 
        return env[var_id]

    elif expr.root in ["int_val", "float_val", "bool_val"]:
        val = expr.subtrees[1].root
        # ty = expr.root
        ty = f"{expr.subtrees[0].subtrees[0].root}_val"
        return Z3_TYPE[ty](val)
    
    elif expr.root == "not":
        b = eval_expr(expr.subtrees[1], env)
        return z3.Not(b)
        
    elif expr.root == "array_access":
        array_id = expr.subtrees[1].subtrees[1].root
        index = eval_expr(expr.subtrees[2], env)
        # return z3.Select(env[array_id], z3.Int(idx))
        return z3.Select(env[array_id], index)

    elif expr.root == "array_mult_assign":
        array_id = expr.subtrees[1].subtrees[1].root
        idx = expr.subtrees[2].subtrees[1].root
        val = eval_expr(expr.subtrees[3], env)
        return z3.Store(env[array_id], z3.Int(idx), array_id[z3.Int(idx)] * val)

    elif expr.root in OP:
        op = OP[expr.root]
        a = eval_expr(expr.subtrees[1], env)
        b = eval_expr(expr.subtrees[2], env)
        return op(a, b)

    elif expr.root == "hole":
        # TODO check what to do with this
        hole_id: str = expr.subtrees[1].root
        hole_ty = expr.subtrees[0].subtrees[0].root
        return Z3_TYPE[hole_ty](hole_id)  # TODO: Check if this is correct
        # In case the variable is not in the environment, we add it. This is needed for the while rule
        if hole_id not in env.keys():
            env[hole_id] = Int(hole_id)  # TODO: Check if this is correct
        return env[hole_id]

    else:
        raise ValueError(f"Unknown expression {expr.root}")


# TODO: Check if this is needed
def fix_env(env: Env, cond: Callable[[Env], z3.BoolRef | Any]):
    """
    Fix the environment `env` by adding the missing variables that appear in the condition `cond` but not in `env` (or in the program AST).
    To avoid writing the condition as `Int('x')` instead of `d['x']`
    """
    from re import findall
    from inspect import getsource

    # regex to match the variables in the lambda expression, i.e to match "'v'" in "d['v']".
    P_vars = findall(r"d\['([^']+)", getsource(cond))
    for v in P_vars:
        if v not in env.keys():
            env[v] = Int(v)
    return env



def wp(
    c: Tree,
    Q: Callable[[Env], z3.BoolRef],
    loop_inv: Callable[[Env], z3.BoolRef] | None = None,
) -> Callable[[Env], z3.BoolRef]:
    """
    Calculates the Weakest Precondition for a given command and postcondition.
    """
    if c.root == "skip":
        return lambda env: Q(env)

    elif c.root == ":=":
        # TODO: add live variables, for the in_vars and out_vars. look at "Week #9: Static Analysis, 236360 - Theory Of Compilation"
        def subst(env: Env):
            if c.subtrees[0].root == 'array_pos_assign':
                var = c.subtrees[0].subtrees[0].subtrees[1].root
                index = eval_expr(c.subtrees[0].subtrees[1], env)
                e = z3.Store(env[var], index, eval_expr(c.subtrees[1], env))
            else:
                var = c.subtrees[0].subtrees[1].root # c.subtrees[0] is the `id` node
                e = eval_expr(c.subtrees[1], env)
            new_env = upd(
                env, var, e
            )  # 'new_env' is the same as 'env', but with the updated value of x
            new_Q = Q(new_env)
            return new_Q  # 'new_Q' is also a function of 'env', but with the updated value of x

        return subst

    elif c.root == ";":

        def seq(env: Dict):
            c1: Tree = c.subtrees[0]
            c2: Tree = c.subtrees[1]
            M = wp(c2, Q, loop_inv=loop_inv)
            return wp(c1, M, loop_inv=loop_inv)(env)

        return seq

    elif c.root == "if":

        def if_then_else(env: Dict):
            c1: Tree = c.subtrees[1]
            c2: Tree = c.subtrees[2]
            b = eval_expr(c.subtrees[0], env)
            then_ = wp(c1, Q, loop_inv=loop_inv)
            else_ = wp(c2, Q, loop_inv=loop_inv)
            return Or(And(b, then_(env)), And(Not(b), else_(env)))

        return if_then_else

    elif c.root == "hole":
        def hole_(env: Dict):
            return Q(env)
        return hole_

    elif c.root == "assert":
        def assert_(env: Env):
            b = eval_expr(c.subtrees[0], env)
            return And(b, Q(env))
        return assert_

    elif c.root == "assume":
        def assume_(env: Env):
            b = eval_expr(c.subtrees[0], env)
            return Implies(b, Q(env))
        return assume_

    else:  # c.root == 'while':
        def while_(env: Env):
            # The case where the loop invariant (loop_inv) is given
            if loop_inv is not None:

                body_c = c.subtrees[1]
                body_vars = get_updated_pvars(body_c)
                # loop_env = mk_env(body_vars)
                loop_env = make_env(body_vars)
                for k, v in env.items():
                    if k not in loop_env:
                        loop_env[k] = v

                # FIXME: get the correct types from the `type` node in the AST
                # loop_vars = [Int(v) for v in body_vars] 
                loop_vars = [Z3_TYPE[ty](v) for v, ty in body_vars]
                b = eval_expr(c.subtrees[0], env=loop_env)  #  env=env?
                # TODO: check if wee need to send `linv` agin
                # wp_body = wp(body_c, Q=linv)
                wp_body = wp(body_c, Q=loop_inv, loop_inv=loop_inv)
                return And(
                    loop_inv(env),
                    ForAll(
                        loop_vars,
                        And(
                            Implies(And(loop_inv(loop_env), b), wp_body(loop_env)),
                            Implies(And(loop_inv(loop_env), Not(b)), Q(loop_env)),
                        ),
                    ),
                )
                
            # The case where the loop invariant (loop_inv) is not given (i.e. we want to synthesize it)
            else: #loop_inv is None, Try to generate the loop invariant
                # FIXME: Just for now, until we implement the loop invariant generation
                raise ValueError("loop_inv is None, but it should be a function that takes an env (dict) and returns a z3 formula")

        return while_
    
def get_inv_as_Z3(inv: Tree) -> Callable[[Dict[Env_Key, Env_Val]], z3.BoolRef]:
    """
    get_inv_as_Z3 gets a Tree representing a loop invariant and returns a Z3 function representing the invariant.
    Parse the text using `Z3Parser` and return the parsed formula as a Z3 function.

    Args:
        inv (Tree): _description_

    Returns:
        Callable[[Dict[Env_Key, Env_Val]], z3.BoolRef]: _description_
    """
    pass
    # # Get the invariant as a string
    # if inv.root == "invariant":
    #     inv = inv.subtrees[0]
    
    

def extend_env(env1: Env, env2: Env) -> Env:
        """
        Extend the `env1` with the items of `env2`, only of there keys are not in `env1`.
        """
        # return {**env2, **env1}
        return {**env1, **{k: v for k, v in env2.items() if k not in env1}}

def verify(
    P: Callable[[Env], z3.BoolRef],
    program: Tree | WhileLang | str,
    Q: Callable[[Env], z3.BoolRef],
    linv: Callable[[Env], z3.BoolRef] | None = None,
    pvars: Set[Tuple[str, str]] = set(),
    env: Env = {},
    debug: bool = False,
) -> bool:
    """
    Verifies a Hoare triple {P} program {Q}
    Where P, Q are assertions (see below for examples)
    and program is the AST of the command c.
    Returns `True` iff the triple is valid.
    Also prints the counterexample (model) returned from Z3 in case it is not.

    Args:
        * `P` (Callable[[Env], z3.BoolRef]): The precondition
        * `program` (Tree | WhileLang | str): The program to be verified
        * `Q` (Callable[[Env], z3.BoolRef]): The postcondition
        * `linv` (Callable[[Env], z3.BoolRef]): The loop invariant of the while loop in the program
        * `pvars` (Set[Tuple[str, str]]): A set of tuples, where each tuple is a pair of the variable name and its type.
        * `env` (Env): The initial environment (mapping from variable names to z3 values).
        
    Raises:
    # FIXME
        ValueError: If `program` is not a `Tree` or a `WhileLang` object.

    Returns:
        Bool: `True` iff the triple is valid.

    Example:
        >>> P = lambda d: And(d['a'] > 0, d['b'] > 0)
        >>> program = 'while a != b do if a > b then a := a - b else b := b - a'
        >>> Q = lambda d: And(d['a'] > 0, d['a'] == d['b'])
        >>> linv = And(d['a'] > 0, d['b'] > 0)
        >>> verify(P, program, Q, linv)

    """

    # FIXME: in `wp.verify()`, add a new argument to change the `print()` output destination (std or file or path)
    
    if isinstance(program, str):
        program = WhileLang(program)
    elif isinstance(program, (Tree)):
        program = WhileLang().from_ast(program)
    elif isinstance(program, WhileLang):
        program = program
    else:
        raise ValueError(f"program should be a WhileLang or a string or a Tree, not a {type(program)}")

    
    # Create the environment
    pvars = program.program_vars.union(pvars)
    env = extend_env(program.make_env(pvars), env)

    # Create the precondition formula
    precondition = P(env)

    # if linv is not None:
    #     env["linv"] = linv

    # Create the weakest precondition formula
    wp_condition = wp(program.program_ast, Q, loop_inv=linv)
    wp_condition = wp_condition(env)

    # Create the verification condition
    verify_cond = Implies(precondition, wp_condition)
    
    if debug:
        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> verify_cond:\n{Colors.RESET}{verify_cond}\n")
        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> precondition:\n{Colors.RESET}{precondition}\n")
        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> wp_condition:\n{Colors.RESET}{wp_condition}\n")

    # Create a Z3 solver
    solver = Solver()
    # Add the negation of the verification condition to the solver.
    solver.add(Not(verify_cond))

    # TODO: add timeout to the solver
    # solver.set(timeout=1000) # 1000 milliseconds

    # TODO: add log file
    if debug:
        import html
        from z3 import set_html_mode

        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> verify_cond:\n{Colors.RESET}{verify_cond}\n")
        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> precondition:\n{Colors.RESET}{precondition}\n")
        print(f"{Colors.BG_YELLOW}{Colors.BLACK}>>> wp_condition:\n{Colors.RESET}{wp_condition}\n")
        # print(Colors.BRIGHT_YELLOW,f">>> WP:\n{str(wp_condition)}",Colors.RESET,)
        set_html_mode(True)
        print(Colors.BRIGHT_YELLOW,">>> P: ",html.unescape(str(precondition)),Colors.RESET,)
        print(Colors.BRIGHT_YELLOW,f">>> WP:\n{html.unescape(str(wp_condition))}",Colors.RESET,)
        # print(Colors.BRIGHT_YELLOW, f">>> program:\n{html.unescape(str(program_ast))}", Colors.RESET)
        # print(Colors.BRIGHT_YELLOW,f">>> program:\n{html.unescape(pretty(program_ast))}",Colors.RESET,)
        print("\n")
        set_html_mode(False)
        print(f"{Colors.BG_BRIGHT_MAGENTA}{Colors.BLACK}>>> solver.assertions:\n{Colors.RESET}{solver.assertions()}\n")

    # If the solver is satisfiable, then the Hoare triple is not valid, that because the verification condition is not true.
    if solver.check() == sat:
        # Hoare triple is not valid
        print("Hoare triple is not valid.")
        model = solver.model()
        print("Counterexample:")
        print(model)
        return False
    # If the solver is unsatisfiable, then the Hoare triple is valid, that because the verification condition is true.
    else:
        # Hoare triple is valid
        print("Hoare triple is valid.")
        return True
