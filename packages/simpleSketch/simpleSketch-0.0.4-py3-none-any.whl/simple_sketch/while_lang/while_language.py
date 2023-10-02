"""
* file: while_language.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: The main module for parsing and interacting with the while language. This module
contains the main WhileLang class, which is the entry point for the language.
"""


from typing import Callable, Dict, List, Optional, Set, Tuple, Union, Any, TypeAlias, NewType , Self
import z3
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat, ArithRef, BoolRef
import operator


from simple_sketch.lib.adt.tree import Tree

# from while_lang.syntax import WhileParser, pretty
from simple_sketch.while_lang.syntax.syntax import WhileParser, pretty
from simple_sketch.z3_handler.z3_handler import Z3_TYPE


# For the debugging and the log file
from simple_sketch.utilities.Utilities import Colors, cprint

# TODO: Add log file


# Hole_Id = str
# TODO
# Hole_Id: TypeAlias = z3.ArithRef | str
# Hole_Val: TypeAlias = z3.ArithRef | z3.IntNumRef | int
Hole_Id: TypeAlias = z3.ArithRef
Hole_Val: TypeAlias = z3.ArithRef | z3.IntNumRef

Var_Id: TypeAlias = str
Var_Val: TypeAlias = int

# Define a type for the program environment, the environment is a mapping from variable names to z3 values.
Env_Key: TypeAlias = Var_Id 
Env_Val: TypeAlias = z3.ExprRef
Env: TypeAlias = Dict[Env_Key, Env_Val]
Linv_t: TypeAlias = Callable[[Dict[Env_Key, Env_Val]], z3.BoolRef]

Program_t: TypeAlias = str




class WhileLang():
    """
    WhileLang
    ----------
    The main WhileLang class. For parsing and interacting with the `while_lang`.
    
    IMPORTANT NOTE: 
    ---------------
    The class is assuming that the program has at most one while loop.
    
    Attributes:
    ----------
        * _program_ast (Tree): The abstract syntax tree (AST) of the program.
        * _program (Program_t): The program as string.
    
    Methods:
    -------
        * make_env (Set[str] | None = None) -> Dict[Env_Key, Env_Val]: 
            - Creates a mapping (dictionary) for the given variables, and their z3 variables (z3.ArithRef).
        * program_vars() -> Set[str]: 
            - Returns the set of variables in the program.
        # TODO: ...
    """
    # Define the class attributes
    _program_ast: Tree
    _program: Program_t # The program as string
    
    # Define the class methods
    def __init__(self, program: Program_t | str | None = None, debug: bool =False) -> None:
        """
        WhileLang constructor
        -------
        The constructor for the WhileLang class.
        It parses a program written in the while language, and stores the program as an abstract syntax tree (AST).
        
        IMPORTANT NOTE: 
        ---------------
        The class is assuming that the program has at most one while loop.
        
        Args:
        -----
            * program (Program_t | str | None): A program written in the while language.

        Raises:
        -------
            Exception: If the program is not valid. The program is not valid if it contains a `while_lang` syntax error.
        """
        self.debug = debug
        if program:
            self._program = program
            ast = WhileParser()(program)
            if ast is None:
                raise Exception(f"Failed to parse the program: {program}")
            self._program_ast = ast
            
    
    def from_ast(self, program_ast: Tree) -> 'WhileLang':
        """
        from_ast
        ---------
        Creates a WhileLang object from the abstract syntax tree (AST) of the program.
        
        Args:
        -----
            * program_ast (Tree): The abstract syntax tree (AST) of the program.
        
        Returns:
        --------
            * `WhileLang` object: The WhileLang object.
        
        Note:
        -----
            * The WhileLang object is assumed to have at most one while loop.
        """
        # TODO - IMPORTANT - test if ` pretty(program_ast)` works correctly
        return WhileLang(pretty(program_ast))
        
    
    @property
    def program_ast(self) -> Tree:
        """
        Returns the abstract syntax tree (AST) of the program.
        """
        return self._program_ast
    
    @program_ast.setter
    def program_ast(self, program_ast: Tree) -> None:
        """
        Sets the abstract syntax tree (AST) of the program.
        """
        self._program_ast = program_ast
        # TODO - IMPORTANT - test if ` pretty(program_ast)` works correctly
        self._program = pretty(program_ast)
    
    @property
    def program(self) -> Program_t:
        """
        Returns the program (as string).
        """
        return self._program
    
    @program.setter
    def program(self, program: Program_t | str) -> None:
        """
        Sets the program (as string).
        """
        self._program = program
        ast = WhileParser()(program)
        if ast is None:
            raise Exception(f"Failed to parse the program: {program}")
        self._program_ast = ast
    
    def to_str(self) -> str:
        """
        Returns the program (as string).
        """
        return self.program
        
    def make_env(self, pvars: Set[Tuple[str, str]] | None = None) -> Dict[Env_Key, Env_Val]:
        """
        make_env
        --------
        Creates a mapping (dictionary) for the given variables, and their z3 variables (z3.ArithRef).
        
        Args:
        ----
            * pvars (Set[Tuple[str, str]]):  A set of tuples, where each tuple is a pair of the variable name and its type.
        
        Returns:
        -------
            * env (Dict[Env_Key, Env_Val]): The mapping from variable names to z3 variables (z3.ArithRef).
        """
        if not pvars: pvars = self.program_vars
        env = {}
        for var_id, var_ty in pvars:
            env[var_id] = Z3_TYPE[var_ty](var_id)
        return env

    
    @property
    def program_vars(self) -> Set[Tuple[str, str]]:
        """
        Returns the set of variables in the program.
        
        Return
        ------
            * (Set[Tuple[str, str]]): A set of tuples, where each tuple is a pair of the variable name and its type.
        """
        pvars = set()
        for n in self._program_ast.nodes:
            if len(n.subtrees) == 2 and n.root == "id":
                var_id = n.subtrees[1].root
                var_ty =  n.subtrees[0].subtrees[0].root
                pvars.add((var_id, var_ty))
        return pvars

    @property
    def program_vars_z3(self) -> Set[z3.ArithRef]:
        """
        Returns the set of variables in the program as z3 variables.
        """
        return {z3.Int(v.subtrees[0].root)for v in self._program_ast.nodes if len(v.subtrees) == 1 and v.root == "id"}

    @property
    def program_holes(self) -> Set[Tuple[str, str]]:
        """
        Returns the set of holes in the program.
        """
        pholes = set()
        for n in self._program_ast.nodes:
            if len(n.subtrees) == 2 and n.root == "hole":
                var_id = n.subtrees[1].root
                var_ty =  n.subtrees[0].subtrees[0].root
                pholes.add((var_id, var_ty))
        return pholes

    @property
    def program_holes_z3(self) -> Set[z3.ArithRef]:
        """
        Returns the set of holes in the program as z3 variables.
        """
        return {z3.Int(v.subtrees[0].root) for v in self._program_ast.nodes if len(v.subtrees) == 1 and v.root == "hole"}

    
    def substitute(self, var: Var_Id, value: Var_Val) -> None:
        """
        Substitute the variable `var` with the value `value` in the `program`.
        If the variable does not exist in the program, raise an exception.
        """
        #TODO
        pass 
    
    def assign_hole_values(self, holes_values : Dict[Hole_Id, Hole_Val] | None) -> 'WhileLang':
        """
        assign_hole_values _summary_

        Args:
            holes_values (Dict[Hole_Id, Hole_Val]): _description_

        Returns:
            WhileLang: new copy of the program with the holes filled.
        """
        # Fill the holes (the C_i's), in the program i.e. replace the `hole` token with an integer.
        # holes_values {hole_id : hole_value}
        filled_program = self.clone()
        # TODO: test if the `self.program` is changed correctly
        if holes_values: filled_program.program_ast = self._assign_hole_values(self.program_ast, holes_values)
        return filled_program

    @classmethod
    def _assign_hole_values(cls, program_ast: Tree, holes_values : Dict[Hole_Id, Hole_Val]) -> Tree:
        # Fill the holes (the C_i's) in the program. i.e. replace the `hole` token with an integer.
        # holes_values {hole_id : hole_value}
        if program_ast.root == 'hole' and len(program_ast.subtrees) == 2:
            hole_ty_val = f"{program_ast.subtrees[0].subtrees[0].root}_val"
            
            hole_id = Z3_TYPE[hole_ty_val[:-4]](program_ast.subtrees[1].root)
            hole_val = Z3_TYPE[hole_ty_val](holes_values[hole_id])
            
            ty_node =  program_ast.subtrees[0]
            new_node = Tree(hole_ty_val, [ty_node, Tree(hole_val)])
            

            return new_node
        else:
            for i in range(len(program_ast.subtrees)):
                program_ast.subtrees[i] = cls._assign_hole_values(program_ast.subtrees[i], holes_values)
        return program_ast
    
    def clone(self) -> 'WhileLang':
        """
        Returns a copy of the current WhileLang object.
        """
        return WhileLang(self.program)
    
    def get_while_loop_body(self) -> Tree | None:
        """
        Returns the body of the while loop in the program.
        If the program does not contain a while loop, return None.
        
        # Note: 
        The class is assuming that the program has at most one while loop.
        
        Returns:
            Tree | None: The body of the while loop.
        """
        while_body = None
        for node in self.program_ast.nodes:
            if node.root == "while":
                while_body = node.subtrees[1].clone()
                break
        return while_body
    
    def get_while_loop(self) -> Union['WhileLang', None]:
        """
        # TODO: maybe use `unroll_while_loops` to also return the `while loop` before unrolling it
        
        Returns the WhileLang program of the while loop in the program.
        If the program does not contain a while loop, return None.
        
        # Note: 
        The class is assuming that the program has at most one while loop.
        
        Returns:
            WhileLang | None: The WhileLang program of the while loop.
        """
        # TODO: maybe use `unroll_while_loops` to also return the `while loop` before unrolling it
        while_prog = None
        for node in self.program_ast.nodes:
            if node.root == "while":
                while_prog = WhileLang(pretty(node))
                break
        return while_prog
    
    def unroll_while_loops(self, N: int) -> 'WhileLang':
        """
        unroll_while_loops
        -------------------
        Unroll all while loops in the program N times.
        
        Unrolling loops - The Idea:
        ---------------------------
        The idea is to exploit the following identity 
        (to replace the while loop with a sequence of statements that are equivalent to the loop):
        ```
        while (b) do C ≡ if (b) then (C; while (b) do C) else skip
        ```
                
        Unrolling the loop means applying this equivalence repeatedly. 
        At some point we must stop the conversion and we simply replace the while loop with `assert false;`. 
        This assertion means that if there is any input that would have caused the loop to iterate more, 
        then that input will cause an assertion failure. 
        
        This means that the loop unrolling generally has to be accompanied by an assumption on the inputs 
        that will prevent inputs that would have caused the loop to iterate too much.
        
        Note:
        -----
        The class is assuming that the program has at most one while loop.
        
        Args:
        ----
            * N (int): The number of times to unroll the while loops.
        
        Returns:
        -------
            * unrolled_prog (WhileLang): The unrolled program.
        """
        unrolled_prog = self.clone()
        unrolled_prog.program_ast = unrolled_prog._unroll_while_loops(unrolled_prog.program_ast, N)
        return unrolled_prog

    @classmethod
    def _unroll_while_loops(cls, prog_ast: Tree, N: int) -> Tree:
        """
        _unroll_while_loops
        -------------------
        Helper function for `unroll_while_loops`. 
        Recursively unroll all while loops in the program N times.

        Args:
            N (int): _description_

        Returns:
            WhileLang: _description_
        """
        if prog_ast.root == "while":
            assert N >= 0 , f"N({N}) must be >= 0"
            b = prog_ast.subtrees[0].clone() #TODO: maybe we don't need to clone here
            then_ = None
            if N > 0:
                # Unroll the while loop once
                while_node = prog_ast.clone()
                c = prog_ast.subtrees[1].clone() #TODO: maybe we don't need to clone here
                then_ = Tree(';', [c, while_node])
                # else_ = Tree('skip', [Tree('skip')]) #  WhileLang("skip").program_ast
                # new_root = Tree('if', [b, then_, else_])
                # prog_ast = new_root
            if N == 0:
                # insert an assertion that will fail if the loop would have iterated more than N times
                # TODO: check how to do this (`Tree('false')`) instead of `1=0`
                # assert_false = Tree('false')
                # assert_false = Tree('==', [Tree('num', [Tree(1)]), Tree('num', [Tree(0)])]) # 1 = 0
                # TODO: check this instead
                # then_ = Tree('assert', [assert_false])
                then_ = WhileLang("assert (False);").program_ast
            
            assert then_ is not None   
            #TODO: else_ = WhileLang("skip").program_ast
            else_ = Tree('skip', [Tree('skip')])
            new_root = Tree('if', [b, then_, else_])
            prog_ast = new_root
            
            # TODO: N = N - 1 ??
            if N > 0: # then_.root == ";":
                prog_ast.subtrees[1].subtrees[1] = cls._unroll_while_loops(prog_ast.subtrees[1].subtrees[1], N-1)
            return prog_ast
        else:
            for i in range(len(prog_ast.subtrees)):
                prog_ast.subtrees[i] = cls._unroll_while_loops(prog_ast.subtrees[i], N)
            return prog_ast
            
        
    
    def  __str__(self) -> str:
        #TODO
        return f"{self.program}"

    def __repr__(self) -> str:
        #TODO
        return f"{self.program}"

    def __eq__(self, other: object) -> bool:
        #TODO
        if isinstance(other, WhileLang):
            return self.program == other.program
        else:
            return False
