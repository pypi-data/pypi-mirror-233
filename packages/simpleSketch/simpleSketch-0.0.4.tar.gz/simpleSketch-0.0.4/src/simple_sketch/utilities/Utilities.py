import sys
from pathlib import Path

# Add the root directory of ex1 to the Python path
# sys.path.extend(str(p) for p in [Path(__file__).parent.parent, Path(__file__).parent.parent/'lib',Path(__file__).parent.parent/'src' ] if p not in sys.path)

from os import linesep, makedirs
from tempfile import NamedTemporaryFile, gettempprefix
from graphviz import Source, Digraph
from typing import Union
from pprint import pprint

from simple_sketch.lib.adt.tree import Tree
from simple_sketch.lib.adt.tree.walk import TreeWalk

class LevelWalk(TreeWalk):
    """
    Description: 
        A level-order walk of a tree.
    """
    def __iter__(self) -> Tree:
        queue = [self.tree]
        while queue:
            node = queue.pop(0)
            yield node
            queue.extend(node.subtrees)



def dot_print(expr: Tree, g_name: str = "G", label: str ="", print_source:bool = False, out_format : str = "pdf", tmp_graph: bool = True, graph_name: str = "graph", only_save: bool = True ) -> None:
    label = label.replace('\\', '\\\\')
    g_name = g_name.replace('\\', '\\\\')
    graph_name = graph_name.replace('\\', '\\\\')
    
    temp = f"""
    // "{label}"
    digraph {g_name}{'{'}
        graph [label="{label}", fontcolor=red, fontsize=14, fontname="Courier New"]
        edge [dir=forward]
    """
    
    nodes = {id(n): (i, n) for (i, n) in enumerate(expr.nodes)}
    edges = {(nodes[id(n)][0], nodes[id(s)][0]) for n in expr.nodes for s in n.subtrees}

    def translate_backslash(x): return str(x).replace("\\", "\\\\")
    
    def get_type(x): 
        ret = ""
        if hasattr(x, 'type'): ret += f"type: {x.type}\n"
        if hasattr(x, 'is_decl'): ret += f"is_decl: True\n"
        if hasattr(x, 'type_var'): ret += f"type_var: {x.type_var}\n"

        return ret
    
    def get_node(x: Tree): return f"{translate_backslash(x.root)}\n{get_type(x)}"


    nodes_string = linesep.join([f"        {i[0]} [label=\"{get_node(i[1])}\"]" for n, i in nodes.items()])
    
    edges_string = linesep.join([f"        {n} -> {s}" for (n, s) in edges])

    if tmp_graph: 
        dir = gettempprefix()
        tmp_file = NamedTemporaryFile(delete=True,  prefix=dir ,suffix=".gv")
        out_file_name=tmp_file.name

    else:
        dir = f"{Path(__file__).parent.parent}/out/"
        makedirs(dir, exist_ok=True)
        out_file_name = f"{dir}/{graph_name}"
        
    s = Source(temp + nodes_string + linesep + edges_string + linesep + "}", filename=f"{out_file_name}", format = out_format)
    if only_save:
        s.render(filename=out_file_name, format = out_format, view=False, cleanup=True)
    else: s.view(filename=out_file_name)
    
    
    if(print_source): print(s.source)
    
    
class Colors:
    # https://ss64.com/nt/syntax-ansi.html
    # ANSI escape sequences for text colors
    # Font colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_YELLOW = "\033[93m"  
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_RED = "\033[91m" 
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    
    # Font styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # ANSI escape sequence for resetting text color
    RESET = '\033[0m'
    # Default text colors
    HEADER = BRIGHT_MAGENTA
    OKBLUE = BRIGHT_BLUE
    OKCYAN = BRIGHT_CYAN
    OKGREEN = BRIGHT_GREEN
    WARNING = BRIGHT_YELLOW
    FAIL = BRIGHT_RED

class Print(object):
    
    def __init__(self, color: Union[str, Colors, None] = None, style: Union[str ,Colors, None] = None) -> None:
        self.color = Colors.RESET if color is None else color
        self.style = Colors.RESET if style is None else style
    
    # TODO: Change it to accept a series of text to print. i.e the same behavior as print
    def __call__(self, *text) -> None:
        print(self.style,self.color, sep='', end='')
        print(*text, sep='', end='')
        print(Colors.RESET, sep='', end='\n')

# TODO: Change it to accept a series of text to print. i.e the same behavior as print
def cprint(*texts, color: Union[str, Colors, None] = None, style: Union[str ,Colors, None] = None) -> None:
    """
    `cprint` print colored text in the terminal.

    Args:
        texts : The texts to be printed.
        color (Union[str, Colors, None], optional): the color of the text. Defaults to None.
        style (Union[str, Colors, None], optional): the style of the text. Defaults to None.
    """
    color_print = Print(color, style)
    color_print(*texts)

def print_sys_path(file_path : Path = Path(__file__)):
    print("-----------------------------------------------------")
    # print sys.path in red color
    print("\033[31m" + "sys.path:\n" + "\033[0m")
    pprint(sys.path)
    
    # print file name and path
    paths = {"file name": file_path.name,
             "parent path": file_path.parent,
             "parent parent path": file_path.parent.parent}
    
    # print paths in (key in red color) : (value in blue color)
    for key, value in paths.items():
        print("\033[31m" + key + "\033[0m", ":", "\033[34m" + str(value) + "\033[0m")
    print("-----------------------------------------------------")

def print_dict(dictionary, indent=''):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f"{indent}{key}:")
            print_dict(value, indent + '  ')
        else:
            print(f"{indent}\"{key}\": \"{value}\"")



if __name__ == "__main__":
    # print_sys_path()

    dot = Digraph(comment='The Round Table')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')
    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')
    print(dot)  #doctest: +NORMALIZE_WHITESPACE
    dot.save('test-output/round-table.gv')
    

