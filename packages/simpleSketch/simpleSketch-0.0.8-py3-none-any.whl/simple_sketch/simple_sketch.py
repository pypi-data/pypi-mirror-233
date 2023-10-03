"""
 - file: simple_sketch.py
 - author: Maher Bisan 
 - date: September 2023
 - description: Simple Sketch module for the project. 
    This module contains the simple sketch class, which is used to represent the simple sketch of the program.
"""


from typing import List, Tuple, TypeAlias

from .synthesis.specification import Specification, Spec_Example
from .synthesis.synthesizer import Synthesizer

from .utilities.Utilities import Colors
#TODO: change the `if self.debug` and the print to Log file



class SimpleSketch:
    """
    A simple sketch class. To synthesize a simple program in the `while_lang` language.
    """
    
    Example: TypeAlias = Tuple[str, str]
    
    
    def __init__(self, timeout: int = 100, max_itr_num: int = 10, num_to_unroll_while_loops: int = 8, debug: bool = False):
        """
        Initialize the simple sketch.
        
        Args
        -----
        * `timeout` (int): the timeout for solving the z3 problem.
        * `max_itr_num` (int): the maximum number of iterations for solving the z3 problem.
        * `num_to_unroll_while_loops` (int): the number of while loops to unroll.
        * `debug` (bool): the debug mode.
        
        
        Example
        -------
        ```
        >>> simple_sketch = SimpleSketch()
        >>> simple_sketch.timeout = 100
        >>> simple_sketch.max_itr_num = 10
        >>> simple_sketch.num_to_unroll_while_loops = 8
        ```
        Note
        ----
        * `timeout` and `max_itr_num` are used for solving the z3 problem.
        * `num_to_unroll_while_loops` is used for unrolling the while loops.
        """
        self.timeout = timeout
        self.max_itr_num = max_itr_num
        self.num_to_unroll_while_loops = num_to_unroll_while_loops
        self.debug = debug
        
    def synthesize(self, 
                    program: str,
                    input_output_examples: List[Tuple[str, str,str]]  = [],
                    pre_condition: str = "",
                    post_condition: str = "",
                    loop_inv: str = "",
                    vars_types: str = "",
                    ):
        """
         Synthesize a simple program in the `while_lang` language.
        
        Args
        -----
        * `program` (str): the program in the `while_lang` language.
        * `input_output_examples` (List[Tuple[str, str, str]]): the input/output examples of the program, each example is a tuple of (input, output, vars_types).
        * `pre_condition` (str): the pre-condition of the program (including the types of the variables).
                - syntax: `condition --types={var1 : type1, var2 : type2, ...}`.
        * `post_condition` (str): the post-condition of the program.
                - syntax: `condition --types={var1 : type1, var2 : type2, ...}`
        * `loop_inv` (str): the loop-inv of the program.
                - syntax: `condition --types={var1 : type1, var2 : type2, ...}`
        * `vars_types` (str): the types of the variables.
        
        Note
        -----
        * The default type of variables is 'int' if not specified
        * In `pre_condition`, `post_condition`, `loop_inv`, and `vars_types`.
                * `condition` is in Z3 syntax.
                * `--types` is optional.
                * `var{i}` : is the name of the variable.
                * `type{i}` is the type of the variable `var1`.
                * `type{i}` can be one of the following types: `int`, `bool`, `Array int`, `Array bool`.
                * The types of the variables should be the same as the variables in the program.

        Returns
        -------
        * `synthesized_program` (str): the synthesized program.
        * `hole_values` (Dict[str, str]): the hole values.
        * `verify_res` (bool): the verification result.
        * `verify_examples_res` (bool): the verification examples result.
        
        Example
        -------
        ```
        >>> simple_sketch = SimpleSketch()
        >>> program = r'''
                    bool b := True; int x := x0; 
                    while (b) { 
                        if (x <= 5) {b := ??==1;}
                        x := x - 1; 
                    }
                '''
        >>> input_output_examples = [("x0 == 10", "x == 5", "{x0 : int}"), 
                                     ("x0 == 0", "x == 0", "{x0 : int}")]
        >>> pre_condition = "And(x0 >= 0) --types={x0 : int}"
        >>> post_condition = "And(x <= 5, Not(b1 == b)) --types={x : int, b1: bool}"
        >>> loop_inv = "And(x >= 0, x <= 10, b == (x <= 5)) --types={x : int, b : bool}"
        >>> simple_sketch.synthesize(program, input_output_examples, pre_condition, post_condition, loop_inv)
        ```
        """
        # TODO: Add main `pvars` dictionary to be using with the `pvars` of the program
        # and with `inout_examples`, `pre_condition`, `post_condition`, `loop_inv`
        # FIXME: Implement the support for `vars_types` dictionary
        
        synthesizer = Synthesizer(
                                program = program,
                                timeout = self.timeout, 
                                max_itr_num = self.max_itr_num, 
                                num_to_unroll_while_loops = self.num_to_unroll_while_loops,
                                debug=self.debug
                            )
        
        inout_examples = [Spec_Example((in_e, vars_types), (out_e, vars_types)) 
                          for in_e, out_e, vars_types in input_output_examples]
        
        # "And(x0 >= 0) --types={x0 : int}" --> ("And(x0 >= 0)", "{x0 : int}")
        def parse_cond(condition: str) -> Tuple[str, str]:
            conds = condition.split("--types=")
            if len(conds) == 1:
                # case: "And(x0 >= 0)"
                conditions = ("True" if conds[0].strip() == "" else conds[0], "")
            else:
                # case: "And(x0 >= 0) --types={x0 : int}"
                conditions = ("True" if conds[0].strip() == "" else conds[0], conds[1])
            return conditions
        
        
        spec = Specification(inout_examples, parse_cond(pre_condition), 
                            parse_cond(post_condition), parse_cond(loop_inv))
        
        synthesizer_res = synthesizer.synthesize(spec)
        synthesized_program = synthesizer_res[0]
        hole_values = synthesizer_res[1]
        verify_res = synthesizer_res[2]
        verify_examples_res = synthesizer_res[3]
        
        if verify_res and verify_examples_res:
            print(f"{Colors.GREEN}The synthesized program is correct.{Colors.RESET}")
            print(f"{Colors.BRIGHT_BLUE}The Holes values are:\n{Colors.RESET}{hole_values}")
            print(f"{Colors.BRIGHT_BLUE}The final synthesized program:\n{Colors.RESET}{synthesized_program}")
            return synthesizer_res
        else:
            print(f"{Colors.RED}The synthesized program is not correct.{Colors.RESET}")
            print(f"{Colors.RED}You may Try to:{Colors.RESET}")
            print(f"{Colors.MAGENTA}{Colors.BOLD} 1. If you have `loop inv`, make SURE it CORRECT!!{Colors.RESET}")
            print(f"{Colors.BRIGHT_MAGENTA}",
                  "2. Increase the `timeout` and/or the `max_itr_num`\n",
                  "3. Increase the `num_to_unroll_while_loops`\n",
                  "4. Change the input/output examples\n",
                  "5. Change the specification\n",
                  "6. Check if the `loop_inv` is correct",
                  Colors.RESET)
            return None
    
    
    
    
    
