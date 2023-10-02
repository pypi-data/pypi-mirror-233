"""
* file: test_z3_text_parser.py
* author: <NAME> <<EMAIL>>
* date: September 2023
* description: test file for the z3 text parser. This module contains the tests for the Z3Parser class.
"""


import sys
from pathlib import Path

# Add  the following paths to sys.path:
sys.path.extend([
    str(p)
    for p in [
        Path(__file__).parent.parent.parent.parent, # root of the project
    ]
    if p not in sys.path]
)



from typing import Callable, Dict, List, Optional, Set, Tuple, Union, Any, TypeAlias, NewType

from lib.adt.tree import Tree
from .z3_text_parser import Z3Parser

import z3

# For the debugging and the log file
from utilities import Colors, cprint

# TODO: Add log file
# TODO: Change to False, before submitting
DEBUG = True
DEBUG = False
DEBUG_Z3_postprocess = True
DEBUG_Z3_postprocess = False


def Z3Parser_TestCases():
    # TODO: add more test cases
    test_cases = [
        {   # 0
            'expr': "x + 2", 
            'types': "{ }", 
            'expected_z3_expr': z3.Int('x') + z3.IntVal(2),
            'is_valid': True
        }
        
        ,{  # 1
            'expr': "And(x + 1 == 2, y < 2 , b)",
            'types': "{ }",
            'expected_z3_expr' : "z3.And( z3.Int('x') + z3.IntVal(1) == z3.IntVal(2), z3.Int('y') < z3.IntVal(2), z3.Int('b') )",
            'is_valid': False
        }
        ,{  # 2
            'expr': "And(x + 1 == 2, y < 2 , b)", 
            'types': "{b : bool}", 
            'expected_z3_expr' :z3.And( z3.Int('x') + z3.IntVal(1) == z3.IntVal(2), z3.Int('y') < z3.IntVal(2), z3.Bool('b') ),
            'is_valid': True
        }
        ,{  # 3
            'expr': "ForAll(x , (x < y) )", 
            'types': "{ }", 
            'expected_z3_expr' :z3.ForAll(z3.Int('x'), z3.Int('x') < z3.Int('y')),
            'is_valid': True
        }
        ,{  # 4
            'expr': "ForAll( [ x , y] , (x < y) )", 
            'types': "{ }", 
            'expected_z3_expr' :z3.ForAll([ z3.Int('x'), z3.Int('y') ], z3.Int('x') < z3.Int('y')),
            'is_valid': True
        }
        ,{
            'expr': "ForAll( [ x ] , (x < y) )", 
            'types': "{ }", 
            'expected_z3_expr' :z3.ForAll([ z3.Int('x') ], z3.Int('x') < z3.Int('y')),
            'is_valid': True
        }
        ,{
            'expr': "Or ( 2 + 1 < x , And ( x == 2 , y < 2 ) )", 
            'types': "{ }", 
            'expected_z3_expr' :z3.Or( z3.IntVal(2) + z3.IntVal(1) < z3.Int('x'), z3.And( z3.Int('x') == z3.IntVal(2), z3.Int('y') < z3.IntVal(2) ) ),
            'is_valid': True
        }
        # Add more test cases
    ]
    return test_cases



class Z3ParserTester:
    """
    Test class for Z3Parser
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
    
    
    def TestZ3Parser(self, expr: str, types: str = "", expected_z3_expr: str = "", is_valid: bool = True, test_num: int = 1, print_dot:bool = False) -> bool:
        print('\n',"-" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Running Test ({test_num})...", Colors.RESET)
        print("-" * (self.terminal_size // 2))
        
        test_res, test_msg = False, ""

        result = Z3Parser()(expr, types)
        if not result:
            print(Colors.BRIGHT_CYAN,">> Invalid expression:\n", expr, Colors.RESET)
            if is_valid != False:
                test_res = self.TEST_FAILED
                test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected valid expression, But got invalid expression {Colors.RESET}"
            else:
                test_res = self.TEST_PASSED
        else:
            result = result[2]
            print(f"{Colors.BRIGHT_CYAN}>> Valid expression:\n{Colors.RESET}", expr)
            # if print_dot: Utilities.dot_print(program_ast, tmp_graph=False, graph_name=f"program{test_num}")
            if is_valid != True:
                test_res = self.TEST_FAILED
                test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected invalid expression, But got valid expression {Colors.RESET}"
            elif not z3.eq(expected_z3_expr, result):
                    test_res = self.TEST_FAILED
                    test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected Z3 expression:\n{expected_z3_expr}\n\n>> But got this Z3 expression:\n{result}{Colors.RESET}"
            else:
                test_res = self.TEST_PASSED
                print(f"{Colors.BRIGHT_CYAN}>> Z3 expression:\n{Colors.RESET}", result)
        
        print("+" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Test {test_num} Result ...", Colors.RESET)
        if test_res == self.TEST_PASSED:
            print(Colors.GREEN,">> TEST PASSED", Colors.RESET)
        else:
            print(Colors.RED,">> TEST FAILED", Colors.RESET) ; print(test_msg)
        print("+" * (self.terminal_size // 2))
        return test_res
    
    
    def TestZ3ParserCases(self, test_cases: list[dict[str, str | bool]], print_dot:bool = False):
        failed_tests, passed_tests = [], []
        for test_num, test_case in enumerate(test_cases):
            expr = test_case.get('expr', '')
            types = test_case.get('types', '')
            expected_z3_expr = test_case.get('expected_z3_expr', '')
            is_valid = test_case.get('is_valid', True)
            test_res = self.TestZ3Parser(expr=expr, types=types, expected_z3_expr=expected_z3_expr, is_valid=is_valid, test_num=test_num, print_dot=print_dot)
            if test_res == self.TEST_FAILED: failed_tests.append(test_num)
            if test_res == self.TEST_PASSED: passed_tests.append(test_num)
            
        
        print(f"{Colors.RED}>> Failed {len(failed_tests)}/{len(test_cases)} tests: {failed_tests} {Colors.RESET}")
        print(f"{Colors.GREEN}>> Passed {len(passed_tests)}/{len(test_cases)} tests{Colors.RESET}")
                
            


if __name__ == "__main__":
    test_cases = Z3Parser_TestCases()
    # Z3ParserTester().TestZ3ParserCases(test_cases, print_dot=False)
    
    Z3ParserTester().TestZ3ParserCases( test_cases=[test_cases[4]], print_dot=False)
    
    
    # expr = Z3Parser()("Or ( 2 + 1 < x , And ( x = 2 , y < 2 ) )")
    # expr = Z3Parser()("Or ( 2 + 1 < x , And ( x = 2 , y < 2 ) )")
    # expr = Z3Parser()("Or ( x <  2) ")
    # expr = Z3Parser()("Or ( x <  2) ")
    # expr = Z3Parser()("x = 2")
    # expr = Z3Parser()("x + 2")
    # print(Z3Parser()("ForAll(x , (x < y) )"))
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


    