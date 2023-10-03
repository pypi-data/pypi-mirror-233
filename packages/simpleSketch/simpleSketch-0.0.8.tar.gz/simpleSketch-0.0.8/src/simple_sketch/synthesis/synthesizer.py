"""
* file: synthesizer.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: synthesizer module for the project. This module contains the
synthesizer class, which is used to synthesize a given input file.
"""



from typing import Dict, List, Set, Tuple
import z3

from .cegis import Cegis
from simple_sketch.verifier import wp

from simple_sketch.z3_handler.z3_handler import  print_z3
from simple_sketch.while_lang.while_language import WhileLang, Env, Env_Key, Env_Val, Hole_Id, Hole_Val, Program_t

from .specification import Specification, Spec_Example

from simple_sketch.utilities import Colors
#TODO: change the `if  self.debug` and the print to Log file

class Synthesizer:
    """
    # TODO: Also, add jupyter notebook for examples of how to use the synthesizer. With formulas `∃C, ∀X, phi -> psi`
    Synthesizer class.
    """
    _while_program: WhileLang | None
    _synthesized_program: WhileLang | None
    timeout: int
    specification: Specification | None
    input_output_examples: List[Spec_Example]
    
    def __init__(self,
                program: Program_t | str | None = None,
                timeout: int = 100,
                max_itr_num: int = 10, 
                num_to_unroll_while_loops: int = 8,
                debug: bool = False
                ):
        """
        Initialize the synthesizer.
        
        Args:
        ----
            * `program` (Program_t | str | None): The program to synthesize.
            * `timeout` (int): The timeout for the cegis loop.
            * `max_itr_num` (int): The maximum number of iterations for the cegis loop. 
            * `num_to_unroll_while_loops` (int): The number of times to unroll the while loops.
            * `debug` (bool): The debug mode.
        
        """
        # TODO: handel the `timeout` and `max_itr_num` in the `cegis` class
        self.timeout = timeout
        self.max_itr_num = max_itr_num
        self.debug = debug
        self.num_to_unroll_while_loops = num_to_unroll_while_loops
        self._synthesized_program = None
        self._while_program = None
        self._while_free_program = None
        if program:
            self._while_program = WhileLang(program)
            self._while_free_program = self._while_program.unroll_while_loops(N=self.num_to_unroll_while_loops )
        
    @property
    def while_program(self) -> WhileLang:
        """ 
        Return the `while_lang` program.
        """
        return self._while_program
    @property
    def while_free_program(self) -> WhileLang:
        """ 
        Return the `while_lang` program without loops.
        """
        return self._while_free_program
    
    
    @while_program.setter
    def while_program(self, while_program: WhileLang | Program_t) -> None:
        if isinstance(while_program, WhileLang):
            self._while_program = while_program
        elif isinstance(while_program, Program_t):
            self._while_program = WhileLang(while_program)
        else:
            raise TypeError(f"Expected a `WhileLang` or a `Program_t` but got a `{type(while_program)}`")
        self._while_free_program = self._while_program.unroll_while_loops(N=self.num_to_unroll_while_loops )
        self._synthesized_program = None
    
    def get_synthesized_program(self) -> WhileLang:
        """
        Return the synthesized program.
        """
        # TODO: check if this is the right way to raise an exception, or to handel this in another way?
        # maybe return `None`?
        if self._synthesized_program is None:
            raise Exception("No synthesized program yet.")
        return self._synthesized_program
    
    def __extend_env(self, env1: Env, env2: Env) -> Env:
        """
        Extend the `env1` with the items of `env2`, only of there keys are not in `env1`.
        """
        # return {**env2, **env1}
        return {**env1, **{k: v for k, v in env2.items() if k not in env1}}
    
    def try_to_synthesize(self,
                          specification: Specification | None
                          ) -> Tuple[WhileLang, Dict[Hole_Id, Hole_Val]]:
        
        specification = specification if specification is not None else Specification()
        
        self.input_output_examples = specification.input_output_examples
        p_vars = self.while_free_program.program_vars
        p_holes = self.while_free_program.program_holes
        p_env = self.while_free_program.make_env()
        
        def union(s1: Set[Tuple[str,str]], s2: Set[Tuple[str,str]]) -> Set[Tuple[str,str]]:
            "union two sets of type `Set[Tuple[str,str]]` by the first element of the tuple"
            s1_keys = {k for k, _ in s1}
            s = s1.copy()
            s.update({(var, ty) for var, ty in s2 if var not in s1_keys})
            return s
        
        p_vars = union(p_vars, union(specification.pre_condition_vars, specification.post_condition_vars))
        p_env = self.__extend_env(p_env,  self.__extend_env(specification.pre_condition_env, specification.post_condition_env,))
        
        # TODO: check if we should add the pre-condition and the post-condition to the verification conditions and the assumptions
        assumptions = [specification.pre_condition(p_env)]
        verification_conditions = [wp.wp(self.while_free_program.program_ast, specification.post_condition)(p_env)]
        
        # extract the input and output examples
        for e in self.input_output_examples:
            # Check if `assumptions[last_i] == verification_conditions[last_i] == True`,
            # if so remove them to avoid unnecessary computation
            if z3.eq(assumptions[0], z3.BoolVal(True)) and z3.eq(verification_conditions[0], z3.BoolVal(True)):
                assumptions.pop()
                verification_conditions.pop()
            penv = self.__extend_env(p_env, self.__extend_env(e.in_env, e.out_env))
            p_vars = union(p_vars, union(e.in_vars, e.out_vars))
            assumptions.append(e.input_example(penv))
            verification_conditions.append(
                wp.wp(self.while_free_program.program_ast, e.output_example, None)(penv))

        X_in = p_vars.difference(p_holes)
        
        if self.debug:
            print("while free program:", self.while_free_program.to_str())
            print("p_env:", p_env)
            print_z3(assumptions, "assumptions:")
            print_z3(verification_conditions, "verification_conditions:")
            print("X:", X_in)
            print("C:", p_holes)
   
        if  self.debug:
            print(assumptions, "assumptions:")
            print(verification_conditions, "verification_conditions:")
        
        cegis_solver = Cegis(verification_conditions, assumptions=assumptions, X=X_in, C=p_holes, 
                            timeout=self.timeout, max_itr_num=self.max_itr_num)

        # call the cegis algorithm
        holes_vals = cegis_solver.cegis_loop()
        filled_program = self.fill_holes(holes_vals)
        self._synthesized_program = filled_program
        return filled_program ,holes_vals
    
    def synthesize(self, 
                   specification: Specification | None
                   ) -> Tuple[WhileLang, Dict[Hole_Id, Hole_Val], bool, bool]:
        """
        Synthesize a program that satisfies the given specification.
        And fill the holes in the `program` and return the program with the correctly (hopefully) filled values for the holes.
        
        Args:
        -----
            * specification (Specification | None): the specification to be synthesized. 
        
        Returns:
        -------
            * Tuple[WhileLang, Dict[Hole_Id, Hole_Val], bool, bool]:
                    - filled_program (WhileLang): the filled program with the holes values filled.
                    - holes_vals (Dict[Hole_Id, Hole_Val] | None): the holes values, if the program was filled successfully, otherwise `None`.
                    - verify_res (bool): if the program is verified by the specification.
                    - verify_examples_res (bool): if the program is verified by the input/output examples.
            
        Raises:
            ValueError: if the specification is not valid. 
            
        """
        
        specification = specification if specification is not None else Specification()
        self.specification = specification
        filled_program, holes_vals = self.try_to_synthesize(specification)
        # verify the filled program for the input/output examples: {input}program{output}
        verify_examples_res = self.verify_filled_program_examples(filled_program, self.specification)
        # verify the filled program for: `{P}program{Q}`
        verify_res = self.verify_filled_program(filled_program, self.specification)
        
        if  self.debug:
            print(f"{Colors.YELLOW}\n>>> filled_program:{Colors.RESET}\n", filled_program.to_str())
            print(f"{Colors.YELLOW}>>> holes_vals:{Colors.RESET}\n", holes_vals)
        
        return filled_program, holes_vals, verify_res, verify_examples_res
        
    
    def fill_holes(self, holes_vals: Dict[Hole_Id, Hole_Val]) -> WhileLang:
        """
        Fill the holes in the given program. 
        """
        filled_prog = self.while_program.assign_hole_values(holes_vals)
        return filled_prog
    
    def verify_filled_program_examples(self, filled_program: WhileLang, specification: Specification) -> bool:
        """
         Verify the program with the final holes values as returned from `synthesize` for the input/output examples.

        Args:
            filled_program (WhileLang): the filled program with the holes values filled.
            specification (Specification): the specification to be synthesized. 
        
        Returns:
        -------
            `True` if the program is verified by the input/output examples, otherwise `False`.
        """
        verify_examples_res = True
        input_output_examples = specification.input_output_examples
        for e in input_output_examples:
            res = wp.verify(
                P = e.input_example,
                program = filled_program,
                Q = e.output_example,
                linv = specification.loop_inv,
                pvars = e.inout_vars.union(specification.loop_inv_vars),
                env = self.__extend_env(e.inout_env, specification.loop_inv_env)
            )
            if res == False:
                verify_examples_res = False
                print(f"{Colors.RED}\n>>> The program is incorrect for the following input/output example:\n{Colors.RESET}")
                print(f"{Colors.BRIGHT_BLUE}>>> input example:\n{Colors.RESET}", e.input_example(e.in_env))
                print(f"{Colors.BRIGHT_BLUE}>>> output example:\n{Colors.RESET}", e.output_example(e.out_env))
            else:
                print(f"{Colors.GREEN}\n>>> The program is correct for the following input/output example:\n{Colors.RESET}")
                print(f"{Colors.BRIGHT_BLUE}>>> input example:\n{Colors.RESET}", e.input_example(e.in_env))
                print(f"{Colors.BRIGHT_BLUE}>>> output example:\n{Colors.RESET}", e.output_example(e.out_env))
        
        return verify_examples_res
       
    
    def verify_filled_program(self, filled_program: WhileLang, specification: Specification) -> bool:
        """
        Verify the program with the final holes values as returned from `synthesize` for the specification: 
        `{Pre-cond}program{Post-cond} && {linv}`. 
        
        Args:
            filled_program (WhileLang): the filled program with the holes values filled.
            specification (Specification): the specification to be synthesized. 
        
        Returns:
        -------
            `True` if the program is verified by the specification, otherwise `False`.
        """
        print(f"{Colors.YELLOW}\n>>> Verifying the program ...{Colors.RESET}\n")
        
        pre_cond, pre_env, pre_vars = specification.pre_condition, specification.pre_condition_env, specification.pre_condition_vars
        post_cond, post_env, post_vars = specification.post_condition, specification.post_condition_env, specification.post_condition_vars
        linv_cond, linv_env, linv_vars = specification.loop_inv, specification.loop_inv_env, specification.loop_inv_vars
        
        p_vars = pre_vars.union(post_vars).union(linv_vars)
        p_env = self.__extend_env(pre_env,  self.__extend_env(post_env, linv_env))
        
        res = wp.verify(
            P= pre_cond,
            program= filled_program,
            Q= post_cond,
            linv= linv_cond,
            pvars= p_vars,
            env= p_env
        )
            
        if res:
            print(f"{Colors.GREEN}\n>>> The program is correct!{Colors.RESET}\n")
            self._synthesized_program = filled_program
        else: 
            print(f"{Colors.RED}\n>>> The program is incorrect!{Colors.RESET}\n")
        
        return res
    
    
    def check_program_equivalence(self, program1: Program_t, program2: Program_t) -> bool:
        """
        Check if the two given programs are equivalent (program1 <==> program2)
            - program1 ==>(implies) program2: program1 is stronger than program2, which mean that for all inputs, if program1 terminates with output o, then program2 terminates with output o.
            - program2 ==>(implies) program1: program2 is stronger than program1, which mean that for all inputs, if program2 terminates with output o, then program1 terminates with output o.
        """
        pass
    
    def check_specification_equivalence(self, spec1: Specification | None, spec2 : Specification | None) -> bool:
        """
        Check if the two given specifications are equivalent.
        """
        pass
    
