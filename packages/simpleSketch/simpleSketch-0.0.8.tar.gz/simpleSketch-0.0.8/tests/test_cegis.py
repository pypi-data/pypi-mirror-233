"""
* file: test_cegis.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description:  Unit tests for the cegis module.
"""

import sys
from pathlib import Path
from synthesis import cegis, pbe

from while_lang import syntax_v1 
sys.path.extend([str(p) for p in [
    Path(__file__).parent.parent,
    Path(__file__).parent,
    ] if p not in sys.path])

from typing import Callable, Dict, List, Set, Any, Tuple
import z3
#TODO: check the import
# from adt.tree import Tree
from lib.adt.tree import Tree
#TODO: check the import form `src`
# import verifier
from src.verifier import verifier, wp
from z3_handler.z3_handler import solve_z3, substitute_z3, get_all_z3_vars, print_z3


from utilities.Utilities import Colors, cprint


# Define a type for hole identifiers and values
# Hole_Id = str
Hole_Id = z3.ArithRef
Hole_Val = int

# Define a type for the program environment, the environment is a mapping from variable names to z3 values.
Env_Key = str 
Env_Val = z3.ArithRef
Env = Dict[Env_Key, Env_Val]
Linv_t = Callable[[Dict[Env_Key, Env_Val]], z3.BoolRef]



Spec_t = Tuple[z3.BoolRef, z3.BoolRef]
Program_t = str


class TestCegis:
    """
     
    """
    def __init__(self):
        import os

        # if the terminal size cannot be obtained (e.g. when running in a notebook) return a default value and ignore the exception
        try:
            self.terminal_size = os.get_terminal_size().columns
        except:
            self.terminal_size = 80
        self.tests = []
        self.run_allTests = True  # If True, checks all tests, even if they are set to False
        
        self.stop_at_first_fail = False  # If True, stops at the first failed test


    def test_cegis(
        self,
        program: str,
        input_examples: List[Callable[[Env], z3.BoolRef | z3.Probe]], 
        output_examples: List[Callable[[Env], z3.BoolRef | z3.Probe]],
        expected_verify_res: bool = True,
        ignore_test=False,
    ) -> None:
        """
        T
        Args:
            * program (str): The  program.
            * input_examples (List[Callable[[Env], z3.BoolRef]]): list of input examples of the program, each input example (element in the `input_examples`) is a list of Z3 formulas.
            * output_examples (List[Callable[[Env], z3.BoolRef]]): list of output examples of the program, each output example (element in the `output_examples`) is a list of Z3 formulas.
            * `expected_verify_res` (bool): The expected result of the `verify` function
            * `ignore_test` (bool, optional): Whether to ignore the test or not, If `True`, the test will be ignored. Defaults to `False`.

        Returns:
            None
            
        Example:
            >>> tester = TestVerify()
            >>> tester.test_cegis(
                            program = "y := (??* x) + ??",
                            input_examples = [
                                lambda env: z3.And(env['x'] == 1),
                                lambda env: z3.And(env['x'] == 2)
                            ],
                            output_examples = [
                                lambda env: z3.And(env['y'] == 3),
                                lambda env: z3.And(env['y'] == 5)
                            ],
                            expected_verify_res = True,
                            ignore_test = True
                        )
        """

        if ignore_test:
            return  # Didn't check the test

        cprint(f">> Running Test...:", color=Colors.BRIGHT_MAGENTA)
        cprint(f"program: {program}", color=Colors.CYAN)
        test_res = cegis.create_synthesis_problem(program, input_examples=input_examples, output_examples=output_examples)
        
        cprint(f"\n-----Test Results-----", color=Colors.BRIGHT_MAGENTA)
        # cprint(f"\n>>> verification_cond :\n{test_res['verification_cond']}", color=Colors.CYAN)
        cprint(f"\n>>> verification_cond:", color=Colors.CYAN)
        print_z3(test_res['verification_cond'])
        # cprint(f"\n>>> prog_wp:\n{test_res['prog_wp']}", color=Colors.CYAN)
        cprint(f"\n>>> assumptions:\n{test_res['assumptions']}", color=Colors.CYAN)
        cprint(f"\n>>> X_in: {test_res['X_in']}", color=Colors.CYAN)
        cprint(f"\n>>> C_vals: {test_res['C_vals']}", color=Colors.BRIGHT_RED)






if __name__ == "__main__":
    import z3
    
    print(Colors.RED, "Running tests for the cegis module", Colors.RESET)

    tester = TestCegis()
    # If True, checks all tests, even if they are set to False
    tester.run_allTests = True
    # tester.stop_at_first_fail = True  # If True, stops at the first failed test
    
    tester.test_cegis(
        program = r"""
        y := (??* x) + ??;
        (if ((y - ??) > k ) then
            (k := 1)
        else
            (k := 2))
        """,
        input_examples = [
            lambda env: z3.And(env['x'] == 1, env['k'] == 3),
            lambda env: z3.And(env['x'] == 2, env['k'] == 3)
        ],
        output_examples = [
            lambda env: z3.And(env['y'] == 3, env['k'] == 1),
            lambda env: z3.And(env['y'] == 5, env['k'] == 1)
        ],
        ignore_test=True
    )

    tester.test_cegis(
        program = r"""
            y := (??* x) + ??;
            assert ((x + 1) = (y - x));
            assert ((y) = ((2*x) + 1));
            assume (x = 1);
            assert (y = 3);
            assume (k = 3);
            (if ((y - ??) > k ) then
                (k := 1)
            else
                (k := 2));
            assert (k = 1)
        """,
        input_examples = [],
        output_examples = [],
        ignore_test=False
        # ignore_test=True
    )
