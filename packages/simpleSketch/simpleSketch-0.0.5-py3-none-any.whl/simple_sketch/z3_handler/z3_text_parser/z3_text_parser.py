"""
* file: z3_text_parser.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: Parse text strings into Z3 expressions.
"""


from typing import Callable, Dict, Any, Tuple

from lark import Lark, Transformer
import operator
import z3

from ..z3_handler import Z3_TYPE


class Z3Transformer(Transformer):
    OP = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        # "/": operator.floordiv,
        "/": operator.truediv,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
        "<=": operator.le,
        ">=": operator.ge,
        "==": operator.eq,
        "**": operator.pow # TODO: check if this works
    }
    
    Z3_connective = {
        # TODO: add more connectives
        "And": z3.And,
        "Or": z3.Or,
        "Not": z3.Not,
        "Implies": z3.Implies,
        "ForAll": z3.ForAll,
        "Exists": z3.Exists
    }
    
    
    def __init__(self, types: Dict[str, str] = {}):
        """
        Initialize the Z3Transformer.
        Args:
        ----
            * `types` (Dict[str, str], optional): The types of the variables in the Z3 expression. Defaults to {}.
        """
        self.types: Dict[str, str] = types 
        self.z3_vars_env: Dict[str, z3.ExprRef] = {}
        

    def start(self, items):
        # RULE: `start: s`
        def s(env: Dict[str, z3.ExprRef]):
            env = {**env, **{k: v for k, v in self.z3_vars_env.items() if k not in env}}
            return items[0](env)
        return s, self.z3_vars_env, self.types
    
    # --- `atom` Rules ---
    def var_id(self, items):
        'var: VAR_ID -> var_id'
        id = items[0].value
        # check if the variable is defined
        if id not in self.z3_vars_env:            
            # FIXME: check if to  `raise an error` or to give default type.
            # Check if the has a type defined in the `types` argument, 
            # if not (raise an error) or give him a default type `z3.Int`.
            
            # if id not in self.types:
                # raise ValueError(f"Variable {id} is not defined with a type.")
            if id not in self.types:
                self.types[id] = "int"
                
            id_ty = self.types[id]
            self.z3_vars_env[id] = Z3_TYPE[id_ty](id)
        return lambda env: env[id]
    
    
    def array_access(self, items):
        'array_access: VAR_ID "[" expr "]"'
        id = items[0].value
    
        # check if the variable is defined
        if id not in self.types:
            # Default type of arras
            self.types[id]  = "Array int"
            
        id_ty = self.types[id]
        # check if `id_ty` is an `Array ` type
        if id_ty[:5] !=  "Array":
            raise ValueError(f"Variable {id} is not defined with a type of Array.")
                   
        # check if `id_ty` is an `Z3_TYPE`
        if id_ty not in Z3_TYPE:
            raise ValueError(f"Variable {id} is not defined with a type.")
        
        if id not in self.z3_vars_env:
            self.z3_vars_env[id] = Z3_TYPE[id_ty](id)
        
        return lambda env: z3.Select(self.z3_vars_env[id], items[2](env))
    
    
    def int_(self, num):
        'int_: INT'
        num = num[0].value
        return lambda env: z3.IntVal(int(num))
    
    def positive_int(self, num):
        'positive_int: POSITIVE_INT'
        num = num[0].value
        return lambda env: z3.IntVal(int(num))
    
    def float_(self, num):
        'float_: FLOAT '
        num = num[0].value
        return lambda env: z3.RealVal(float(num))

    def bool_(self, items):
        'bool_: "True" | "False"'
        b = items[0].value
        return lambda env: z3.BoolVal(b)

    def string_(self, num):
        'string_: STRING'
        num = num[0].value
        return lambda env: z3.StringVal(str(num))

    def bracket_expr(self, items):
        'atom : "(" expr ")"'
        return  lambda env: (items[1](env))
    
    # TODO: add type checking
    # --- `expr` Rules ---
    
    def _binary_op(self, left, op, right):
        'Helper function, for rules in the form `expr: expr OP expr`. Where `OP` is a TOKEN.'
        # TODO: add type checking
        return lambda env: self.OP[op.value](left(env), right(env))
    
    def rel_expr(self, items):
        'expr : expr REL_OP expr'
        return self._binary_op(items[0], items[1], items[2])

    def addsub_expr(self, items):
        'expr: expr ADD_SUB expr -> addsub_expr'
        return self._binary_op(items[0], items[1], items[2])
    def muldiv_expr(self, items):
        'expr: expr MUL_DIV expr -> muldiv_expr'
        return self._binary_op(items[0], items[1], items[2])
    def pow_expr(self, items):
        'expr: expr POW expr     -> pow_expr'
        return self._binary_op(items[0], items[1], items[2])
        
    
    # --- `id_list` Rules --- 
    def idlist(self, items):
        'id_list: "[" var ("," var)* "]" -> idlist'
        vars = items[1:-1] # remove "[", "]"
        return lambda env: [vars[i](env) for i in range(0, len(vars), 2)]
    
    # --- `formula_list` Rules ---
    def formula_list(self, items):
        'formula_list: formula1 | formula_list "," formula1'
        if len(items) == 1:
            # Case: `formula_list:  formula1`
            return lambda env: [items[0](env)]
        else:
            # Case: `formula_list: formula_list "," formula1`
            return lambda env: items[0](env) + [items[2](env)] 
    
    # --- `formula` Rules ---
    def not_formula(self, items):
        'formula : NOT "(" formula1 ")"'
        return lambda env: z3.Not(items[2](env))
        
    def and_formula(self, items):
        'formula : AND "(" formula_list ")"'
        return lambda env: z3.And(*items[2](env))
    
    def or_formula(self, items):
        'formula : OR "(" formula_list ")"'
        return lambda env: z3.Or(*items[2](env))
    
    def implies_formula(self, items):
        'formula : IMPLIES "(" formula1 "," formula1 ")"'
        return lambda env: z3.Implies(items[2](env), items[4](env))
    
    def forall_formula(self, items):
        'formula : FORALL "(" id_list "," formula1 ")"'
        return lambda env: z3.ForAll(items[2](env), items[4](env))
    
    def exists_formula(self, items):
        'formula : EXISTS "(" id_list "," formula1 ")"'
        return lambda env: z3.Exists(items[2](env), items[4](env))
    
    
class Z3Parser:
    """
    Z3Parser
    ---------
    """
    ALLOWED_TYPES = list(Z3_TYPE.keys())
    
    def __init__(self):
        """
        """
        self.parser = Lark.open('z3_syntax.lark',  rel_to=__file__, parser='earley', keep_all_tokens=True)

    def __call__(self, 
                z3_text: str, 
                types: Dict[str, str] | str = {}
                ) -> Tuple[ 
                            Callable[[Dict[str, Any]], z3.BoolRef], 
                            Dict[str, z3.ExprRef], 
                            z3.BoolRef,
                            Dict[str, str]
                        ] | None :
        """
        Parse the Z3 expression and return the corresponding `z3.BoolRef` expression.

        Args:
        ----
            * `z3_text` (str): The Z3 expression to be parsed.
            * `types` (Dict[str, str] | str, optional): The types of the variables in the Z3 expression. Defaults to {}.
                    - `types` is a dictionary that maps variable names to their types.
                    - The types are specified as strings, and are one of the following: 
                        - `int`
                        - `real`
                        - `bool`
                        - `Array int`
                        - `Array bool`
                    - If a variable is not in the `types` dictionary, then it is assumed to be of type `int`.
                    - If `types` is a `string`, then it is assumed to be a of the form:
                    - `types = "{name1 : type1, name2 : type2, name3 : type3}"`
                    - where `name{i}` are variable names, and `type{i}` are the types of the variables.
        
        Returns
        -------
        Tuple (z3_expr, z3_vars_env, z3_expr(z3_vars)) | None:
            `z3_expr` (Callable[[Dict[str, Any]], z3.BoolRef]): the z3 parsed expression as a function of the variables.
            `z3_vars_env` ([Dict[str, z3.ExprRef]): The variables in the z3 expression (map each variable to its z3 expression)
            `z3_expr(z3_vars)` (z3.BoolRef): The evaluated z3 expression.
            `z3_vars_types` (Dict[str, str]): The types of the variables in the z3 expression (for `Z3_TYPE`).
        
        Raises:
        -------
            ValueError: If the type of the variable is invalid.
            ValueError: If the Z3 expression is invalid.
            
        Examples:
        ---------
            >>> Z3Parser()("x < 2")
            (x < 2, {'x': Int('x')}, x < 2, {'x': 'Int'})
            >>> Z3Parser()("And ( x = 2 , y < 2 )")
            (And(x == 2, y < 2), {'x': Int('x'), 'y': Int('y')}, And(x == 2, y < 2), {'x': 'Int', 'y': 'Int'})
        """
        
        # if `types` is string, then convert it to dictionary
        if isinstance(types, str):
            # TODO: Fix this in another way!!
            if len(types) == 0 or types.strip()[0] != '{' and types.strip()[-1] != '}':
                types = "{" + types + "}"
            # TODO: make it look better
            if types.strip()[1:-1].strip() == "":
                types = {}
            else:
                try:
                    types = {k.strip(): v.strip() for k, v in [pair.split(":") for pair in types[1:-1].split(",")]}
                except Exception as e:
                    e.add_note(f"Invalid types string: {types}")
                    raise
                
        for var, ty in types.items():
            if ty not in self.ALLOWED_TYPES:
                raise ValueError(f"Invalid type {ty} for variable {var}. Allowed types: {self.ALLOWED_TYPES}")
        
        self.types = types
        
        # for the case `z3_text` is empty
        if z3_text.strip() == "":
            z3_text = "True"
        
        try:
            tree = self.parser.parse(z3_text)
            res = Z3Transformer(self.types).transform(tree)
            z3_expr: Callable[[Dict[str, Any]], z3.BoolRef] = res[0]
            z3_vars_env: Dict[str, z3.ExprRef] = res[1]
            z3_vars_types: Dict[str, str] = res[2]
            return z3_expr, z3_vars_env, z3_expr(z3_vars_env), z3_vars_types
        except Exception as e:
            e.add_note(f"Invalid Z3 expression: {z3_text}")
            raise e
        
    def parse(
        self, 
        z3_text: str, 
        types: Dict[str, str] | str = {}
        ) -> Tuple[ Callable[[Dict[str, Any]], z3.BoolRef], Dict[str, Any], z3.BoolRef,Dict[str, str]] | None :
        """
        The same as `__call__` 
        """
        return self.__call__(z3_text, types)
            


    
if __name__ == '__main__':
    # from utilities import Utilities 
    
    # Run the test
    # test_postprocess()
    # print(Z3Parser()("x < 2"))
    # print(Z3Parser()("And ( x = 2 , y < 2 )")[2])
    
    # TODO: handel the case `b` type `z3.Bool`
    expr = Z3Parser()("And(x + 1 = 2, y < 2 , b, 1 = 2)")
    print("invalid expr" if not expr else f"\nvars: {expr[1]}\nexpr[2]: {expr[2]}")
    
    expr = Z3Parser()("ForAll([ x , y ] , (x + 1 = y) )")
    # expr = Z3Parser()("ForAll([ x ] , (x + 1 = y) )")
    print("invalid expr" if not expr else f"\nvars: {expr[1]}\nz3_expr: {expr[2]}")
    
    
    expr = Z3Parser()("Or ( 2 + 1 < x , And ( x = 2 , y < 2 ) )")
    print("invalid expr" if not expr else f"\nvars: {expr[1]}\nexpr[2]: {expr[2]}")
    

    expr = Z3Parser()("ForAll([ x , y ], And(x + 1 = 2, y < 2 , b=1, 1 = 2))")
    print("invalid expr" if not expr else f"\nvars: {expr[1]}\nexpr[2]: {expr[2]}")
    
    expr = Z3Parser()("Exists(x, Or ( 2 + 1 < x , And ( x = 2 , y < 2 )))")
    print("invalid expr" if not expr else f"\nvars: {expr[1]}\nexpr[2]: {expr[2]}")
    
    
    # expr = Z3Parser()("Or ( 2 + 1 < x , And ( x = 2 , y < 2 ) )")
    # expr = Z3Parser()("Or ( 2 + 1 < x , And ( x = 2 , y < 2 ) )")
    # expr = Z3Parser()("Or ( x <  2) ")
    # expr = Z3Parser()("Or ( x <  2) ")
    # expr = Z3Parser()("x = 2")
    # expr = Z3Parser()("x + 2")
    # print(Z3Parser()("ForAll( [ x , y] , (x < y) )"))
    # print(Z3Parser()("ForAll( [ x , y] , (x < y) )"))
    # print(Z3Parser()("ForAll( [ x ] , (x < y) )"))
    # print(Z3Parser()("x + 2"))
    # print(Z3Parser()(r"""
    #                 x + 1
    #                 """))
    # print(Z3Parser()(r"""
    #                 And(x + 1 == 2, y < 2 , b, 1 == 2)
    #                 """))
    # print(Z3Parser()(r"""
    #                 And ( x = 2 , y < 2 )
    #                 """))
    # print(Z3Parser()(r"""
    #                  Or ( 2 + 1 < x , And ( x = 2 , y < 2 ))
    #                 """))
