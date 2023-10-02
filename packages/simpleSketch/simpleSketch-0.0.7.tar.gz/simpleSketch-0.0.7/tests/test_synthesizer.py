

import sys
from pathlib import Path
sys.path.extend(str(p) for p in [
    Path(__file__).parent.parent.parent# root 
    ] if p not in sys.path)


from lib.adt.tree import Tree

from src.while_lang.while_language import WhileLang, Env, Env_Key, Env_Val, Hole_Id, Hole_Val, Program_t
from typing import Callable, Dict, List, Set, Any, Tuple, TypeAlias, NewType

from src.synthesis.synthesizer import  Synthesizer 
from src.synthesis.specification import Specification, Spec_Example

from z3 import *
from utilities import Utilities 
from utilities.Utilities import Colors
# TODO: ADD LOG FILE
DEBUG = True
DEBUG_WhileParser_postprocess = False
DEBUG_WhileParser_Grammar = False



def Synthesizer_TestCases() -> list[dict[str, str | bool | list | set  | Dict]]:
    # TODO: Add more test cases

    test_cases = [
        {   # 0
            'program':r"""
                a := ?? ; b := ??; c := ??; d := ??;
                y := a*(x*x*x) + b*(x*x) + c*(x) + d;
            """,
            'specification' : None,
            'input_output_examples' : [
                Spec_Example(input_example = lambda d: d['x'] == 2, output_example = lambda d: d['y'] == 6), 
                Spec_Example(input_example = lambda d: d['x'] == 1, output_example = lambda d: d['y'] == -30), 
                Spec_Example(input_example = lambda d: d['x'] == -4, output_example = lambda d: d['y'] == 60), 
                Spec_Example(input_example = lambda d: d['x'] == -9, output_example = lambda d: d['y'] == 50) 
            ],
            'expected_holes_values':{Int('c2'): IntVal(-1), Int('c0'): IntVal(1), Int('c1'): IntVal(10), Int('c3'): IntVal(-40)},
            'is_valid': True
        },
        {   # 1 
            'program':r"""
                a := ?? ; b := ??; c := ??; d := ??;
                y := a*(x*x*x) + b*(x*x) + c*(x) + d;
            """,
            'specification' : None,
            'input_output_examples' : [
                Spec_Example(input_example = lambda d: d['x'] == 2, output_example = lambda d: d['y'] == 6), 
                Spec_Example(input_example = lambda d: d['x'] == 1, output_example = lambda d: d['y'] == -30), 
                Spec_Example(input_example = lambda d: d['x'] == -4, output_example = lambda d: d['y'] == 60), 
                Spec_Example(input_example = lambda d: d['x'] == -9, output_example = lambda d: d['y'] == 50) 
            ],
            'expected_holes_values':{Int('c2'): IntVal(-1), Int('c0'): IntVal(1), Int('c1'): IntVal(10), Int('c3'): IntVal(-40)},
            'is_valid': True
        },

        {   # 2 (Euclid's algorithm) 
            # P=lambda d: And(d['a'] > 0, d['b'] > 0),
            # program="while a != b do if a > b then a := a - b else b := b - a",
            # Q=lambda d: And(d['a'] > 0, d['a'] == d['b']),
            # linv=lambda d: And(d['a'] > 0, d['b'] > 0),  # figure it out!
            'program':r"""
                a := 4;
                b := 2;
                while (a != b) 
                {
                    assert ( a > 0 );
                    assert ( b > 0 );
                    if ( a > b ) {
                        a := (?? * a) + (?? * b);
                    }
                    else {
                        b := (?? * a) + (?? * b);
                    }
                }
                assert ( a > 0 );
                assert ( a == b );
                assert ( a == 2 );
            """,
            'specification' : None,
            'input_output_examples' : [
                # Spec_Example(input_example = lambda d: And(d['a'] == 4, d['b'] == 2), output_example = lambda d: And(d['a'] == 2)) 
                # Spec_Example(input_example = lambda d: d['x'] == 1, output_example = lambda d: d['y'] == 1),  
            ],
            'expected_holes_values':{Int('c0'): IntVal(1), Int('c1'): IntVal(-1), Int('c2'): IntVal(-1), Int('c3'): IntVal(1)},
            'is_valid': True
        },
        {   # 3  
            # P=lambda d: And(d['n'] > 0),
            # program="while (i < n) do i := i + 2",
            # Q=lambda d: And(d['i'] <= n + 1),
            # linv=lambda d: And(d['n'] - d['i'] >= -1)
            'program':r"""
                assume (n > 0);
                i := 0;
                while (i < n) { i := i + 2; }
                assert (n - i >= -1);
            """,
            'specification' : None,
            'input_output_examples' : [
                # Spec_Example(input_example = lambda d: And(d['a'] == 4, d['b'] == 2), output_example = lambda d: And(d['a'] == 2)) 
                # Spec_Example(input_example = lambda d: d['x'] == 1, output_example = lambda d: d['y'] == 1),  
            ],
            'expected_holes_values':{Int('c0'): IntVal(2)},
            'is_valid': True
        },
        {   # 4 (Euclid's algorithm) 
            # P=lambda d: And(d['a'] > 0, d['b'] > 0),
            # program="while a != b do if a > b then a := a - b else b := b - a",
            # Q=lambda d: And(d['a'] > 0, d['a'] == d['b']),
            # linv=lambda d: And(d['a'] > 0, d['b'] > 0),  # figure it out!
            'program':r"""
                assume ( a > 0 );
                assume ( b > 0 );
                while (a != b) {
                    assert ( a > 0 );
                    assert ( b > 0 );
                    if ( a > b ) {
                        a := (?? * a) + (?? * b);
                    }
                    else {
                        b := (?? * a) + (?? * b);
                    }
                }
                assert ( a > 0 );
                assert ( a == b );
            """,
            'specification' : None,
            'input_output_examples' : [
                # Spec_Example(input_example = lambda d: And(d['a'] == 4, d['b'] == 2), output_example = lambda d: And(d['a'] == 2)) 
                # Spec_Example(input_example = lambda d: d['x'] == 1, output_example = lambda d: d['y'] == 1),  
            ],
            'expected_holes_values':{Int('c0'): IntVal(1), Int('c1'): IntVal(-1), Int('c2'): IntVal(-1), Int('c3'): IntVal(1)},
            'is_valid': True
        },
        {   # 5
            'program':r"""
                i := ??;
                y := i*i  + x*??;
                assert (y == x + x + 9);
            """,
            'specification' : None,
            'input_output_examples' : [
            ],
            'expected_holes_values':{Int('c0'): IntVal(3), Int('c1'): IntVal(2)},
            'is_valid': True
        }
        
        # Add more test cases
    ]
    return test_cases
    

class SynthesizerTester:
    """
    Test class for `Synthesizer` class
    """
    TEST_PASSED = True
    TEST_FAILED = False
    
    def __init__(self):
        from os import get_terminal_size
        # if the terminal size cannot be obtained (e.g. when running in a notebook) return a default value and ignore the exception
        try:
            self.terminal_size = get_terminal_size().columns
        except:
            self.terminal_size = 80
    
    
    def TestSynthesizer(self, program: str, expected_holes_values: Dict[Hole_Id, Hole_Val] | None,
                        specification: Specification, input_output_examples: List[Spec_Example],
                        is_valid: bool = True, test_num: int = 1, print_dot:bool = False) -> bool:
        print('\n',"-" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Running Test ({test_num})...", Colors.RESET)
        print("-" * (self.terminal_size // 2))
        test_res, test_msg = False, ""
        
        synthesis_obj = Synthesizer(program=program)
        res = synthesis_obj.synthesize(specification, input_output_examples)
        if res:
            filled_program ,holes_vals = res
            print(f"{Colors.BRIGHT_CYAN}>> program:{Colors.RESET}\n", program)
            # sort the holes values by their keys (hole ids) to make the comparison easier
            if holes_vals is not None : holes_vals = dict(sorted(holes_vals.items(), key=lambda item: str(item[0]))) 
            if expected_holes_values is not None : expected_holes_values = dict(sorted(expected_holes_values.items(), key=lambda item: str(item[0]))) 
            
            if not holes_vals and not expected_holes_values:
                test_res = self.TEST_PASSED
            elif holes_vals and holes_vals != expected_holes_values:
                test_res = self.TEST_FAILED
                test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected holes values: {expected_holes_values}\n\n>> But got holes values: {holes_vals}{Colors.RESET}"
            else:
                test_res = self.TEST_PASSED
        else:
            raise NotImplementedError("TODO: Handle this case")
        
        print("+" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Test {test_num} Result ...", Colors.RESET)
        if test_res == self.TEST_PASSED:
            print(Colors.GREEN,">> TEST PASSED", Colors.RESET)
            print(f"{Colors.BRIGHT_CYAN}>> filled_program:{Colors.RESET}\n{filled_program}\n")
            print(f"{Colors.BRIGHT_CYAN}>> holes values: {holes_vals}{Colors.RESET}")
        else:
            print(Colors.RED,">> TEST FAILED", Colors.RESET) ; print(test_msg)
        print("+" * (self.terminal_size // 2))
        return test_res
    
    
    def TestSynthesizerCases(self, test_cases: List[Dict[str, Any]], print_dot:bool = False):
        failed_tests, passed_tests = [], []
        for test_num, test_case in enumerate(test_cases):
            program = test_case.get('program', '')
            specification = test_case.get('specification', {})
            input_output_examples = test_case.get('input_output_examples', [])
            expected_holes_values = test_case.get('expected_holes_values', None)
            is_valid = test_case.get('is_valid', True)
            test_res = self.TestSynthesizer(program=program, 
                                            expected_holes_values=expected_holes_values, 
                                            input_output_examples = input_output_examples, 
                                            specification=  specification,
                                            is_valid=is_valid, test_num=test_num, print_dot=print_dot)
            if test_res == self.TEST_FAILED: failed_tests.append(test_num)
            if test_res == self.TEST_PASSED: passed_tests.append(test_num)
            
        
        print(f"{Colors.RED}>> Failed {len(failed_tests)}/{len(test_cases)} tests: {failed_tests} {Colors.RESET}")
        print(f"{Colors.GREEN}>> Passed {len(passed_tests)}/{len(test_cases)} tests{Colors.RESET}")
                
            


if __name__ == "__main__":
    test_cases = Synthesizer_TestCases()
    # TODO: x**2
    # program = r"""
    # y := a*(x**3) + b*(x**2) + c*(x) + d;
    # """
    
    # SynthesizerTester().TestSynthesizerCases(test_cases, print_dot=False)
    
    # SynthesizerTester().TestSynthesizerCases( test_cases=[test_cases[4]], print_dot=False)
    # SynthesizerTester().TestSynthesizerCases( test_cases=[test_cases[5]], print_dot=False)
    
    
