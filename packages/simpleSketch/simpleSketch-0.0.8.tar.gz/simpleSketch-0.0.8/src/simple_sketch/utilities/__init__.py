# import sys
# import pathlib

# # Add the lib directory to the PYTHONPATH
# f_path = pathlib.Path(__file__).resolve()

# sys.path.extend(str(p) for p in [f_path.parent.parent, f_path.parent.parent/'lib', f_path.parent.parent/'src' ] if p not in sys.path)



from .Utilities import Colors, cprint, dot_print, Print

__all__ = [
    'Colors',
    'cprint',
    'dot_print',
    'Print'
]
