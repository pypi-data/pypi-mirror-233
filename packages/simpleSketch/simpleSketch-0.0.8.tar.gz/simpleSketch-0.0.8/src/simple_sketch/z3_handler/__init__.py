# import sys
# import pathlib

# # Add  the following paths to sys.path:
# sys.path.extend([
#     str(p)
#     for p in [
#         pathlib.Path(__file__).parent, # src/while_lang
#         pathlib.Path(__file__).parent.parent, # src
#         pathlib.Path(__file__).parent.parent.parent, # root of the project
#         pathlib.Path(__file__).parent.parent.parent/"lib", # lib
#     ]
#     if p not in sys.path]
# )


from .z3_handler import (Z3_TYPE, Z3_VAL, print_z3, substitute_z3, solve_z3, get_all_z3_vars)
from . import z3_text_parser


__all__ = [
    "Z3_TYPE",
    "Z3_VAL", 
    "print_z3", 
    "substitute_z3", 
    "solve_z3",
    "get_all_z3_vars",
    "z3_text_parser"
]
