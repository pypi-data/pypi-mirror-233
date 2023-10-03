import sys
from pathlib import Path

# Add  the following paths to sys.path:
sys.path.extend([
    str(p)
    for p in [
        Path(__file__).parent.parent.parent # /simple_sketch
    ]
    if p not in sys.path]
)

from typing import Callable, Dict, List, Optional, Set, Tuple, Union, Any
import z3
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat, ArithRef, BoolRef
import operator
from simple_sketch.lib.adt.tree import Tree

from simple_sketch.z3_handler.z3_text_parser.z3_text_parser import Z3Parser

# from while_lang.syntax_v1 import WhileParser, pretty
from simple_sketch.while_lang.syntax.syntax import WhileParser, pretty

from simple_sketch.verifier.wp import *
# For the debugging and the log file
from simple_sketch.utilities.Utilities import Colors, cprint



# TODO: Add log file
# TODO: Change to False, before submitting
DEBUG = True
# DEBUG = Flase



class TestVerify:
    G = "\033[92m"  # BRIGHT_GREEN
    B = "\033[94m"  # BRIGHT_BLUE
    C = "\033[96m"  # BRIGHT_CYAN
    R = "\033[91m"  # BRIGHT_RED
    M = "\033[95m"  # BRIGHT_MAGENTA
    Y = "\033[93m"  # BRIGHT_YELLOW
    RST = "\033[0m"  # RESET

    def __init__(self):
        import os

        # if the terminal size cannot be obtained (e.g. when running in a notebook) return a default value and ignore the exception
        try:
            self.terminal_size = os.get_terminal_size().columns
        except:
            self.terminal_size = 80
        self.tests = []
        self.run_allTests = (
            True  # If True, checks all tests, even if they are set to False
        )
        self.stop_at_first_fail = False  # If True, stops at the first failed test

    def add_test(
        self,
        P: Callable,
        program: str,
        Q: Callable,
        linv: Callable | None = None,
        expected_verify_res: bool = True,
        ignore_test=True,
    ):
        """
        * `P` (Callable) : The precondition.
        * `program` (str): The program to verify.
        * `Q` (Callable): The postcondition.
        * `linv` (Callable): The loop invariant. If not included, defaults to `None`.
        * `expected_verify_res` (bool): The expected result of the test (the return value of the `verify` function). defaults to `True`.
        * `ignore_test` (bool): Whether to check the test or not. If not included, defaults to `False`.
        """
        self.tests.append(
            {
                "P": P,
                "program": program,
                "Q": Q,
                "linv": linv,
                "expected_verify_res": expected_verify_res,
                "ignore_test": ignore_test,
            }
        )

    def test_verify(
        self,
        P: Callable,
        program: str,
        Q: Callable,
        linv: Callable | None,
        expected_verify_res: bool,
        ignore_test=True,
    ):
        """
        Test the `verify` function.
        By calling the `verify` function with the given `P`, ast of the `program`, `Q`, and `linv`,
        and comparing the returned value with the `expected_verify_res`.

        Args:
            * `P` (Callable): The precondition
            * `program` (str): The program to be verified
            * `Q` (Callable): The postcondition
            * `linv` (Callable): The loop invariant of the while loop in the program
            * `expected_verify_res` (bool): The expected result of the `verify` function
            * `ignore_test` (bool, optional): Whether to ignore the test or not, If `True`, the test will be ignored. Defaults to `False`.

        Returns:
            int: 0 if the test failed, 1 if the test passed, 2 if the test was ignored

        Example:
            >>> tester = TestVerify()
            >>> tester.test_verify(P = lambda d:  And(d['a'] > 0, d['b'] > 0),
                            program = 'while a != b do if a > b then a := a - b else b := b - a',
                            Q = lambda d: And(d['a'] > 0, d['a'] == d['b']),
                            linv = And(d['a'] > 0, d['b'] > 0),
                            expected_verify_res = True,
                            ignore_test = True)
        """
        
        if ignore_test:
            return 2  # Didn't check the test

        print(self.M + ">> Running Test...", self.RST)
        ast = WhileParser()(program)
        prog = WhileLang(program)
        if ast:
            # env = mk_env(get_pvars(ast))
            env = prog.make_env()
            print("-" * (self.terminal_size // 2))
            print(f"{self.C}>>> env:{self.B} {env} {self.RST}")
            print(f"{self.C}>>> P:{self.B} {P(env)} {self.RST}")
            print(f"{self.C}>>> program:{self.B} {program} {self.RST}")
            print(f"{self.C}>>> Q:{self.B} {Q(env)} {self.RST}")
            if linv != None:
                print(f"{self.C}>>> linv:{self.B} {linv(env)} {self.RST}")
            print("-" * (self.terminal_size // 2))
            try:
                print(self.C + ">> verifying..." + self.RST)
                verify_res = verify(P, ast, Q, linv)
                if expected_verify_res == verify_res:
                    print(self.G + "\n>> Test Passed" + self.RST)
                    test_res = 1  # Test passed
                else:
                    print(
                        self.R
                        + f"\n>> Test Failed: expected {expected_verify_res}, got {verify_res}"
                        + self.RST
                    )
                    test_res = 0  # Test failed
            except Exception as e:
                print(self.R + ">> Test Failed, with the *Exception*:\n", e, self.RST)
                test_res = 0  # Test failed
            # dot_print(ast, tmp_graph=False, graph_name='ast')
        else:
            print(self.R + ">> Invalid program:\n" + program + self.RST)
            test_res = 0  # Test failed
        print(self.M + ">> End of test.\n" + self.RST)
        return test_res

    def test_all(self, tests: List[Dict]):
        """
        Arg:
            * `tests` (List[Dict]): Each `test` in the tests list is a `dict` with the following keys:
                * `P` (Callable) : The precondition.
                * `program` (str): The program to verify.
                * `Q` (Callable): The postcondition.
                * `linv` (Callable): The loop invariant. If not included, defaults to `None`.
                * `expected_verify_res` (bool): The expected result of the test (the return value of the `verify` function).
                * `ignore_test` (bool): Whether to check the test or not. If not included, defaults to `True`.

        Example:
            >>> tester = TestVerify()
            >>> tester.test_all([
                            {
                                'P': lambda _ : True,
                                'program': "a := 3; a:= b + 1",
                                'Q': lambda d: d['b'] == d['a'] - 1,
                                'linv': None,
                                'expected_verify_res': True,
                                'ignore_test' : False
                            },
                            {
                                'P': lambda _ : True,
                                'program': "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )",
                                'Q': lambda d: d['a'] == d['b'],
                                'linv': lambda d: d['a'] == d['b'],
                                'expected_verify_res': True,
                                'ignore_test' : False
                            }
                        ])

        """
        if self.run_allTests:
            for test in tests:
                test["ignore_test"] = False

        results = []
        passed_tests_count = failed_tests_count = ignored_tests_count = 0
        for i, test in enumerate(tests):
            test["ignore_test"] = test.get("ignore_test", False)
            test["linv"] = test.get("linv", None)
            # if test['ignore_test']:
            #     # results.append(f"Test {i} {self.B}didn't check{self.RST}")
            #     continue

            print(f"{self.Y}>> Test {i}:{self.RST}")
            res = self.test_verify(
                P=test["P"],
                program=test["program"],
                Q=test["Q"],
                linv=test.get("linv", None),
                expected_verify_res=test["expected_verify_res"],
                ignore_test=test["ignore_test"],
            )
            if res == 0:
                results.append(f"Test {i} {self.R}failed{self.RST}")
                failed_tests_count += 1
                if self.stop_at_first_fail:
                    break
            elif res == 1:
                results.append(f"Test {i} {self.G}passed{self.RST}")
                passed_tests_count += 1
            elif res == 2:
                results.append(f"Test {i} {self.B}didn't check{self.RST}")
                ignored_tests_count += 1
        print("\n".join(results))
        print(f"{self.G}>> Passed {passed_tests_count}/{len(results)} tests{self.RST}")
        print(f"{self.R}>> Failed {failed_tests_count}/{len(results)} tests{self.RST}")
        print(
            f"{self.B}>> Ignored {ignored_tests_count}/{len(results)} tests{self.RST}"
        )

    def run_all_tests(self):
        "runs all the tests which are added to the `tests` list by the `add_test` function"
        self.test_all(self.tests)


if __name__ == "__main__":
    import z3

    tester = TestVerify()
    # If True, checks all tests, even if they are set to False
    tester.run_allTests = True
    tester.stop_at_first_fail = False  # If True, stops at the first failed test
    tester.stop_at_first_fail = True  # If True, stops at the first failed test

    # TODO:
    # OP['/'] = operator.truediv
    # OP['/'] = operator.floordiv
    
    # TODO: Add the "Shalev" tests

    tester.test_verify(
        # Test #TODO
        P=lambda d: And(d["n"] > 0),
        program="i:=0 ; while (i < n) {i := i + 1 ; if (i >= n/2) {a := n/2 ; skip; } else {skip}}",
        Q=lambda d: And(d["i"] >= d["n"] / 2, d["a"] == d["n"] / 2),
        linv=lambda d: And(d["i"] <= d["n"]),
        expected_verify_res=False,
        ignore_test=True
        # ignore_test=False
    )
        

    tester.add_test(
        # Test 0
        P=lambda _: True,
        program="a := 3 ; b := a ; c := b - 1 ; a := 5;",
        # Q = lambda d: And(d['a'] == d['b'], d['c'] == d['a'] - 1, d['c'] == 2, d['a'] == 3, d['b'] == 3),
        Q=lambda d: And(
            d["b"] == 3,
            d["c"] == d["b"] - 1,
            d["c"] == 2,
            d["a"] == 5,
            d["a"] != d["b"],
        ),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 1
        P=lambda _: True,
        program="a := 2 ; b := a;",
        Q=lambda d: And(d["a"] == 2, d["b"] == 2, d["a"] == d["b"]),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 2
        P=lambda d: And(d["x"] == 5, d['y'] == 2),
        program=r"x:=1 ; if( x < y ) {a := 3 ; b:= a * 2;} else {b := 2;}",
        Q=lambda d: And(
            d["a"] == 3, d["b"] == d["a"] * 2, d["b"] == 6, d["x"] == 1, d["y"] == 2
        ),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 3
        P=lambda _: True,
        program=r" x:=1; y:=2 ; if(x < y) { a := 3 ; b:= a * 2;} else {b := 2 ; } skip ; a := 4 ;",
        Q=lambda d: And(
            d["a"] == 4, d["b"] != d["a"] * 2, d["b"] == 6, d["x"] == 1, d["y"] == 2
        ),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 4
        P=lambda _: True,
        program=r"a := 3; a:= b + 1;",
        Q=lambda d: d["b"] == d["a"] - 1,
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 5
        P=lambda _: True,
        program=r"if (4 < 5) {a := 1;} else {a := 2;}",
        Q=lambda d: d["a"] == 1,
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 6
        P=lambda _: True,
        program="a := b ; while (i < n) { a := a + 1 ; b := b + 1 ; i := i + 1 ;}",
        Q=lambda d: d["a"] == d["b"],
        linv=lambda d: And(d["a"] == d["b"]),
        expected_verify_res=True,
        # ignore_test = False
        ignore_test=True,
    )
    # Following are other programs that you might want to try
    tester.add_test(
        # Test 7  # Program 1 #TODO
        P=lambda d: d["x"] > 0,
        program=r"y := 0 ; while (y < i) {x := x + y ; if ((x * y) < 10) {y := y + 1;} else {skip;} }",
        Q=lambda d: d["x"] > 0,
        linv=lambda d: And(
            d["y"] >= 0,
            d["y"] <= d["i"],
            Or(
                And(d["x"] * d["y"] >= 10, d["x"] == d["x"] + d["y"] * d["i"]),
                And(d["x"] * d["y"] < 10, d["x"] == d["x"] + d["y"] - 1),
            ),
        ),  # figure it out!
        expected_verify_res=False,  # figure it out: True or False
        ignore_test=True,
    )
    tester.add_test(
        # Test 8  # Program 2 (Euclid's algorithm?) #TODO
        P=lambda d: And(d["a"] > 0, d["b"] > 0),
        program=r"while (a != b) {if (a > b) {a := a - b;} else {b := b - a;}}",
        Q=lambda d: And(d["a"] > 0, d["a"] == d["b"]),
        linv=lambda d: And(d["a"] > 0, d["b"] > 0),  # figure it out!
        expected_verify_res=True,  # figure it out: True or False
        ignore_test=True,
    )
    tester.add_test(
        # Test 9
        P=lambda _: True,
        program=r"a := b ; while (i < n) {a := a + 1 ; b := b + 1; } skip ; a := 4;",
        Q=lambda d: And(d["a"] == d["b"], d["a"] == 4),
        linv=lambda d: d["a"] == d["b"],
        expected_verify_res=False,
        ignore_test=True,
    )
    tester.add_test(
        # Test 10
        P=lambda _: True,
        program=r"b := 0; a := b ; i := 0 ; n:=3 ; while (i < n) {a := a + 1 ; b := b + 1 ; i := i + 1;}",
        Q=lambda d: And(d["a"] == 3, d["b"] == 3, d["i"] == d["n"]),
        linv=lambda d: And(d["a"] == d["b"], d["i"] <= d["n"], d["b"] == d["i"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(  # TODO: check this
        # Test 11
        P=lambda d: And(d["i"] == 0, d["n"] == 3, d["b"] == 0),
        program=r" a := b ; while (i < n) {a := a + 1 ; b := b + 1; i := i + 1; }",
        Q=lambda d: And(d["a"] == 3, d["b"] == 3),
        linv=lambda d: And(d["a"] == d["b"], d["i"] <= d["n"], d["b"] == 1 * d["i"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 12
        P=lambda _: True,
        program=r"i := 0 ; n := 3 ; b:=2 ; a := b ; while (i < n) {a := a + 1 ; b := b + 1 ; i := i + 1;} skip;",
        Q=lambda d: d["a"] == 2 + d["n"],  # Or(d['b'] >= 5, d['b'] <= 5),
        linv=lambda d: And(
            d["a"] == d["b"],
            d["i"] <= d["n"],
            d["i"] >= 0,
            d["i"] <= 3,
            d["b"] == 2 + d["i"],
        ),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 13 #From lecture 8, slide 16
        # And(d['x'] == d['y'] , d['i'] > 0),
        P=lambda d: And(d["x"] == Int("y"), Int("i") > 0),
        program=r"x := x + 1;",
        Q=lambda d: And(d["x"] == Int("y") + 1),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 14 # From lecture 7, slide 21
        P=lambda d: And(d["y"] == d["y"]),
        program=r"x := y ; while (i > 0)  { x := x + 1 ; y := y + 1 ; i := i - 1; }",
        Q=lambda d: And(d["x"] == d["y"], Not(d["i"] > 0)),
        linv=lambda d: And(d["x"] == d["y"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 15 - sort two numbers
        P=lambda d: d["a"] != d["b"],
        program=r"if (b < a ) { temp := a ; a := b ; b := temp ;} else {skip;}",
        Q=lambda d: And(d["a"] < d["b"]),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 16 - Not sort two numbers
        P=lambda d: d["a"] != d["b"],
        program=r"if (b < a) {a := b;}",
        Q=lambda d: And(d["a"] < d["b"]),
        linv=None,
        expected_verify_res=False,
        ignore_test=True,
    )
    tester.add_test(
        # Test 17 - Simple program equivalence (two swap programs, verify that they are equivalent)
        P=lambda d: And(d["a"] == d["c"], d["b"] == d["d"]),
        program=r"{temp := a ; a := b ; b := temp;} {c:= d-c ; d:= d-c ; c:= d+c; }",
        # program=r"(temp := a ; a := b ; b := temp ) ; ( c:= d-c ; d:= d-c ; c:= d+c )",
        Q=lambda d: And(d["a"] == d["c"], d["b"] == d["d"]),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 18 - Lection 8, slide 25
        P=lambda d: And(d["n"] >= 0),
        program=r" i := 0 ; while (i < n) {i := i + 1;}",
        Q=lambda d: d["i"] == d["n"],
        linv=lambda d: d["i"] <= d["n"],
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 19 - simple square function (a = n*n = n^2)
        P=lambda d: And(d["n"] >= 0),
        program=r" a:=0; i:=0; while (i < n) {a := a + n ; i := i + 1;}",
        Q=lambda d: d["a"] == d["n"] * d["n"],
        linv=lambda d: And(d["a"] == d["n"] * d["i"], d["i"] <= d["n"]),
        # 'linv': lambda d: And(d['a'] == d['n'] * d['i']), #TODO: check this linv
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 20 - Lecture 8, slide 25
        P=lambda d: d["n"] >= 0,
        program=r" i := 0 ; while (i < n) {i := i + 1;}",
        Q=lambda d: d["i"] == d["n"],
        linv=lambda d: d["i"] <= d["n"],
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 21 - Lecture 8, slide 25
        P=lambda d: d["n"] >= 0,
        program=r"while (i < n) {i := i + 1;}",
        Q=lambda d: d["i"] == d["n"],
        linv=lambda d: d["i"] <= d["n"],
        expected_verify_res=False,
        ignore_test=True,
    )

    tester.add_test(
        # Test 22 -
        P=lambda d: And(d["x"] == Int("y")),
        program=r"x:=x + 1;",
        Q=lambda d: And(d["x"] == Int("y") + 1),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 23
        P=lambda d: d["n"] == 3,
        program=r"i := 0 ; n := 3 ; while (i < n) {i := i + 1 ;}",
        Q=lambda d: And(d["i"] == d["n"], d["i"] == 3),
        # Q = lambda d: And(d['i'] == d['n']),
        linv=lambda d: And(d["i"] <= d["n"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 24
        P=lambda d: Int("n")== 3,  # in case we only consider the variables that are updated by the loop body
        program=r"i := 0  ; while (i < n) {i := i + 1;}",
        Q=lambda d: And(d["i"] == Int("n"), d["i"] == 3),
        linv=lambda d: And(d["i"] <= Int("n")),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 25
        P=lambda d: And(d["n"] >= 0, d["b0"] >= 0),
        # program=r"b := b0;  i := 0 ; while (i < n) { b := b + 1 ; i := i + 1 ;}",
        program=r"int b := b0;  i := 0 ; while (i < n) { b := b + 1 ; i := i + 1 ;}",
        Q=lambda d: And(d["b"] == d["b0"] + d["n"], d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"], d["b"] == d["i"] + d["b0"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 26
        P=lambda d: And(d["n"] >= 0, d["b0"] >= 0, d["x"] >= 0),
        program=r" b := b0;  i := 0 ; while (i < n) { b := b + x ; i := i + 1 ;}",
        Q=lambda d: And(d["b"] == d["b0"] + d["x"] * d["n"], d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"], d["b"] == d["x"] * d["i"] + d["b0"]),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 27
        P=lambda d: And(d["n"] >= 0),
        program=r" n:=5;  x:=3 ; b := 2;  i := 0 ; while (i < n) {b := b + x ; i := i + 1;}",
        Q=lambda d: And(d["b"] == 2 + 3 * 5, d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"], d["b"] == 3 * d["i"] + 2),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 28
        P=lambda d: And(d["n"] >= 0, d["x"] >= 0, d["b0"] >= 0),
        program=" b:=b0; a := b ; i:=0 ; (while i < n do ( a := a + x ; b := b + x; i := i + 1))",
        Q=lambda d: And(
            d["a"] == d["b"], d["b"] == d["b0"] + d["n"] * d["x"], d["i"] == d["n"]
        ),
        linv=lambda d: And(
            d["a"] == d["b"], d["i"] <= d["n"], d["b"] == d["b0"] + d["x"] * d["i"]
        ),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 29
        P=lambda d: And(d["n"] >= 0, d["x"] >= 0, d["b0"] >= 0),
        program=" b:=b0; a := b ; i:=0 ; (while i < n do ( a := a + x ; b := b + x; i := i + 1))",
        Q=lambda d: And(
            d["a"] == d["b"], d["b"] == d["b0"] + d["n"] * d["x"], d["i"] == d["n"]
        ),
        linv=lambda d: And(
            d["a"] == d["b"], d["i"] <= d["n"], d["b"] == d["b0"] + d["x"] * d["i"]
        ),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 30
        P=lambda d: And(d["n"] == 3),
        program="b := 1 ; i:=0; while i < n do ( b := b + 1 ; i := i + 1 )",
        Q=lambda d: And(d["b"] == 4, d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"], d["b"] == d["i"] + 1),
        expected_verify_res=True,
        # ignore_test=False
        ignore_test=True,
    )

    tester.add_test(
        # Test 31
        P=lambda d: And(d["n"] == 3),
        program="b := 0 ; while i < n do ( b := b + 1 ; i := i + 1 )",
        Q=lambda d: And(d["b"] == 3, d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"], d["b"] == d["i"]),
        expected_verify_res=False,  # because the `i` is not defined
        ignore_test=True,
    )
    tester.add_test(
        # Test 32
        P=lambda d: And(d["n"] >= 0),
        program=r"i := 0 ; while (i < n) {i := i + 1;}",
        Q=lambda d: And(d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"]),
        expected_verify_res=True,
        ignore_test=True
        # ignore_test=False
    )

    tester.add_test(
        # Test 33
        P=lambda d: And(d["n"] >= 0),
        program=r"while (i < n) { i := i + 1; }",
        Q=lambda d: And(d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"]),
        expected_verify_res=False,
        ignore_test=True,
    )
    tester.add_test(
        # Test 34
        P=lambda _: True,
        program="i:=0; while i < n do ( i := i + 1 )",
        Q=lambda d: And(d["i"] == d["n"]),
        linv=lambda d: And(d["i"] <= d["n"]),
        expected_verify_res=False,
        ignore_test=True
        # ignore_test=False
    )
    tester.add_test(
        # TODO:
        # Ask about the operator / in the program.
        # for example, in the program `Int('n')/2` the `/` operator is not recognized
        # and throws the following error: `TypeError: unsupported operand type(s) for //: 'ArithRef' and 'int'`
        # Test 35
        P=lambda d: And(d["n"] == 8),
        program=r"a := (n/2);",
        Q=lambda d: And(d["a"] == 4),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 36
        P=lambda d: And(d["n"] == 8, d["i"] == 5),
        program=" a := 0 ; if (i >= (n/2)) then (a := (n/2) ; skip) else skip ",
        Q=lambda d: And(d["i"] >= (d["n"] / 2), d["a"] == (d["n"] / 2), d["a"] == 4),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )

    tester.add_test(
        # Test 37
        P=lambda _: True,
        program="n := 8 ; a := (n/2) ",
        Q=lambda d: And(d["a"] == 4),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 38
        P=lambda d: And(d["x"] == Int("y")),
        program=r"x:=x + 1;",
        Q=lambda d: And(d["x"] + 1 == Int("y")),
        linv=None,
        expected_verify_res=False,
        ignore_test=True,
    )
    tester.add_test(
        # Test 39
        P=lambda d: And(d["n"] >= 0, 0 <= d["i0"], d["i0"] <= d["n"], d["b0"] >= 0),
        program="i:=i0; b:=b0; a := b ; (while i < n do ( a := a + 1 ; b := b + 1; i := i + 1)) ; skip; a := 4 ",
        Q=lambda d: And(d["a"] == 4, d["b"] == d["b0"] + (d["n"] - d["i0"])),
        linv=lambda d: And(
            d["a"] == d["b"],
            d["i"] <= d["n"],
            d["b"] == 1 * (d["i"] - d["i0"]) + d["b0"],
        ),
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 40
        P=lambda d: And(d["n"] >= 0, 0 <= d["i0"], d["i0"] <= d["n"], d["b0"] >= 0),
        program="i:=i0; b:=b0; a := b ; (while i < n do ( a := a + 1 ; b := b + 1; i := i + 1)) ; skip; a := 4 ",
        Q=lambda d: And(d["a"] == d["b"], d["b"] == d["b0"] + (d["n"] - d["i0"])),
        linv=lambda d: And(
            d["a"] == d["b"],
            d["i"] <= d["n"],
            d["b"] == 1 * (d["i"] - d["i0"]) + d["b0"],
        ),
        expected_verify_res=False,
        ignore_test=True,
    )
    tester.add_test(
        # Test 41
        P=lambda d: d["x"] == Int("y"),
        program=r" x := x/2; ",
        Q=lambda d: d["x"] == Int("y") / 2,
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 42
        P=lambda d: And(d["y0"] > 0, d["x"] == Int("y")),
        program=" x := x / y0 ",
        Q=lambda d: d["x"] == Int("y") / d["y0"],
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 43
        P=lambda d: d["x"] == 17,
        program=" x := x / 3 ",
        Q=lambda d: d["x"] == 5,
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )
    tester.add_test(
        # Test 44 - sort(a, b)
        P= lambda d: True,
        program=r""" 
        if ( b < a ) { 
            temp := a ; 
            a := b ; 
            b := temp ;
        } else {
            skip;
        }
        """,
        Q=lambda d: And(d["a"] <= d["b"]),
        linv=None,
        expected_verify_res=True,
        ignore_test=True,
    )

    tester.run_all_tests()
