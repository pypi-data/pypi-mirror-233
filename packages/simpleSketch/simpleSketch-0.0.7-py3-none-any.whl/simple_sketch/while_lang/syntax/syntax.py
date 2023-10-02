



from simple_sketch.lib.adt.tree import Tree  

from lark import Lark, Transformer, v_args
from typing import List, Dict, Union, Tuple, TypeAlias, Set

from simple_sketch.utilities.Utilities import Colors



class SymbolTable:
    """
    # TODO: haddel the case if one of them is `Tree` (value1 = expr = Tree(num, 1) and value2 = 2)))
    """
    Value: TypeAlias = Union[int, float, bool, Tree]
    Value_t = ['int', 'float', 'bool', 'Array int', 'Array bool']
    table: Dict[str, Tuple[Value, str]]
    
    def __init__(self):
        self.symtable= {}
    
    def insert(self, var_id: str, value: Value | None = None, type_:str = 'int') -> None:
        # TODO
        if type_ not in self.Value_t:
            raise ValueError(f"Type {type_} is not supported")
        # TODO: check if we can change this for each block (like in C)
        # Prevent re-declaration of variables
        if var_id in self.symtable:
            raise ValueError(f"Variable {var_id} already declared (exists in the symbol table)")
        # TODO: add support for `Tree`
        if value is None:
            value = False if type_ == 'bool' else 0 if type_ == 'int' else 0.0
        self.symtable[var_id] = (value, type_)
    
    def get(self, var_id: str):
        return self.__getitem__(var_id)
    
    def __getitem__(self, var_id: str) -> Tuple[Value, str]:
        if var_id not in self.symtable:
            raise KeyError(f"Variable {var_id} does not exist (not declared))")
        return self.symtable[var_id]
    
    def __setitem__(self, var_id: str, value: Value):
        old_var =  self.__getitem__(var_id)
        # TODO: maybe to try casting?
        # TODO: haddel the case if one of them is `Tree` (value1 = expr = Tree(num, 1) and value2 = 2)))
        if type(value) != type(old_var[0]):
            raise TypeError(f"Type mismatch: {type(value)} and {type(old_var[0])}")
        self.symtable[var_id] = (value, old_var[1])
    
    def __iter__(self):
        return iter(self.symtable)
    
    def __len__(self):
        return len(self.symtable)

    def get_type(self, var_id: str) -> str:
        return self.__getitem__(var_id)[1]
    
    def get_value(self, var_id: str) -> Value:
        return self.__getitem__(var_id)[0]
    
    def set_value(self, var_id, value):
        self.__setitem__(var_id, value)
    
    def __contains__(self, var_id: str):
        return var_id in self.symtable
    
    def __str__(self):
        s = ""
        for var_id, (value, type_) in self.symtable.items():
            s += f"{var_id}: {value} ({type_})\n"
        return s
    
    def __repr__(self):
        return str(self)



class TypeChecker:
    def check(self, operation, operand1, operand2=None):
        type1 = operand1[1]
        type2 = operand2[1] if operand2 else None

        if operation in ['add', 'sub', 'mul', 'div']:
            if type1 != type2:
                raise TypeError(f"Type mismatch: {type1} and {type2}")
        elif operation in ['rel_op', 'and_op', 'or_op', 'not_op']:
            if type1 != 'bool' or (type2 and type2 != 'bool'):
                raise TypeError(f"Operands must be of type 'bool', got {type1} and {type2}")

        return True

# def check_type(expr: Tree, expected_type: List[str]):
#     """
#     It Assumes that `expr.subtrees[0].subtrees[0].root` is the type of `expr`
#     """
#     # FIXME: add it to class TypeChecker
#     expr_type = expr.subtrees[0].subtrees[0].root if expr.subtrees[0].root == 'type' else None
    
#     if expr_type not in expected_type:
#         raise TypeError(f"Expected type {expected_type}, got {expr_type}")
#     return True

def check_type2(expr1: Tree, expr2: Tree):
    """
    It Assumes that `expr.subtrees[0].subtrees[0].root` is the type of `expr`
    """
    # FIXME: add it to class TypeChecker
    # TODO: try casting first?
    expr1_type = expr1.subtrees[0].subtrees[0].root if expr1.subtrees[0].root == 'type' else None
    expr2_type = expr2.subtrees[0].subtrees[0].root if expr2.subtrees[0].root == 'type' else None
    if expr1_type != expr2_type:
        raise TypeError(f"Type mismatch: {expr1_type} and {expr2_type}")
    return True

def check_type_str(expr1_type: str, expr2_type: str):
    # FIXME: add it to class TypeChecker
    # TODO: try casting first?
    if expr1_type != expr2_type:
        raise TypeError(f"Type mismatch: {expr1_type} and {expr2_type}")
    return True

def check_type(types1: Set[str], types2: Set[str]) -> bool:
    """
    Return
    ------
        * True if `types1` is sub-set of `types2`, i.e. `types1 ⊆ types2`.
        * False otherwise.
    """
    # Check if `types1` is sub-set of `types2`
    return  types1.issubset(types2)

class WhileTransformer(Transformer):
    """
    #TODO: Not declared variables are not handled properly. 
    # It should be used ONLY for the 'Sketching' part.
    # The default type for variables is `int`, with unknown (uninitialized) value.
    
    # FIXME: Create a new class for `expr` rules: `class Expr(Tree)`
    # FIXME: Create a new class for `statement` rules: `class Statement(Tree)`
    """
    # CNAME = str
    
    def __init__(self):
        self.__holes_count = 0
        self.symbol_table = SymbolTable()
        self.type_checker = TypeChecker()
    
     # ---- Helper functions ----
    # def _default_value(self, type_: str, array_size: int | None = None) -> Tree:
    #     "get the default values for `['int', 'positive_int', 'float', 'bool']` as `Tree`"
    #     #  TODO: maybe change `num` to `int`
    #     if type_ in ['int', 'positive_int', 'float', 'bool']:
            
    #         if type_ == 'int' or type_ == 'positive_int':
    #             t = Tree('int', [self.__make_type('int'), Tree(0)])
    #         elif type_ == 'float':
    #             t = Tree('float', [self.__make_type('float'), Tree(0.0)])
    #         else: #type_== 'bool':
    #             t = Tree('bool', [self.__make_type('bool'), Tree(False)])
    #         setattr(t, 'type', type_)
    #         return t
    #     elif type_[:6] == 'array_':
    #         # TODO: don't add default vals for the array items (like for `var_id`)
    #         # TODO
    #         t = Tree('array', [self._default_value(type_[6:])*array_size])
    #     else:
    #         raise ValueError(f"Type {type_} is not supported")
        
    def __check_declared(self, var: Tree):
        """Assumes that:
        1. `var.subtrees[0].subtrees[0].root` is the type of `var`
        2. `var.subtrees[1].root` is the name(id) of `var`
        """
        var_id, var_ty= var.subtrees[1].root, var.subtrees[0].subtrees[0].root
        if var_id in self.symbol_table:# TODO check if needed
            raise ValueError(f"Variable {var_id} ({var_ty}) declared")
        
    def __check_not_declared(self, var: Tree):
        """Assumes that:
        1. `var.subtrees[0].subtrees[0].root` is the type of `var`
        2. `var.subtrees[1].root` is the name(id) of `var`
        """
        var_id, var_ty= var.subtrees[1].root, var.subtrees[0].subtrees[0].root
        if var_id not in self.symbol_table:# TODO check if needed
            raise ValueError(f"Variable {var_id} ({var_ty}) not declared")

    def __is_declared(self, var: Tree):
        """Assumes that:
        1. `var.subtrees[0].subtrees[0].root` is the type of `var`
        2. `var.subtrees[1].root` is the name(id) of `var`
        """
        var_id, var_ty= var.subtrees[1].root, var.subtrees[0].subtrees[0].root
        return var_id in self.symbol_table

    def __expr_type(self, var: Tree) -> str | None:
        """Assumes that:
        1. `var.subtrees[0].subtrees[0].root` is the type of `var`
        2. `var.subtrees[1].root` is the name(id) of `var`
        """
        if var.subtrees[0].root != 'type':
            raise ValueError(f"Expected `var` to have `type` as first subtree, got {var.subtrees[0].root}")
        return var.subtrees[0].subtrees[0].root
        
    def __make_type(self, type: str | None) -> Tree:
        return Tree('type', [Tree(type)])
    
    
    # ---- `atom` Rules ----
    def int_(self, num) -> Tree:
        'Rule: `int_: INT`'
        # TODO: maybe change `num` to `int`
        t = Tree('int_val', [self.__make_type('int'), Tree(int(num[0].value))])
        return t
    
    def positive_int(self, num) -> Tree:
        'positive_int: POSITIVE_INT'
        # TODO: maybe change `num` to `int`
        t = Tree('int_val', [self.__make_type('int'), Tree(int(num[0].value))])
        return t
    
    def float_(self, num) -> Tree:
        'float_: FLOAT'
        t = Tree('float_val', [self.__make_type('float'), Tree(float(num[0].value))])
        return t

    def bool_(self, item) -> Tree:
        'Rule: `bool: "True" | "False"`'
        val = True if item[0].value == 'True' else False
        t = Tree('bool_val', [self.__make_type('bool'), Tree(val)])
        return t

    # bracket_expr
    def bracket_expr(self, items) -> Tree:
        'Rule: `atom: "(" expr ")"`'
        return items[1]
    
    # # hole
    # def hole(self, items) -> Tree:
    #     'Rule: `atom: "??"`'
    #     hole_id = f'c{self.__holes_count}'
    #     self.__holes_count += 1
    #     # FIXME: check how to create holes with diffrent type
    #     t = Tree('hole', [self.__make_type('int'), Tree(hole_id)])
    #     return t
    
    # hole
    def hole(self, items) -> Tree:
        'Rule: `hole: "??" | "int?" | "float?" | "bool?" | "array?"`'
        hole_id = f'c{self.__holes_count}'
        self.__holes_count += 1
        # '??' is the default type for holes (i.e. `int`)
        hole_ty = items[0].value[:-1] if len(items[0].value) > 2 else 'int'
        t = Tree('hole', [self.__make_type(hole_ty), Tree(hole_id)])
        return t
    
    # array_access
    def array_access(self, items) -> Tree:
        'Rule: `atom: var "[" expr "]"`'
        array_id, index = items[0], items[2]
        self.__check_not_declared(array_id)
        check_type({self.__expr_type(array_id)}, {'Array int', 'Array float', 'Array bool'})
        check_type({self.__expr_type(index)}, {'int'})
        # FIXME: IN `WP`, ALSO CHECK IF: `0 <= eval(index) < array_id.size`
        array_ty = array_id.subtrees[0].subtrees[0].root[6:]
        t = Tree('array_access', [self.__make_type(array_ty), array_id, index])
        return t
    
    # ---- `var` Rules ----
    def var_id(self, name) -> Tree:
        """
        #TODO: Not declared variables are not handled properly. 
        # It should be used ONLY for the 'Sketching' part.
        # The default type for variables is `int`, with unknown (uninitialized) value.
        
        'Rule:  `var: ID -> var_id`'

        Return(Tree): 
        ```
              id
            /     \\
          type   var_id
            |
        var_type
        ```
        Where: 
            - var_id (str): is the name of this var. 
            - var_type (str): is the type of this var. Default to `None`. 
        """
        var_id, var_type = name[0].value, None
        # check if the id is already declared, if so, get its type
        if var_id in self.symbol_table:
            var_type = self.symbol_table.get_type(var_id)
            # TODO:check if its type Array, if so:
            # add the array size (from `symbol_table`) to the `array` ('t') subtrees, also as `attr`

        t = Tree('id', [self.__make_type(var_type), Tree(var_id)])
        return t
    
    # ---- `type` Rules ----
    def type_(self, item) -> Tree:
        'Rule: `type_: "int" | "float" | "bool"`'
        t = Tree('type', [Tree(item[0].value)])
        # setattr(t, 'type', 'type')
        return t
    
    def array_type(self, items) -> Tree:
        'Rule: `array_type: "Array" type_'
        type_ = items[1].subtrees[0].root
        t = Tree('type', [Tree(f"Array {type_}")])
        # setattr(t, 'type', 'type')
        return t
    
    # ---- `statements` Rules ----
    def seq(self, items) -> Tree:
        'Rule: `statements: statements statement'
        return Tree(';', [items[0], items[1]])
    
    def empty_stmt(self, items):
        'Rule: `statement: ";"`'
        return Tree('skip', [Tree('skip')])
    
    # ---- `statement` Rules ----
    def skip_stmt(self, _) -> Tree:
        'Rule: `statement: "skip" ";"'
        t = Tree('skip', [Tree('skip')])
        return t
    
    def ifelse_stmt(self, items) -> Tree:
        'Rule: `statement:"if" "(" expr ")" block ( "else" block )?'
        # FIXME: remove the declared vars from the then block? so ` if(b) {int a:=1;} else {int a:=2;}` will work ok
        cond = items[2]
        then_stmt, else_stmt = items[4], items[6] if len(items) > 6 else self.skip_stmt(None)
        check_type({self.__expr_type(cond)}, {'bool'})  # TODO: Add support for casting to bool
        t = Tree('if', [cond, then_stmt, else_stmt])
        return t
    
    def while_stmt(self, items) -> Tree:
        'Rule: `statement: "while" "(" expr ")" block'
        cond, stmt = items[2], items[4]
        check_type({self.__expr_type(cond)}, {'bool'})  # TODO: Add support for casting to bool
        t = Tree('while', [cond, stmt])
        return t
    
    def assert_stmt(self, items) -> Tree:
        # Rule: `statement: "assert" "(" expr ")" ";"`
        cond = items[2]
        check_type({self.__expr_type(cond)}, {'bool'})# TODO: Add support for casting to bool
        t = Tree('assert', [cond])
        return t
    
    def assume_stmt(self, items) -> Tree:
        # Rule: `statement: "assume" "(" expr ")" ";"`
        cond = items[2]
        check_type({self.__expr_type(cond)}, {'bool'}) # TODO: Add support for casting to bool
        t = Tree('assume', [cond])
        return t
    
    def block_stmt(self, items) -> Tree:
        'Rule: `block: "{" statements "}"'
        return items[1]
    
    # ---- `declaration` Rules ----
    def var_decl(self, items) -> Tree:
        'Rule: `declaration: type_ var (":=" expr)? ";"'
        var_type:Tree = items[0]
        var_id: Tree = items[1]
        var_id_str = var_id.subtrees[1].root
        # Replace the default type(`None`) with the actual type
        var_id.subtrees[0] = var_type
        # setattr(var_id, 'type', var_type.subtrees[0].root)
        self.__check_declared(var_id)
        # For case when there is no initialization (i.e. `type_ var ;`), we initialize it with the default value.
        if len(items) > 3:
            # Case: `type_ var := expr;`
            expr = items[3]
            # check if `expr` has no type(i.e. None), if so then give him the type of `var`
            if self.__expr_type(expr) is None:
                # check if `expr` is some `var` (int x := y;) 
                if expr.root == 'id':
                    expr_id = expr.subtrees[1].root
                    expr_type = var_type.subtrees[0].root
                    if expr_id != var_id_str:
                        # check if `expr` is declared
                        if expr_id in self.symbol_table:
                            expr_type = self.symbol_table.get_type(expr_id)
                        else:
                            # declare `expr`
                            self.symbol_table.insert(expr_id, expr, expr_type)
                            # setattr(expr, 'is_decl', True)
                    expr.subtrees[0] = self.__make_type(expr_type)
                else:
                    expr.subtrees[0] = var_type.clone()
                        

            check_type2(var_id, expr)
        else:
            # TODO: check if we dont need to add default value. (so the solver works ok)
            # expr = self._default_value(items[0].subtrees[0].root)
            expr = var_id.clone() # e.g. `int x:= x;`
        
        self.symbol_table.insert(var_id_str, expr, var_type.subtrees[0].root)
        setattr(var_id, 'is_decl', True)
        # TODO: check if we need to add `Tree` node `type` for `:=`
        return Tree(':=', [var_id, expr])
    
    def array_decl3(self, items) -> Tree:
        'Rule: `declaration: array_type var ":=" var ";"`'
        array_type, array_id, array_id2 = items[0], items[1], items[3] #type Tree
        # Replace the default type(`None`) with the actual type
        array_id.subtrees[0] = array_type
        
        # if declared raise error
        self.__check_declared(array_id)
        
        # check if `array_id2` is the same as `array_id` (e.g. `Array int A := A;`), if so declare it with the type of `array_id`
        if array_id.subtrees[1].root == array_id2.subtrees[1].root:
            array_id2.subtrees[0] = array_type.clone()
        else:
            # check if `array_id2` is declared, if so get its type, else declare it with the type of `array_id`
            if array_id2.subtrees[1].root in self.symbol_table:
                array_id2.subtrees[0] = self.__make_type(self.symbol_table.get_type(array_id2.subtrees[1].root))
            else:
                array_id2.subtrees[0] = array_type.clone()
                # declare `array_id2`
                self.symbol_table.insert(array_id2.subtrees[1].root, array_id2, array_type.subtrees[0].root)
                # setattr(array_id2, 'is_decl', True)
        
        check_type2(array_id, array_id2)
        self.symbol_table.insert(array_id.subtrees[1].root, array_id2, array_type.subtrees[0].root)
        setattr(array_id, 'is_decl', True)
        return Tree(':=', [array_id, array_id2])
        
        
    
    def array_decl(self, items) -> Tree:
        # FIXME: no need for size in `array_type` (i.e. `array_type: "Array" type_ "[" positive_int "]"`).
        # XXX: Use it for `Vector` (z3.Vector) type (i.e. `array_type: "Vector" type_ "[" positive_int "]"`)
        'Rule: `declaration: array_type var "[" positive_int "]" (":=" "[" expr_list "]")? ";"`'
        array_type, array_id, array_size = items[0], items[1], items[3] #type Tree
        # Replace the default type with the actual type
        array_id.subtrees[0] = array_type
        # setattr(array_id, 'type', array_type.subtrees[0].root)
        self.__check_declared(array_id)
        
        array_elem_ty =  array_type.subtrees[0].root[6:]
        
        # TODO: add the array size to the `array_type` subtrees, also as `attr`
        
        if len(items) > 6:
            # Case: ` array_type var "[" positive_int "]" ":=" "[" expr_list "]" ";"`
            expr_list:Tree = items[7]
            if len(expr_list.subtrees) != array_size.subtrees[0].root:
                raise ValueError(f"Array size mismatch: {array_size.subtrees[0].root} != {len(expr_list.subtrees)}")
            # check_type(array_size, ['positive_int']) # TODO: also (`int` > 0)?
            for expr in expr_list.subtrees: 
                expr_ty = self.__expr_type(expr)
                # check if `expr` has no type(i.e. None), if so then give him the type of `var`
                if expr_ty is None:
                    expr_ty = array_elem_ty
                    expr.subtrees[0] = self.__make_type(expr_ty)
                    # setattr(expr, 'type',expr_ty)
                check_type_str(array_elem_ty, expr_ty)
        else:
            # For case when there is no initialization, we initialize it with the default value.
            # expr_list:Tree = self._default_value(array_type.subtrees[0].root, array_size.subtrees[0].root)
            # TODO: don't add default vals for the array items
            # expr_list:Tree = self._default_value(array_type.subtrees[0].root, array_size.subtrees[0].root)
            expr_list:Tree = array_id.clone()
        # declare `array_id`
        self.symbol_table.insert(array_id.subtrees[1].root, expr_list, array_type.subtrees[0].root)
        setattr(array_id, 'is_decl', True)
        # TODO: also store the `array_size` in `symbol_table` so we can get it in `var_id` Rule.
        return Tree(':=', [array_id, expr_list])
    
    def array_decl2(self, items) -> Tree:
        'Rule: array_type var ";"'
        array_type, array_id = items[0], items[1] #type Tree
        # Replace the default type with the actual type
        array_id.subtrees[0] = array_type
        # setattr(array_id, 'type', array_type.subtrees[0].root)
        self.__check_declared(array_id)
        self.symbol_table.insert(array_id.subtrees[1].root, array_id, array_type.subtrees[0].root)
        setattr(array_id, 'is_decl', True)
        return Tree(':=', [array_id, array_id.clone()])
     

    def expr_list(self, items) -> Tree:
        'Rule: `expr_list: expr ("," expr)*`'
        expr_list = [ items[i] for i in range(0, len(items), 2) ]
        return Tree('expr_list', expr_list)
        
        
    # ---- `assignment` Rules ----
    def var_assign(self, items) -> Tree:
        'Rule: `assignment: var ":=" expr ";"`'
        var, expr = items[0], items[2]
        # Check if `var` wasn't declared
        # self.__check_not_declared(var)
        

        # if `var` is not declared, declare it with the type of `expr`, or `int` if `expr` has no type
        if not self.__is_declared(var):
            # check if `expr` has no type(i.e. None), if so then give him  and `var` the type `int`
            expr_ty = self.__expr_type(expr)
            if expr_ty is None:
                expr_ty = 'int'
                # check if `expr` is some `var` (int x := y;) 
                if expr.root == 'id':
                    expr_id = expr.subtrees[1].root
                    if expr_id != var.subtrees[0].root:
                        # check if `expr` is declared
                        if expr_id in self.symbol_table:
                            expr_ty = self.symbol_table.get_type(expr_id)
                        else:
                            # declare `expr`
                            self.symbol_table.insert(expr_id, expr, expr_ty)
                            # setattr(expr, 'is_decl', True)
                expr.subtrees[0] = self.__make_type(expr_ty)
                    
            # Declare `var` with the type of `expr`
            # change the default type of `var`(None) to the type of `expr`
            var.subtrees[0] = self.__make_type(expr_ty)
            # add `var` to the symbol table
            self.symbol_table.insert(var.subtrees[1].root, expr, expr_ty)
            setattr(var, 'is_decl', True)
        
        # if `var` is declared,  and `expr` has no type, then give `expr` the type of `var`
        elif self.__is_declared(var) and self.__expr_type(expr) is None:
            # FIXME: first, check if we need to check if the `expr.subtrees[0]` is `type` node before we change it.
            expr.subtrees[0] = var.subtrees[0].clone()
        
        # TODO: try casting first?
        check_type2(var, expr)
        t = Tree(':=', [var, expr])
        # update the `value` of `var` in the symbol table
        self.symbol_table.set_value(var.subtrees[1].root, expr) #TODO: check if needed
        return t
    
    def array_assign(self, items) -> Tree:
        'Rule: `assignment: var ":=" "[" expr_list "]" ";"`'
        array_id, expr_list = items[0], items[3]
        # Check if `var` wasn't declared
        self.__check_not_declared(array_id)
        # check if the type of `var` is `Array`
        check_type({self.__expr_type(array_id)}, {'Array int', 'Array float', 'Array bool'})
        array_type = array_id.subtrees[0]
        array_elem_ty = array_type.subtrees[0].root[6:]
        #  FIXME: Check if the array size == len(expr_list)

        for expr in expr_list.subtrees: 
            expr_ty = self.__expr_type(expr)
            # check if `expr` has no type(i.e. None), if so then give him the type of `array`
            if expr_ty is None:
                expr_ty = array_elem_ty
                expr.subtrees[0] = self.__make_type(expr_ty)
                # setattr(expr, 'type',expr_ty)
            check_type_str(array_elem_ty, expr_ty)
                
        # TODO: check if this is correct
        t = Tree(':=', [array_id, expr_list])
        # update the `value` of `var` in the symbol table
        self.symbol_table.set_value(array_id.subtrees[1].root, expr_list) #TODO: check if needed
        return t
    
    def array_pos_assign(self, items) -> Tree:
        # FIXME: IN `WP`, ALSO CHECK IF: `0 <= eval(index) < array_id.size`
        'Rule: `var "[" expr "]" ":=" expr ";" -> array_pos_assign`'
        array_id, index, expr = items[0], items[2], items[5]
        self.__check_not_declared(array_id)
        array_ty = self.__expr_type(array_id)
        
        assert array_ty is not None, "Array type is None"
        
        check_type({array_ty}, {'Array int', 'Array float', 'Array bool'})
        check_type({self.__expr_type(index)}, {'int'})
        # FIXME: IN `WP`, ALSO CHECK IF: `0 <= eval(index) < array_id.size`
        
        check_type_str(array_ty[6:], self.__expr_type(expr))
        
        # TODO:?
        # # create node for `array_id[index]` with: `type = expr.type`, `id=array_id[index]`
        # array_element = Tree('id', [expr.subtrees[1], Tree(f'{array_id}[]')])
        t = Tree(':=', [
                        Tree('array_pos_assign', [array_id, index]), 
                        expr
        ])# FIXME: IN `WP`, ALSO CHECK IF: `0 <= eval(index) < array_id.size`
        # TODO: update the `value` of `array_id[index]` in the symbol table???
        return t
    
    # ---- `expr` Rules ----
    def _binary_op(self, items, op_type: str, res_type: str) -> Tree:
        """
        Handles binary operations.
        For rules in the form `expr: expr OP expr`. Where `OP` is a TOKEN.
        """
        left, op, right = items
        
        # if `left` or `right` has no type, then give it the type of op `op_type`
        if self.__expr_type(left) is None:
            left.subtrees[0] = self.__make_type(op_type)
        if self.__expr_type(right) is None:
            right.subtrees[0] = self.__make_type(op_type)
        
        check_type({self.__expr_type(left)}, {op_type}); check_type({self.__expr_type(right)}, {op_type})
        t = Tree(op.value, [self.__make_type(res_type) ,left, right])
        return t

    def andor_expr(self, items) -> Tree:
        'Rule: `expr: expr BOOL_OP expr `'
        return self._binary_op(items, op_type='bool', res_type='int')
        
    def not_expr(self, items) -> Tree:
        'Rule: `expr: NOT expr`'
        op, expr = items
        check_type({self.__expr_type(expr)}, {'bool'})
        t = Tree(op.value, [self.__make_type('bool') ,expr])
        # setattr(t, 'type', 'bool')
        return t
        
    def rel_expr(self, items) -> Tree:
        'Rule: `expr: expr REL_OP expr `'
        # FIXME: add support for casting
        # FIXME: add support for Arrays types
        return self._binary_op(items, op_type='int', res_type='bool')
        
    def addsub_expr(self, items) -> Tree:
        'Rule: `expr: expr ADD_SUB expr `'
        return self._binary_op(items, op_type='int', res_type='int')
    
    def muldiv_expr(self, items) -> Tree:
        'Rule: `expr: expr MUL_DIV expr `'
        return self._binary_op(items, op_type='int', res_type='int')
        
    def pow_expr(self, items) -> Tree:
        'Rule: `expr: expr POW expr `'
        return self._binary_op(items, op_type='int', res_type='int')
    
    
    
    # ### `inv` Rules ###
    # # TODO
    # def invariant(self, items) -> Tree:
    #     return Tree('invariant', [items[0]])

    # def not_invariant(self, items) -> Tree:
    #     return Tree('not', [items])

    # def and_invariant(self, items) -> Tree:
    #     return Tree('and', [items])
    
    # def or_invariant(self, items) -> Tree:
    #     return Tree('or', [items])

    # def bracket_invariant(self, items) -> Tree:
    #     # return Tree(items[0])
    #     return items[0]

    # ### TOKENS ###
    # def POSITIVE_INT(self, items) -> Tree:
    #     return Tree('num', [Tree(int(items.value))])

    # def INT(self, items) -> Tree:
    #     return Tree('num', [Tree(int(items.value))])

    # def REL_OP(self, items):
    #     return str(items)
    # def ADD_SUB(self, items):
    #     return str(items)
    # def MUL_DIV(self, items):
    #     return str(items)
    # def POW(self, items):
    #     return str(items)


class WhileParser:
    """
    WhileParser
    -----------
    
    """
    def __init__(self, debug: bool = False):
        """
         
        """
        self.parser = Lark.open('while_lang.lark',  rel_to=__file__, parser='earley', 
                                keep_all_tokens=True, debug=debug)        
    def __call__(self, program_text) -> Tree | None:
        """
        
        """
        try:
            tree = self.parser.parse(program_text)
            tree = WhileTransformer().transform(tree)
            return tree
        except Exception as e:
            e.add_note(f"ERROR - WhileParser - Invalid program:\n{program_text}")
            # e.add_note(f"WhileParser: {e.with_traceback()}")
            raise

        
       
    

def pretty(expr: Tree, indent=0, with_type_hint=False) -> str:
    """
    pretty
    ------
    Formats an `Tree` expression for pretty printing.
    
    Args
    ----
        - expr (Tree): The expression to format.
        - indent (int): The indentation level.
        - with_type_hint (bool): If `True`, add the type of the expression as a comment.
    
    
    # TODO: IMPORTANT - NEED FIXING - IT IS NOT USED IN `WhileLang` class
    # TODO: IT IS NOT USED IN `WhileLang` class
    """
    # Base case: if the expression is a leaf node, return its value
    if not expr.subtrees:
        return str(expr.root)

    # TODO: add the new grammar for `invariant` , `and` , `or` and `not`
    # Recursive case: handle different constructs in the language
    if expr.root == 'skip':
        return 'skip ;'
    elif expr.root == ':=':
        return f"{pretty(expr.subtrees[0],0,with_type_hint)} := {pretty(expr.subtrees[1],0,with_type_hint)} ;"
    elif expr.root == ';':
        return f"{pretty(expr.subtrees[0], indent,with_type_hint)} \n{' ' * indent}{pretty(expr.subtrees[1], indent,with_type_hint)}"
    elif expr.root == 'if':
        return (f"if ({pretty(expr.subtrees[0],0,with_type_hint)}) {'{'}\n{' ' * (indent + 4)}{pretty(expr.subtrees[1], indent + 4,with_type_hint)}\n"
                f"{' ' * indent}{'}'} else {'{'}\n{' ' * (indent + 4)}{pretty(expr.subtrees[2], indent + 4,with_type_hint)}\n{' ' * (indent)}{'}'}")
    elif expr.root == 'while':
        return f"while ( {pretty(expr.subtrees[0],0,with_type_hint)} ) {'{'}\n{' ' * (indent + 4)}{pretty(expr.subtrees[1], indent + 4,with_type_hint)}\n{' ' * (indent)}{'}'}"
    elif expr.root in ['!=', '<=', '>=', '+', "-", '*', '**','/', '<', '>', '==']:
        return f"{pretty(expr.subtrees[1],0,with_type_hint)} {expr.root} {pretty(expr.subtrees[2],0,with_type_hint)}"
    elif expr.root == 'int_val':
        return str(expr.subtrees[1].root)
    elif expr.root == 'float_val':
        return str(expr.subtrees[1].root)
    elif expr.root == 'bool_val':
        return "True" if expr.subtrees[1].root == True else "False"
    elif expr.root == 'id':
        id_ty, id = expr.subtrees[0].subtrees[0].root, expr.subtrees[1].root
        is_decl = getattr(expr, 'is_decl', False)
        if is_decl: 
            return f'{id_ty} {id}'
        else: 
            return f'&{id_ty}& {id}' if with_type_hint else id
    elif expr.root == 'hole':
        return f'?? ({str(expr.subtrees[1].root)})'
    elif expr.root == 'assert':
        return f'assert ({pretty(expr.subtrees[0],0,with_type_hint)}) ;'
    elif expr.root == 'assume':
        return f'assume ({pretty(expr.subtrees[0],0,with_type_hint)}) ;'
    elif expr.root == 'type':
        return f'{expr.subtrees[0]}'
    elif expr.root == 'not':
        return f'not({pretty(expr.subtrees[1],0,with_type_hint)})'
    # FIXME
    # elif expr.root == 'and':
    #     return f'({pretty(expr.subtrees[0],0,with_type_hint)}) and ({pretty(expr.subtrees[1],)})'
    elif expr.root == 'array_pos_assign':
        return f'{pretty(expr.subtrees[0],0,with_type_hint)}[{pretty(expr.subtrees[1],0,with_type_hint)}]'
    elif expr.root == 'array_access':
        return f'{pretty(expr.subtrees[1],0,with_type_hint)}[{pretty(expr.subtrees[2],0,with_type_hint)}]'
    else:
        raise ValueError(f"Unknown expression {expr.root}")




    
if __name__ == '__main__':

    def TestWhileParser(program_text: str, is_valid=True):
        expr = WhileParser()(program_text)
        if expr:
            print(f"{Colors.GREEN}Valid expr{Colors.RESET}")
            print(f"{Colors.YELLOW}expr{Colors.RESET}:\n{expr}")
            print(f"{Colors.YELLOW}pretty(expr){Colors.RESET}:\n{pretty(expr)}")
        else:
            print(f"{Colors.RED}Invalid expr!!{Colors.RESET}")

    
    # expr = WhileParser()("cca := -21")
    # print(f"\nexpr:\n{expr}" if expr else "invalid expr!!")

    TestWhileParser("c := (22 - 2) ; (sx := c)")
    # TestWhileParser("i := 0 ; while (i < n) do ( i := i + 1 )")
    
    
    
    parser = Lark.open('while_lang.lark',  rel_to=__file__, parser='lalr', keep_all_tokens=True)
    
    parser.parse("x := 2 + 2 *4 ; y := 2")
    
    
    # TestWhileParser(r"""x := 2 ** 3 """)
    # TestWhileParser(r"""a := 3 ; b := a ; c := b - 1 ; a := 5""")


    
    # print(WhileParser()(r"""
    #                 if (x = 2) then (
    #                     x := 2 + 2 *4
    #                 )
    #                 """))
    
    # TestWhileParser(r"""
    #                 if (x = 2) then (
    #                     x := 2 + 2 *4
    #                 )
    #                 """)
    # TestWhileParser(r"""
    #                 if (x = 2) then (
    #                     x := 2 + 2 *4 ;
    #                 )else (
    #                     skip;
    #                 )
    #                 """)

    # TestWhileParser(r"""
    #                 while ( b ) 
    #                 invariant ( c1 = 1 )
    #                 do (
    #                     C := c1
    #                 );
    #                 """)
    # TestWhileParser(r"""
    #                 while ( b ) 
    #                 invariant ( c1 = 1 )
    #                 do (
    #                     C := c1
    #                 );
    #                 """)
    # TestWhileParser(r"""
    #                 while ( b ) 
    #                 invariant ( c1 = 1 )
    #                 do (
    #                     C := c1
    #                 )
                    # """)

    # TestWhileParser(r"""
    #                 while ( b ) 
    #                 invariant ( a < 0 or (( b > 0 and s < 0 ) and not ( a = 0 ) ))
    #                 do (
    #                     C := c1
    #                 );
    #                 x := x + 1;
    #                 """)
    # TestWhileParser(r"""
    #                 while ( b ) 
    #                 invariant ( a < 0 or (( b > 0 and s < 0 ) and not ( a = 0 ) ))
    #                 do (
    #                     C := c1
    #                 );
    #                 x := x + 1
    #                 """)
    
    # TestWhileParser(r"""
    #                 while ( b ) do (
    #                     C := c1
    #                 );
    #                 x := 2
    #                 """)

    # TestWhileParser(r"""
    #                 if (b) then (
    #                     C := c1 ;
    #                     while (b) do (
    #                         C := c1
    #                     )
    #                 ) else (
    #                     skip
    #                 );
    #                 x := 2
    #                 """)
    
    # TestWhileParser(r"""
    #                 if (b) then (
    #                     C := c1 ;
    #                     if (b) then (
    #                         C := c1 ;
    #                         while (b) do (
    #                             C := c1
    #                         )
    #                     ) else (
    #                         skip
    #                     )
    #                 ) else (
    #                     skip
    #                 );
    #                 x := 2
    #                 """)
    # #4
    # TestWhileParser(r"""
    #                 if (b) then (
    #                     C := c1 ;
    #                     if (b) then (
    #                         C := c1 ;
    #                         if (b) then (
    #                             assert (1 = 0)
    #                         ) else (
    #                             skip
    #                         )
    #                     ) else (
    #                         skip
    #                     )
    #                 ) else (
    #                     skip
    #                 );
    #                 x := 2
    #                 """)
    
    # TestWhileParser("while x < 2 do x := x + 1 ; z := z + 1 ", is_valid=True)
    
    # # these two are the same
    # TestWhileParser("while (x < 2) do ( (if (x = 2) then (x := x - 1) else (y := y + 1)) ; z := z + 1) ", is_valid=True)
    # TestWhileParser("while x < 2 do (if x = 2 then x := x - 1 else y := y + 1 ; z := z + 1) ", is_valid=True)

    # # these 3 are the same
    # TestWhileParser(r"""
    #                 assume ( x > 0);
    #                 while (x < 2) do ( 
    #                         if (x = 2) then(
    #                             x := x - 1
    #                         ) else (
    #                             y := y + 1
    #                         );
    #                         k := k + 1
    #                     ); 
    #                 z := z + 1
    #                 """, is_valid=True)
    
    # TestWhileParser(" assume ( x > 0) ; while (x < 2) do ( if (x = 2) then (x := x - 1) else (y := y + 1) ; k := k + 1 ) ; z := z + 1 ", is_valid=True)
    # TestWhileParser(" assume ( x > 0) ; while x < 2 do (if x = 2 then x := x - 1 else y := y + 1 ; k := k + 1 ); z := z + 1 ", is_valid=True)
    
    # # these 3 are the same
    # TestWhileParser(r"""
    #                 assume ( x > 0);
    #                 while (x < 2) do ( 
    #                         if (x = 2) then(
    #                             x := x - 1
    #                         ) else (
    #                             y := y + 1
    #                         )
    #                     ); 
    #                 z := z + 1
    #                 """, is_valid=True)
    
    # TestWhileParser(" assume ( x > 0); while (x < 2) do ( if (x = 2) then (x := x - 1) else (y := y + 1) ) ; z := z + 1 ", is_valid=True)
    # TestWhileParser(" assume ( x > 0); while x < 2 do (if x = 2 then x := x - 1 else y := y + 1); z := z + 1 ", is_valid=True)
    
    # TestWhileParser(" assert (x = ( 2 < 0) ) ", is_valid=True)
    # TestWhileParser(" assert (x = ( ( 2 - ( 2 / 2) ) = 0 ) ) ", is_valid=True)
    # TestWhileParser(" assert (x = 2 - 2 / 2 = 0 ) ", is_valid=True)
    # TestWhileParser(" x:= 2*3 ; if (2 > x) then (u := 2 ; y:= 2) else (u := 1 ; y := 1) ; z := 22", is_valid=True)
    # TestWhileParser("while (x < 2) do ( x := x + 1 ; y := y + 1) ; z := z + 1 ", is_valid=True)
    # TestWhileParser("assert (x = 2 - 2 / 2 = 0 ) ; while (x < 2) do ( x := x + 1 ; y := y + 1) ; z := z + 1 ; if (2 > x) then (u := 2 ; y:= 2) else (u := 1 ; y := 1) ; zz := zz + 1", is_valid=True)
    
    
    # # TestWhileParser(" x:= 2*3 + 5 - 3", is_valid=True)
    # # TestWhileParser(" x:= 1 + (2 * 3 )/5 - 10", is_valid=True)
    # # TestWhileParser(" x:= 1 + 2 + 3 ", is_valid=True)
    # # TestWhileParser(" x:= 1 * 2 + 3 ", is_valid=True)
    # # TestWhileParser(" x:= 1 + 2 * 3 ", is_valid=True)
    # # TestWhileParser(" x:= 1 + 2 * 3 - 1 + 2 / 5", is_valid=True)
    # # TestWhileParser(" x:= 10*22 / 1 + 2 * 3 - 1 + 2 / 5", is_valid=True)
    # # TestWhileParser("a := 1 ; while a != b do ( i := i + 1 ; if a > b then a := a - b else b := b - a )", is_valid=True)
    # # TestWhileParser(" k := hole ; num := op; id := id ; assert ?? ", is_valid=True)
    # # TestWhileParser(" k := hole ; num := 2; hole := num ; assert ?? ", is_valid=True)
    # # TestWhileParser(" k := 2 ; assert k > 1 ; assume x = 2; assert (x + 1) = 3", is_valid=True)
    # # TestWhileParser("?? := 0; while (i < ??) do ( i := i + ?? ; j := i + ??)",  is_valid=False)

