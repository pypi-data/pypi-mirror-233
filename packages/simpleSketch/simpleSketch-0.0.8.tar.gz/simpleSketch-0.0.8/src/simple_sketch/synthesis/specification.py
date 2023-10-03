"""
* file: specification.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: specification module for the project. This module contains the
specification class, which is used to represent the specification of the program.
"""




from typing import Callable, Dict, List, Union, Set, Tuple
import z3

from simple_sketch.while_lang.while_language import  Env

from simple_sketch.z3_handler.z3_text_parser import Z3Parser



Spec_t = List[z3.BoolRef] # assertions in the specification

class Spec_Example:
    """
    A class for the input/output example in the specification.
    
    # TODO:
    ## change `input_example` and `output_example` to be `str` instead of `Callable[[Env], z3.BoolRef]`,
    ## and call the `Z3Parser` to parse them into z3 expressions, and generate the `Callable[[Env], z3.BoolRef]`
    """
    input_example: Callable[[Env], z3.BoolRef]
    output_example: Callable[[Env], z3.BoolRef]
    
    def __init__(self, 
                input_example: Callable[[Env], z3.BoolRef]  | Tuple[str, str], 
                output_example: Callable[[Env], z3.BoolRef] | Tuple[str, str]
                ) -> None:
        """
        Initialize the input/output example.
         
        """
        # TODO: check if the type of `input_example` and `output_example` is str, 
        #  if so, use `z3_text_parser` to parse them into z3 expressions, and `Callable[[Env], z3.BoolRef]`
        
        self.in_env = {}
        self.in_vars: Set[Tuple[str, str]] = set()
        self.out_env = {}
        self.out_vars: Set[Tuple[str, str]] = set()
        
        if isinstance(input_example, Tuple):
            # TODO:  check how to use `z3.parse_smt2_string`
            z3_expr = Z3Parser()(z3_text=input_example[0], types=input_example[1]) # TODO: need testing
            if z3_expr is None:
                raise ValueError(f"Invalid z3 expression: {input_example}")
            input_example = z3_expr[0]
            self.in_env = z3_expr[1]
            self.in_vars = {(var, ty) for var, ty in z3_expr[3].items()}
        else:
            input_example = input_example
        
        if isinstance(output_example, Tuple):
            # TODO:  check how to use `z3.parse_smt2_string`
            # self.specification[key] = z3.parse_smt2_string(expr) 
            z3_expr = Z3Parser()(z3_text=output_example[0],types=output_example[1]) # TODO: need testing
            if z3_expr is None:
                raise ValueError(f"Invalid z3 expression: {output_example}")
            output_example = z3_expr[0]
            self.out_env = z3_expr[1]
            self.out_vars = {(var, ty) for var, ty in z3_expr[3].items()}
        else:
            output_example = output_example
        
        self.inout_vars = self.in_vars.union(self.out_vars)
        self.inout_env = {**self.in_env, **{k: v for k, v in self.out_env.items() if k not in self.in_env}}
        self.input_example = input_example
        self.output_example = output_example
    
    def __call__(self, env: Env) -> Tuple[z3.BoolRef, z3.BoolRef]:
        """
        Return the input/output example as a tuple of z3 expressions.
        """
        return (self.input_example(env), self.output_example(env))
    
    def __repr__(self):
        return f"({self.input_example}, {self.output_example})"
    
    def __str__(self):
        # TODO: test it
        from inspect import getsource
        input_example_str = getsource(self.input_example)
        output_example_str = getsource(self.output_example)
        return f"({input_example_str}, {output_example_str})"


class Specification:
    """
    A class for the specification of the program.
    """
    
    def __init__(self, 
                input_output_examples: List[Spec_Example] = [],
                pre_condition: Tuple[str, str] | None = None,
                post_condition: Tuple[str, str] | None = None,
                loop_inv: Tuple[str, str] | None = None,
                **kwargs: Union[str, z3.BoolRef, Callable[[Env], z3.BoolRef] ]
                ) -> None:
        """
        Initialize the specification.
        """
        
        self.input_output_examples = input_output_examples
        self.__init_spec(pre_condition, post_condition, loop_inv)
        
        # TODO: check if needed
        # store the specification as dictionary of z3 expressions
        self._specification: Dict[str, Tuple[Callable[[Env], z3.BoolRef], Env]] = {}
        
        # TODO: check if needed
        for key, expr in kwargs.items():
            if isinstance(expr, str):
                # TODO:  check how to use `z3.parse_smt2_string`
                # self.specification[key] = z3.parse_smt2_string(expr) 
                z3_expr = Z3Parser()(z3_text=expr) # TODO: need testing
                if z3_expr is None:
                    raise ValueError(f"Invalid z3 expression: {expr}")
                # TODO: check what best to use. Maybe store the (z3_expr[0], z3_expr[1])?
                # self._specification[key] = z3_expr[0](z3_expr[1])
                self._specification[key] = z3_expr[0], z3_expr[1]
                
            # elif isinstance(expr, z3.BoolRef):
            #     # TODO: Need to test it and FIX it
            #     self._specification[key] = (lambda _: expr, self.__make_env(expr))
            elif isinstance(expr, Callable):
                self._specification[key] = (expr, {})
            else:
                raise ValueError(f"Invalid type {type(expr)} of value: {expr}")
            
    def __init_spec(
        self,
        pre_condition: Tuple[str, str] | None = None,
        post_condition: Tuple[str, str] | None = None,
        loop_inv: Tuple[str, str] | None = None 
        ):
        
        # FIXME: make it look better
        pre_cond = pre_condition if pre_condition else ("True", {})
        try:
            e = Z3Parser().parse(pre_cond[0], pre_cond[1])
            if e is None: 
                raise ValueError(f"Invalid pre-condition: {pre_cond}")
        except Exception as e:
            e.add_note(f"ERROR - Z3Parser - Invalid pre-condition:\n{pre_cond}")
            raise 
            
        self.pre_condition: Callable[[Env], z3.BoolRef] = e[0]
        self.pre_condition_env: Env = e[1]
        self.pre_condition_vars: Set[Tuple[str, str]] = {(var, ty) for var, ty in e[3].items()}

        post_cond = post_condition if post_condition else ("True", {})
        try:
            e = Z3Parser().parse(post_cond[0], post_cond[1])
            if e is None: 
                raise ValueError(f"Invalid post-condition: {post_cond}")
        except Exception as e:
            e.add_note(f"ERROR - Z3Parser - Invalid post-condition:\n{post_cond}")
            raise 
        self.post_condition: Callable[[Env], z3.BoolRef] = e[0]
        self.post_condition_env: Env = e[1]
        self.post_condition_vars: Set[Tuple[str, str]] = {(var, ty) for var, ty in e[3].items()}

        self.loop_inv: Callable[[Env], z3.BoolRef] | None = None
        self.loop_inv_env: Env = {}
        self.loop_inv_vars: Set[Tuple[str, str]] = set()

        if loop_inv:
            try:
                e = Z3Parser().parse(loop_inv[0], loop_inv[1])
                if e is None: 
                    raise ValueError(f"Invalid loop inv: {loop_inv}")
            except Exception as e:
                e.add_note(f"ERROR - Z3Parser - Invalid loop-inv:\n{loop_inv}")
                raise 
            self.loop_inv: Callable[[Env], z3.BoolRef] | None = e[0]
            self.loop_inv_env: Env = e[1]
            self.loop_inv_vars: Set[Tuple[str, str]] = {(var, ty) for var, ty in e[3].items()}
     
     
     
    @property
    def expected_verify_res(self) -> bool:
        """
        Return the expected verification result. (Default: True)
        """
        return self._expected_verify_res
    
    @expected_verify_res.setter
    def expected_verify_res(self, expected_verify_res: bool) -> None:
        self._expected_verify_res = expected_verify_res
    
    
    @property
    def specification(self) -> Dict[str, Tuple[Callable[[Env], z3.BoolRef], Env]]:
        """
        Return the specification as a dictionary of z3 expressions (z3.BoolRef).
        """
        return self._specification
    

        
    def __getitem__(self, key: str) -> Tuple[(z3.BoolRef | Callable[[Env], z3.BoolRef]), Env]:
        """
        Return the z3 expression (z3.BoolRef) of the specification with the key `key`.
        """
        return self._specification[key]
    
    def __contains__(self, key: str) -> bool:
        """
        Return True if the specification contains the key `key`, otherwise return False.
        """
        return key in self._specification
    
    def get(self, key: str):
        """
        Return the z3 expression (z3.BoolRef) of the specification with the key `key`.
         If the key does not exist, return the default value (z3.BoolVal(True), {}).
        """
        return self._specification.get(key, (lambda _ : z3.BoolVal(True), {}))
