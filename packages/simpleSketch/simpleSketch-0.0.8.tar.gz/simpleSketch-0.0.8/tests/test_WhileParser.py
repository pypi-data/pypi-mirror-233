

import sys
from pathlib import Path

sys.path.extend(str(p) for p in [
    Path(__file__).parent.parent.parent.parent# root 
    ] if p not in sys.path)


from lib.adt.tree import Tree
from src.while_lang.syntax.syntax import WhileParser , pretty


from utilities import Utilities 
from utilities.Utilities import Colors
# TODO: ADD LOG FILE
DEBUG = True
DEBUG_WhileParser_postprocess = False
DEBUG_WhileParser_Grammar = False



def WhileParser_TestCases() -> list[dict[str, str | bool]]:
    """
    # FIXME: need to fix `program_ast` to match the new grammar ast
    """
    # TODO: Add more test cases
    test_cases = [
        {   #0
            'program': "c := a ; b := 1 ;", 
            'program_ast': r";{:={id{c}, id{a}}, :={id{b}, num{1}}}",
            'is_valid': True
        }
        
        ,{  # 1
            'program': "a := 3 ; b := a ; c := b - 1 ; a := 5", 
            'program_ast': r";{:={id{a}, num{3}}, ;{:={id{b}, id{a}}, ;{:={id{c}, -{id{b}, num{1}}}, :={id{a}, num{5}}}}}",
            'is_valid': True
        } 
        
        ,{  # 2
            'program': "abc := -2", 
            'program_ast' :":={id{abc}, num{-2}}",
            'is_valid': True
        }
        ,{  # 3
            'program': "x:=1 ; if ( x < y ) then ( a := 3 ; b:= a * 2 ) else b := 2", 
            'program_ast' :r";{:={id{x}, num{1}}, if{<{id{x}, id{y}}, ;{:={id{a}, num{3}}, :={id{b}, *{id{a}, num{2}}}}, :={id{b}, num{2}}}}",
            'is_valid': True
        },
        {   # 4
            'program': "if ( x < y )  then a := 3  else b := 2", 
            'program_ast' :r"if{<{id{x}, id{y}}, :={id{a}, num{3}}, :={id{b}, num{2}}}",
            'is_valid': True
        }
        ,{  # 5
            'program': "x := 1 + 2 * 3 - 2 / 2; assert x = 6", 
            'program_ast' :r";{:={id{x}, -{+{num{1}, *{num{2}, num{3}}}, /{num{2}, num{2}}}}, assert{={id{x}, num{6}}}}",
            'is_valid': True
        }
        ,{  # 6
            'program': r"""
                    if (b) then (
                        C := c1 ;
                        if (b) then (
                            C := c1 ;
                            if (b) then (
                                assert (1 = 0)
                            ) else (
                                skip
                            )
                        ) else (
                            skip
                        )
                    ) else (
                        skip
                    );
                    x := 2
                    """, 
            'program_ast' :r";{if{id{b}, ;{:={id{C}, id{c1}}, if{id{b}, ;{:={id{C}, id{c1}}, if{id{b}, assert{={num{1}, num{0}}}, skip{skip}}}, skip{skip}}}, skip{skip}}, :={id{x}, num{2}}}",
            'is_valid': True
        }
        ,{  # 7
            'program':r"""
                assume ( x > 0);
                while (x < 2) do ( 
                        if (x = 2) then(
                            x := x - 1
                        ) else (
                            y := y + 1
                        );
                        k := k + 1
                    ); 
                z := z + 1
                """, 
            'program_ast' :r";{assume{>{id{x}, num{0}}}, ;{while{<{id{x}, num{2}}, ;{if{={id{x}, num{2}}, :={id{x}, -{id{x}, num{1}}}, :={id{y}, +{id{y}, num{1}}}}, :={id{k}, +{id{k}, num{1}}}}}, :={id{z}, +{id{z}, num{1}}}}}",
            'is_valid': True
        }
        ,{  # 8
            'program':r"""
                ?? := 0; while (i < ??) do ( i := i + ?? ; j := i + ??)
                """, 
            'program_ast' : "",
            'is_valid': False
        }
        ,{  # 9
            'program':r"""
                i := 0; while (i < ??) do ( i := i + ?? ; j := i + ?? ;)
                """, 
            'program_ast' : r";{:={id{i}, num{0}}, while{<{id{i}, hole{c0}}, ;{:={id{i}, +{id{i}, hole{c1}}}, :={id{j}, +{id{i}, hole{c2}}}}}}",
            'is_valid': True
        }
        ,{  # 10
            'program':r"""
                a := 4;
                b := 2;
                while (a != b) do 
                (
                    assert ( a > 0 );
                    assert ( b > 0 );
                    if ( a > b ) then (
                        a := (?? * a) + (?? * b)
                    )
                    else (
                        b := (?? * a) + (?? * b)
                    )
                );
                assert ( a > 0 );
                assert ( a = b );
                assert ( a = 2 )
            """, 
            'program_ast' : r";{:={id{a}, num{4}}, ;{:={id{b}, num{2}}, ;{while{!={id{a}, id{b}}, ;{assert{>{id{a}, num{0}}}, ;{assert{>{id{b}, num{0}}}, if{>{id{a}, id{b}}, :={id{a}, +{*{hole{c0}, id{a}}, *{hole{c1}, id{b}}}}, :={id{b}, +{*{hole{c2}, id{a}}, *{hole{c3}, id{b}}}}}}}}, ;{assert{>{id{a}, num{0}}}, ;{assert{={id{a}, id{b}}}, assert{={id{a}, num{2}}}}}}}}",
            'is_valid': True
        }
       
        # Add more test cases
    ]
    return test_cases
    

class WhileParserTester:
    """
    Test class for WhileParser
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
    
    
    def TestWhileParser(self, program: str, expected_ast: str = "", is_valid: bool = True, test_num: int = 1, print_dot:bool = False) -> bool:
        print('\n',"-" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Running Test ({test_num})...", Colors.RESET)
        print("-" * (self.terminal_size // 2))
        
        test_res, test_msg = False, ""
        program_ast = WhileParser()(program)
        
        if not program_ast:
            print(Colors.BRIGHT_CYAN,">> Invalid program:\n", program, Colors.RESET)
            if is_valid != False:
                test_res = self.TEST_FAILED
                test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected valid program, But got invalid program {Colors.RESET}"
            else:
                test_res = self.TEST_PASSED
        else:
            # print(Colors.BRIGHT_CYAN,">> Valid program:\n", program, Colors.RESET)
            print(f"{Colors.BRIGHT_CYAN}>> Valid program:\n{Colors.RESET}", program)
            if print_dot: Utilities.dot_print(program_ast, tmp_graph=False, graph_name=f"program{test_num}")
            if is_valid != True:
                test_res = self.TEST_FAILED
                test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected invalid program, But got valid program {Colors.RESET}"
            elif expected_ast != str(program_ast):
                    test_res = self.TEST_FAILED
                    test_msg = f"{Colors.BRIGHT_MAGENTA}>> Expected AST:\n{expected_ast}\n\n>> But got AST:\n{program_ast}{Colors.RESET}"
            else:
                test_res = self.TEST_PASSED
                print(f"{Colors.BRIGHT_CYAN}>> program AST:\n{Colors.RESET}", program_ast)
                print(f"\n{Colors.BRIGHT_CYAN}>> pretty program:\n{Colors.RESET}", pretty(program_ast))
        
        print("+" * (self.terminal_size // 2))
        print(Colors.YELLOW, f">> Test {test_num} Result ...", Colors.RESET)
        if test_res == self.TEST_PASSED:
            print(Colors.GREEN,">> TEST PASSED", Colors.RESET)
        else:
            print(Colors.RED,">> TEST FAILED", Colors.RESET) ; print(test_msg)
        print("+" * (self.terminal_size // 2))
        return test_res
    
    
    def TestWhileParserCases(self, test_cases: list[dict[str, str | bool]], print_dot:bool = False):
        failed_tests, passed_tests = [], []
        for test_num, test_case in enumerate(test_cases):
            program = test_case.get('program', '')
            program_ast = test_case.get('program_ast', '')
            is_valid = test_case.get('is_valid', True)
            test_res = self.TestWhileParser(program=program, expected_ast=program_ast, is_valid=is_valid, test_num=test_num, print_dot=print_dot)
            if test_res == self.TEST_FAILED: failed_tests.append(test_num)
            if test_res == self.TEST_PASSED: passed_tests.append(test_num)
            
        
        print(f"{Colors.RED}>> Failed {len(failed_tests)}/{len(test_cases)} tests: {failed_tests} {Colors.RESET}")
        print(f"{Colors.GREEN}>> Passed {len(passed_tests)}/{len(test_cases)} tests{Colors.RESET}")
                
            


if __name__ == "__main__":
    test_cases = WhileParser_TestCases()
    WhileParserTester().TestWhileParserCases(test_cases, print_dot=True)
    
    # WhileParserTester().TestWhileParserCases( test_cases=[test_cases[5]], print_dot=True)
    
    
    
    
