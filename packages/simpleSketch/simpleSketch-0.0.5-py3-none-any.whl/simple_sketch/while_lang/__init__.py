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


from . import syntax
from . import while_language
