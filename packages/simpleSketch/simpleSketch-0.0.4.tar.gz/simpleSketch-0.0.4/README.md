# Simple Sketch (Program Synthesis by Sketching)

>This project is a part of the course 236347 Software Synthesis and Automated Reasoning (SSAR) at the Technion.

## Description

The goal of software synthesis is to generate programs automatically from specifications.
In Sketching, insight is communicated through a partial program, a sketch that
expresses the high-level structure of an implementation but leaves holes in place of the low-level details.

Simple Sketch can Synthesis a program based on a set of input and output examples, or by adding assertions to the program.

Simple Sketch uses counterexample guided inductive synthesis procedure (CEGIS) to synthesize a program.

Look at the examples section in the GUI to see how to use the program.

>> **Note:** This project is still under development. Check updates regularly at the [SimpleSketch repository](https://github.com/maher-bisan/SimpleSketch)

>>**IMPORTANT:** The tests (under `/tests`) still fail, because the tests are not updated to the new version of the program (the new parser)
The tests will be updated soon. In the meantime, you can use the examples in the GUI to test the program.

## Example

```
i := ??;
y := i*i + x * ??;
assert (y == x + x + 9);
```
The above program is a simple example of a program synthesis problem.
The goal is to find a program that satisfies the specification.

After running the program, the output is:

```
i := 3;
y := i*i + x * 2;
assert (y == x + x + 9);
```

## Installation

### Build from source

```
git clone https://github.com/maher-bisan/SimpleSketch.git
cd simple_sketch
python3.11 -m venv .venv
source .venv/bin/activate
pip install .
```

On windows, run the following command instead:

```
python -m venv .venv
.venv\Scripts\activate
pip install .
```

### Install from PyPI

```
pip install simpleSketch
```

## Documentation

Under construction. In the meantime, you can read the docstrings in the code.

## Usage

### Open the GUI

In the terminal, run the following command:

```
python3.11 src/simple_sketch/simple_sketch_gui/simple_sketch_gui.py
```

Or, if used pip to install the package, run the following command:

```
simpleSketch-gui
```

### Examples

After opening the GUI, you can select an example from the dropdown menu, at the sidebar.

### Run a program

To run a program, click the "Run" button.
Click the "Clear" button to clear the entire text areas.
