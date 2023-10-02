"""
* file: cegis.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: cegis module for the project.
This module contains the Cegis class, which implements the CEGIS algorithm to synthesize a program.
"""


# 

from typing import Dict, List, Set, Tuple
import z3

from simple_sketch.z3_handler import solve_z3, substitute_z3
from simple_sketch.z3_handler import Z3_TYPE, Z3_VAL

from simple_sketch.while_lang.while_language import  Hole_Id, Hole_Val

from simple_sketch.utilities import Colors, cprint
#TODO: change the `if self.debug` and the print to Log file

class Cegis():
    """
    Cegis
    ------
    Counter Example Guided Inductive Synthesis (CEGIS) algorithm.
    # TODO: ...
    
    Attributes:
    ----------
        * verification_conditions (List[z3.BoolRef]): The verification conditions of the program.
        * assumptions (List[z3.BoolRef]): The assumptions of the program.
        * max_itr_num (int): The maximum number of iterations to run the CEGIS loop.
        * timeout (int): The timeout for each iteration of the CEGIS loop (the timeout for the solver).
        # TODO:...
    
    Methods:
    -------
        * # TODO:...
    """
    # * `verification_conditions` is a list of Z3 formulas, each formula is a `ForAll` expression, where the variables are the input variables of the program, and the body is the output variables of the program.
    
    FOUND_NEW_C_VALS: bool = True
    NO_NEW_C_VALS: bool = False
    verification_conditions: List[z3.BoolRef]
    assumptions: List[z3.BoolRef]
    max_itr_num: int
    timeout: int
    
    def __init__(self,
                verification_conditions : List[z3.BoolRef],
                assumptions: List[z3.BoolRef],
                X: Set[Tuple[str,str]],
                C: Set[Tuple[str,str]],
                max_itr_num: int = 5,
                timeout: int = 1000,
                debug: bool = False
                ) -> None:
        """
        Initialize the Cegis algorithm.
        
        Args:
            * `verification_conditions` (List[z3.BoolRef]): The verification conditions of the program.
            * `assumptions` (List[z3.BoolRef]): The assumptions of the program.
            * `X` (Set[Tuple[str,str]]): The input variables of the program.
            * `C` (Set[Tuple[str,str]]): The holes variables of the program.
            * `max_itr_num` (int): The maximum number of iterations to run the CEGIS loop.
            * `timeout` (int): The timeout for each iteration of the CEGIS loop (the timeout for the solver).
            * `debug` (bool): The debug mode.
       
        Raises:
            * Exception: If the length of `verification_conditions` is less than the length of `assumptions`.
        
        Examples:
            * Initialize the Cegis algorithm:
                >>> cegis = Cegis(verification_conditions=[z3.BoolVal(True)], assumptions=[z3.BoolVal(True)], X={'x': 'Int'}, C={'c': 'Bool'})
                >>> cegis
                Cegis(verification_conditions=[BoolVal(True)], assumptions=[BoolVal(True)], X={'x': 'Int'}, C={'c': 'Bool'})
        
        Notes:
            * The length of `verification_conditions` and `assumptions` must be the same.
        """
        self.debug = debug
        
        if len(verification_conditions) < len(assumptions):
            raise Exception(f"The length of `verification_conditions` ({len(verification_conditions)}) must be less or equal to the length of `assumptions` ({len(assumptions)})")
        
        # make the length of `verification_conditions` and `assumptions` the same
        if len(verification_conditions) > len(assumptions):
            if self.debug:
                cprint(f"The length of `verification_conditions` ({len(verification_conditions)}) is more than the length of `assumptions` ({len(assumptions)}), so we add `True` to the end of `assumptions`", color=Colors.RED)
            assumptions.extend([z3.BoolVal(True)] * (len(verification_conditions) - len(assumptions)))

        self.verification_conditions = verification_conditions
        self.assumptions = assumptions
        
        assert len(self.verification_conditions) == len(self.assumptions)
        
        # FIXME: make it look better
        self.X_ty = {x : x_ty for x, x_ty in X} # map each var to its type
        self.C_ty = {c : c_ty for c, c_ty in C}
        
        self.C: List[z3.ExprRef] = [Z3_TYPE[c_type](c) for c, c_type in C]
        self.C_in_bad_values: List[List[z3.BoolRef]] = [] 

        self.X_in_vars: List[z3.ExprRef] = [Z3_TYPE[x_type](f'{x}_in') for x, x_type in X]
        self.X: List[z3.ExprRef] = [Z3_TYPE[x_type](x) for x, x_type in X]
        
        self.X_in_constrains = z3.And([x == x_in for x, x_in in zip(self.X, self.X_in_vars)])
        # counter example values for x, to add each time
        self.X_in_values: List[List[Tuple[z3.ExprRef, z3.ExprRef,]]] = [[]]

        
        # XXX: add support for more z3 types
        def get_random_z3_val(ty: str):
            from random import randint, choice
            if ty in ['int', 'float', 'Array int']:
                return Z3_VAL[ty](randint(-100, 100))
            elif ty in ['bool', 'Array bool']:
                return Z3_VAL[ty](choice([True, False]))
            else:
                raise Exception(f"The type {ty} is not supported")
        
        # initial (random) guess for the C
        self.C_in_new_values_to_try: List[Tuple[z3.ExprRef, z3.ExprRef]] = [(c, get_random_z3_val(self.C_ty[str(c)]))  for c in self.C]

        # The maximum number of iterations to run the CEGIS loop
        self.max_itr_num = max_itr_num
        # The timeout for each iteration of the CEGIS loop (the timeout for the solver)
        self.timeout = timeout #TODO


    def hole_assignments(self) -> List[z3.BoolRef]:
        """
        Generate the formula to check if the program is valid after assigning the new values to the holes.
        """
    
        # programs_formula2 = [z3.ForAll(self.X, z3.Implies( z3.And(self.X_in_constrains, assumption), vc))
        #                     for assumption, vc in zip(self.assumptions, self.verification_conditions)]
        programs_formula = [z3.Implies( z3.And(self.X_in_constrains, assumption), vc)
                            for assumption, vc in zip(self.assumptions, self.verification_conditions)]
        
        formulas = []
        formulas.extend([substitute_z3(prog_formula, self.C_in_new_values_to_try) for prog_formula in programs_formula])
        formulas = [z3.Not(z3.And(*formulas))]
                
        # add the old X_in values so we don't get the same values again, in the counter-example
        for X_in_vals in self.X_in_values:
            if len(X_in_vals) > 0:
                formulas.append(z3.Not( z3.And([x_in == x_in_val for x_in, x_in_val in X_in_vals]) ))
                
        if self.debug:
            print(f"{Colors.BG_BRIGHT_MAGENTA}{Colors.BLACK}>>> hole_assignments formulas:{Colors.RESET}\n")
            print(f"{Colors.BG_BRIGHT_MAGENTA}{Colors.BLACK}{formulas}:{Colors.RESET}\n")
        return formulas
    
    def verify_hole_assignments(self,
                                formulas: List[z3.BoolRef]
                                ) -> z3.ModelRef | None:

        """
        Verify the program after assigning the new values to the holes.
        Returns `None` if the program is valid, and a counter-example otherwise.
        """
        # Solve the formula to get the counter-example values for the X_in vars.
        cprint(f">>>> Try to Verify the program with the C values. If the C values are not valid, then we get new  X values from the counter-example", color=Colors.GREEN)
        cprint(f">>>> The C Values: ",self.C_in_new_values_to_try, color=Colors.BLUE)
        
        model = solve_z3(formulas, name="The program to verify with the C values")
        if self.debug:
            print("verify_res: ", model)
        return model
    
    def get_new_X(self,
                  model: z3.ModelRef
                ) -> None:
        # use the examples, and also look at the "history" of the passed "x's" to generate a new "x"
        cprint("\nThe C values are not valid, so get a new X values from the model counterexample to get a new C values", color=Colors.GREEN)
        
        model_vars = [str(x) for x in model.decls()]      
        # FIXME: Get the correct counterexample for this kind of program
        # XXX `Counterexample:[x = 15, div0 = [else -> 0], mod0 = [else -> 0]]`
            
        # get the counter-example values for the X_in vars.
        # if there is no counter-example for some `x_in` in `X_in_vars`, then choose some random value for it.
        X_in_new_values = []
        for x_in in self.X_in_vars:
            if str(x_in) not in model_vars:
                print(f"{x_in} is not in the model, so choose some random value for it")
                # TODO: change this to random value instead of 0 
                #TODO: make sure that when choosing this value, we don't get X_in_new_values that are the same as the old ones
                # FIXME: to the corect z3.type insted of `z3.IntVal`
                X_in_new_values.append((x_in, z3.IntVal(0))) # FIXME: to the corect z3.type insted of `z3.IntVal`
            else:
                # TODO: check if this should be `model.eval(x_in)` or `model[x_in]`
                X_in_new_values.append((x_in, model.eval(x_in)))
        
        cprint("The new X values are: ", X_in_new_values, color=Colors.BLUE)
        # add the new X_in values to the old ones
        self.X_in_values.append(X_in_new_values)

    def generate_new_constraint(self) -> List[z3.BoolRef] :
        """
        Generate a new constraint, to send to the solver.
        """
        # uses `get_new_X` to generate the new constraint. To send to the solver.
        # Now for each new X_in values, create a new formula to get new C values
        programs_formulas_X = [(z3.Implies(z3.And(assumption), vc))
                               for assumption, vc in zip(self.assumptions, self.verification_conditions)]
        formulas = []
        
        # substitute the new X_in values in the prog_formula
        for i, X_in_vals in enumerate(self.X_in_values):
            if len(X_in_vals) > 0:
                X_val_to_assign = [(Z3_TYPE[self.X_ty[str(x_in)[:-3]]](str(x_in)[:-3]), x_val) for x_in, x_val in X_in_vals]
                formulas.extend([substitute_z3(prog_formula_X, X_val_to_assign) for prog_formula_X in programs_formulas_X])
        
        # TODO: check if this correct 
        if len(formulas) == 0:
            formulas = programs_formulas_X
        # Add the `C_in_bad_values` that we want to avoid
        self.C_in_bad_values.append([c == c_val for c, c_val in self.C_in_new_values_to_try])
        for C_in_bad_vals in self.C_in_bad_values:
            if len(C_in_bad_vals) > 0:
                formulas.append(z3.Not( z3.And(C_in_bad_vals)) )
        return formulas
    
    
    def solve_constraint(self,
                        formulas: List[z3.BoolRef]
                        ) -> bool:
        """
         solve_constraint
        -----------------
        Solve the constraint, to find a new values for the holes.
        
        Returns:
        -------
            * `True`: If new C values are found.
            * `False` (bool): If no new C values are found.
        """
        if self.debug:
            print(f"{Colors.BRIGHT_MAGENTA}>>> solve_constraint formulas{Colors.RESET}\n")
            print(f"{Colors.BRIGHT_MAGENTA}>>> Now, after we got the new X values, we try to get new C values (by using the solver){Colors.RESET}\n")
            
        # Now, use the solver to get new C values
        model = solve_z3(formulas, name="The formula we need to solve to get new C values")
        if model:
            model_vars = [str(c) for c in model.decls()]
            C_in_new_values_to_try = []
            # FIXME: Get the correct counterexample for this kind of program
            # XXX `Counterexample:[x = 15, div0 = [else -> 0], mod0 = [else -> 0]]`
            
            for c in self.C:
                if str(c) not in model_vars:
                    # TODO: change this to random value instead of 0
                    # FIXME: change ` z3.IntVal` to the correct val
                    C_in_new_values_to_try.append((c, z3.IntVal(0))) 
                else:
                    C_in_new_values_to_try.append((c, model.eval(c)))
                    
            print("The new C values are: ", C_in_new_values_to_try)
            self.C_in_new_values_to_try = C_in_new_values_to_try
            return self.FOUND_NEW_C_VALS
        else:
            cprint("No new C values found", color=Colors.YELLOW)
            return self.NO_NEW_C_VALS

    
    def cegis_loop(self) -> Dict[Hole_Id, Hole_Val]:
        """
        cegis_loop
        -----------
        The CEGIS loop. 
        It calls the `hole_assignments` function to get new C values, 
        and then calls the `verify_hole_assignments` function to check if these C values are valid.
        If the C values are valid, then it calls the `get_new_X` function to get new X values, 
        
        """
        for i in range(self.max_itr_num):
            # TODO: add log file
            print(f"{Colors.BRIGHT_MAGENTA}\n>>>> IN THE {i} ITERATION{Colors.RESET}")

            formulas = self.hole_assignments()
            model = self.verify_hole_assignments(formulas)

            # not true for all values of x (the C assignment is not valid). So get a new X values to get a new C values
            if model is not None:
                self.get_new_X(model)
                formulas_X = self.generate_new_constraint()
                
                # To find new C values
                if self.solve_constraint(formulas_X) == self.NO_NEW_C_VALS:
                    cprint(f"Stop after {i} iterations, because we didn't find new C values", color=Colors.RED)
                    cprint("The Last values of the C (holes) are: ", self.C_in_new_values_to_try, color=Colors.YELLOW)
                    cprint("Check if these C values are correct, if not then the program is not valid, or the input Examples are incorrect", color=Colors.RED)
                    return {c: c_val for c, c_val in self.C_in_new_values_to_try}
            else:
                cprint(f"Stop after {i} iterations, because we didn't find new X values", color=Colors.RED)
                cprint("The C values are valid, And the program is valued", color=Colors.YELLOW)
                cprint("The values of the holes are: ", self.C_in_new_values_to_try, color=Colors.YELLOW)
                return {c: c_val for c, c_val in self.C_in_new_values_to_try}
            
        cprint(f"Stop after {self.max_itr_num} iterations, because we reached the maximum number of iterations", color=Colors.RED)
        cprint("No valid values were found for the holes (C) within the maximum number of iterations", color=Colors.RED)
        cprint("Try to increase the maximum number of iterations, or check if the input Examples are correct",
               "or give another specification", color=Colors.RED)
        # return None
        return {c: c_val for c, c_val in self.C_in_new_values_to_try}
        
