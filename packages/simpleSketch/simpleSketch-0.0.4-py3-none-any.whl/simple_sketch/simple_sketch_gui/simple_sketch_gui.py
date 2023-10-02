"""
 - file: simple_sketch_gui.py
 - author: Maher Biasn
 - date: September 2023
 - description: simple sketch gui module for the project. 
    This module is used to create a simple gui for the project, using tkinter.
"""


import os
import sys
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk 
import tkinter.messagebox
# from CTkToolTip import CTkToolTip
import traceback

from typing import List, Tuple, Dict
# TODO
import threading 
from textwrap import dedent

from simple_sketch.simple_sketch import SimpleSketch
from simple_sketch.utilities import Colors
# ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_widget_scaling(1.0)



# To Enable Resizing
def start_resize(event, master):
    # master.resizing = True
    # master.prev_x = event.x
    # master.prev_y = event.y
    x, y = event.x, event.y
    width, height = master.winfo_width(), master.winfo_height()
    
    print("-"*50)
    print(f"width = {width}")
    print(f"event.x = {event.x}")
    print(f"width - x = {width - x}\n")
    
    print(f"height = {height}")
    print(f"event.y = {event.y}")
    print(f"height - y = {height - y}")
    
    if (width - x <= master.grip_size or x < master.grip_size ) or ( height - y <= master.grip_size or y <= master.grip_size):
        master.resizing = True
        master.start_x = x
        master.start_y = y

def stop_resize(event, master):
    master.resizing = False


def do_resize(event, master, horizontal=True, vertical=True):
    master.resizing = getattr(master, "resizing", False)
    if not master.resizing:
        return
    x, y = event.x, event.y
    dx, dy = x - master.start_x, y - master.start_y

    if horizontal:
        master.configure(width= master.winfo_width() + dx)
        master.start_x = x
    if vertical:
        master.configure(height=  master.winfo_height() + dy)
        master.start_y = y

def enable_resizing(master, horizontal=True, vertical=True):
    master.resizing = False
    master.grip_size = 20
    # Enable resizing of the textBox
    master.bind("<ButtonPress-1>", lambda event: start_resize(event, master))
    master.bind("<ButtonRelease-1>", lambda event: stop_resize(event, master))
    master.bind("<B1-Motion>", lambda event: do_resize(event, master, horizontal, vertical))



class SideBarFrame(ctk.CTkFrame):
    def __init__(self, master, debug: bool = False,**kw):
        super().__init__(master, **kw)
        self.debug = debug
        self.grid_rowconfigure(6, weight=1)
        
        
        self.logo_label = ctk.CTkLabel(self, text="Simple Sketch\nSideBar", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self, text="About", command=self.about_button_callback)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        # Examples
        self.examples_label = ctk.CTkLabel(self, text="Examples:", anchor="w")
        self.examples_label.grid(row=4, column=0, padx=20, pady=(10, 10))
        
        self.examples_mvar = tk.StringVar()
        self.examples_optionemenu = ttk.OptionMenu(self, variable=self.examples_mvar, default="Examples")
        self.examples_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
        examples_optionemenu: tk.Menu = self.examples_optionemenu['menu']
        
        
        self.set_examples_menu(master_menu = examples_optionemenu, examples_path = "src/simple_sketch/simple_sketch_gui/assets/examples")
        
        # Icons
        icons_buttons = ['GitHub.png', 'Pypi.png', 'Docs.png']
        for i, image in enumerate(icons_buttons):
            # button = ctk.CTkButton(self.icons_frame, image=image, width=50, height=50)
            button = ctk.CTkButton(self, text=image, width=50, height=50, command=self.sidebar_button_event)
            button.grid(row=7+i, column=0, padx=20, pady=(20, 20))
            
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(10, 10))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=12, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=13, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
    
    def set_examples_menu(self, master_menu: tk.Menu, examples_path:str):
        """
         
        """
        if self.debug :
            print(f"set_examples_menu: {examples_path}")
        examples_list = []
        
        for file in os.listdir(examples_path):
            file_path = os.path.join(examples_path, file)
            # In case it is directory
            if os.path.isdir(file_path):
                examples_menu = tk.Menu(master_menu, tearoff=0)
                master_menu.add_cascade(label=file, menu = examples_menu)
                self.set_examples_menu(examples_menu, file_path)
            # In case it is file
            elif os.path.isfile(file_path) and (file.endswith(".json") or file.endswith(".yaml")):
                example_name = file[:-5]
                # master_menu.add_command(label=example_name, command = lambda file_path=file_path: self.load_example(file_path))
                master_menu.add_command(label=example_name, command = lambda file_path=file_path: self.load_example(file_path))
        if self.debug : print(f"examples_list: {examples_list}")
        return examples_list
    
    def load_example(self, example_path: str):
        """
        """
        import json
        import yaml 
        print(f"load_example: {example_path}")
        
        def replace_none_with_empty_string(d):
            if isinstance(d, dict):
                return {k: replace_none_with_empty_string(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [replace_none_with_empty_string(x) for x in d]
            else:
                return "" if d is None else d
        
        self.examples_mvar.set("/".join(example_path.split("/")[5:])[:-5])
        
        try:
            with open(example_path, "r") as f:
                if example_path.endswith(".json"):
                    example_file : Dict = json.load(f)
                elif example_path.endswith(".yaml"):
                    example_file: Dict = yaml.safe_load(f)
                else:
                    raise Exception(f"Unsupported file type: {example_path}")
                
                example_file = replace_none_with_empty_string(example_file)
                
                program = example_file.get("program", "")
                input_output_examples: List[Tuple[str,str,str]] = []
                for example in example_file.get("input_output_examples", {}):
                    input_output_examples.append((example.get("input", ""), example.get("output", ""), 
                                                  example.get("vars", "")))
                
                pre_condition = example_file.get("pre_condition", {})
                post_condition = example_file.get("post_condition", {})
                loop_inv = example_file.get("loop_inv", {})
                
                self.master.main_frame.conditions_frame.insert_conditions(
                        pre_cond = pre_condition.get("condition", ""), pre_cond_vars = pre_condition.get("condition_vars", ""),
                        post_cond = post_condition.get("condition", ""), post_cond_vars = post_condition.get("condition_vars", ""),
                        loop_inv = loop_inv.get("condition", ""), loop_inv_vars = loop_inv.get("condition_vars", "")
                        )
                
                self.master.main_frame.program_to_sketch.insert_program(program)
                self.master.main_frame.inout_examples_frame.insert_inout_examples(input_output_examples)
                self.master.main_frame.output_frame.clear()
                
                
        except Exception as e:
            # TODO: handle the exception better
            print(f"Error: {e}")
            traceback.print_exc()
            tkinter.messagebox.showerror(title="Error", message=f"Error: {e}")
            return

    def set_menu_example_event(self):
        new_example = self.examples_mvar.get()
        print(f"new_example: {new_example}")
        tkinter.messagebox.showinfo(title="Example", message= new_example)
        
    def set_example_event(self, new_example: str):
        print(f"new_example: {new_example}")
        tkinter.messagebox.showinfo(title="Example", message=f"new_example:\n{new_example}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)               

    def sidebar_button_event(self):
        print("sidebar_button click")

    def about_button_callback(self):
        """
        ---------------------------------------------------------------------
        | This function is called when the 'about' button is pressed.        |
        | It should show a pop up window with information about the project. |
        ---------------------------------------------------------------------
        """
        print("about_button_callback called")
        # Create a new window
        about_window = tk.Toplevel(self)
        about_window.title("About")
        # Create a frame to hold the text
        about_frame = tk.Frame(about_window)
        about_frame.pack(fill="both", expand=True)
        ABOUT_TEXT = "ABOUT_TEXT"
        # Create a label with the text to display in the window
        about_text = tk.Label(about_frame, text=ABOUT_TEXT)
        about_text.pack(fill="both", expand=True)
        # Create a button to close the window
        about_close_button = tk.Button(about_frame, text="Close", command=about_window.destroy)
        about_close_button.pack(fill="both", expand=True)
        # Set the window to the center of the screen
        about_window.update_idletasks()
        about_window.geometry("+%d+%d" % (about_window.winfo_screenwidth() // 2, about_window.winfo_screenheight() // 2))
        about_window.mainloop() # Start the Tkinter event loop


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, windo_title:str = 'info', windo_text: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x300")
        self.title = windo_title
        self.windo_title = windo_title

        self.label = ctk.CTkLabel(self, text=windo_title)
        self.label.pack(padx=20, pady=20)
        
        self.text = ctk.CTkTextbox(self, width=400, height=250, font=ctk.CTkFont(size=14))
        self.text.pack(padx=20, pady=20)
        self.text.insert("0.0", windo_text)
        self.text.configure(state="disabled")
        enable_resizing(self.text)
        
        # Create a button to close the window
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=20, pady=20)
        
        self.configure(border_width=1, border_color="gray")


class InfoWindoButton(ctk.CTkButton):
    def __init__(self, master, windo_title:str = 'info', windo_text: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.windo_title = windo_title
        self.windo_text = windo_text
        self.toplevel_window = None
        
        self.bind("<Button-1>", self.open_toplevel) 
        
        

    def open_toplevel(self, event):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(windo_title=self.windo_title, windo_text=self.windo_text)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it



class InOutExamplesFrame(ctk.CTkScrollableFrame):
    
    def __init__(self,  master, debug: bool = False, **kw):
        super().__init__(master, **kw)
        self.debug = debug
        # Bug in the mouse-wheel binding of CTkScrollableFrame.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356#issuecomment-1474104298
        self.bind("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        
        self.propagate(False)
        self.configure(width=300, height=350)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((4), weight=1)
        # enable_resizing(self)
        
        self.inout_examples_list: List[Tuple[str, str, str]] = []
        
        self.label = ctk.CTkLabel(self, text="In/Out Examples", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        # ---- Frame to take the input/output examples ---
        self.in_out_examples_frame = ctk.CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.in_out_examples_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.in_out_examples_frame.grid_columnconfigure(0, weight=1)
        # self.in_out_examples_frame.grid_rowconfigure((0,1,2,), weight=1)
        self.example: Dict[str, ctk.CTkTextbox] = {} 
        for i, example_part in enumerate(["Input Example", "Output Example", "Vars"]):
            example_label = ctk.CTkLabel(self.in_out_examples_frame, text=example_part, font=ctk.CTkFont(weight="bold"))
            example_label.grid(row=i*2, column=0, sticky="nw")
            self.example[example_part] = ctk.CTkTextbox(self.in_out_examples_frame, width=300, height=50)
            self.example[example_part].grid(row=i*2+1, column=0, sticky="nsew")
            # Enable resizing of the textBox
            enable_resizing(self.example[example_part])


        # ---- Buttons frame ---
        self.Buttons_frame = ctk.CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.Buttons_frame.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.Buttons_frame.grid_rowconfigure(0, weight=1)
        self.Buttons_frame.grid_columnconfigure((0,1), weight=1)
        # add_examples_buttons
        self.add_examples_button = ctk.CTkButton(self.Buttons_frame, text="Add Example", width=50, height=50, command=self.add_example_event)
        self.add_examples_button.grid(row=0, column=0, sticky="nsew", padx=(20,10), pady=(10,10))
        # examples_list_buttons
        self.clear_examples_list_button = ctk.CTkButton(self.Buttons_frame, text="Clear List", width=50, height=50,command=self.clear_examples_list)
        self.clear_examples_list_button.grid(row=0, column=1, sticky="nsew", padx=(10,20), pady=(10,10))
        self.Buttons_frame.configure(border_width=1, border_color="gray")
        
        # ---- input/output examples list ---
        self.examples_list_label = ctk.CTkLabel(self, text="Examples List", font=ctk.CTkFont(weight="bold"))
        self.examples_list_label.grid(row=3, column=0, padx=(20,20), pady=(5,5), sticky="nw")
        self.examples_list_textbox = ctk.CTkTextbox(self, width=300, height=200)
        self.examples_list_textbox.grid(row=4, column=0, padx=(20,20), pady=(5,5), sticky="nsew")
        self.examples_list_textbox.configure(state="disabled")  # configure textbox to be read-only
        # Enable resizing of the textBox
        enable_resizing(self.examples_list_textbox)

        # Show the input/output examples list 
        self.show_examples_list()
    
    def add_example_event(self):
        in_example = self.example['Input Example'].get("0.0", "end")
        out_example = self.example["Output Example"].get("0.0", "end")
        examples_vars = self.example["Vars"].get("0.0", "end")
        if self.debug:
            print(f"in_example: {in_example}")
            print(f"out_example: {out_example}")
            print(f"examples_vars: {examples_vars}")
        
        self.inout_examples_list.append((in_example, out_example, examples_vars))
        self.show_examples_list()
    
    def show_examples_list(self):
        self.examples_list_textbox.configure(state="normal")  # configure textbox to be read-only
        self.examples_list_textbox.delete("0.0", "end")
        for i, (in_example, out_example, examples_vars) in enumerate(self.inout_examples_list):
            self.examples_list_textbox.insert("end", f"Example {i+1}:\n")
            self.examples_list_textbox.insert("end", f"Input: {in_example}\n")
            self.examples_list_textbox.insert("end", f"Output: {out_example}\n")
            self.examples_list_textbox.insert("end", f"Vars: {examples_vars}\n")
            self.examples_list_textbox.insert("end", "\n")
        self.examples_list_textbox.configure(state="disabled")  # configure textbox to be read-only

    def insert_inout_examples(self, inout_examples: List[Tuple[str, str, str]]):
        self.inout_examples_list = inout_examples
        self.clear_examples_input_textbox()
        self.show_examples_list()

    def clear_examples_list(self):
        self.inout_examples_list = []
        self.show_examples_list()

    def get_inout_examples(self) -> List[Tuple[str, str, str]]:
        return self.inout_examples_list
    
    def clear_examples_input_textbox(self) -> None:
        for example in self.example.values():
            example.delete("0.0", "end")
    
    def clear(self) -> None:
        self.clear_examples_input_textbox()
        self.clear_examples_list()

class CondFrame(ctk.CTkScrollableFrame):
    class CondInputFrame(ctk.CTkFrame):
        def __init__(self, master, condition_name:str, **kw):
            super().__init__(master, **kw)
            # self.m
            self.propagate(False)
            # self.configure(width=300, height=350)
            self.grid_columnconfigure((0,1,2), weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure((1,2), weight=2)
            # enable_resizing(self)
        
            # section label
            self.label = ctk.CTkLabel(self, text=condition_name, font=ctk.CTkFont(weight="bold"))
            self.label.grid(row=0, column=0, sticky="nw")
            
            # section info button
            # self.info_btn = ctk.CTkButton(self, text="info", width=50,
            #                          command = lambda section_info=condition_name: self.show_section_info(section_info))
            self.info_btn = InfoWindoButton(master=self, text="info", width=100, windo_title=f"INFO FOR: {condition_name}",
                                            windo_text=f"INFO FOR: {condition_name}\n"\
                                            + "* The `condition` should be in Z3 syntax.\n"\
                                            + "* `vars` is the types of the variables in the condition.\n"\
                                            + "* The syntax is: `var1: type1, var2: type2,..., var{i}: type{i}`.\n"\
                                            + "* `var{i}` : is the name of the variable.\n"\
                                            + "* `type{i}` is the type of the variable `var1`.\n"\
                                            + "* `type{i}` can be one of the following types: `int`, `bool`, `Array int`, `Array bool`.\n"\
                                            + "* The types of the variables should be the same as the variables in the program."
            )
            
            
            self.info_btn.grid(row=0, column=1, sticky="nw", padx=(5,5), pady=(10,10))

            
            # condition
            self.condition = ctk.CTkTextbox(self, width=250, height=50)
            self.condition.grid(row=1, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky="nsew" )
            self.condition.insert("0.0", "Some example text!")

            # condition vars
            self.condition_vars = ctk.CTkTextbox(self, width=250, height=50)
            # self.condition_vars.grid(row=2, column=0, columnspan=3, padx=(10,10), pady=(10,10) )
            self.condition_vars.insert("0.0", "vars example")
            
            # Button to toggle the visibility of the section vars.
            self.show_vars_btn = ctk.CTkButton(self, text="show vars", width=50,
                                          command=lambda entry=self.condition_vars: self.toggle_button(entry))
            self.show_vars_btn.grid(row=0, column=2,padx=(5,20), pady=(10,10), sticky="nsew")
        
        def insert_cond(self, cond: str, cond_vars: str) -> None:
            self.condition.delete("0.0", "end")
            self.condition.insert("0.0", cond)
            self.condition_vars.delete("0.0", "end")
            self.condition_vars.insert("0.0", cond_vars)
        
        def get_cond(self) -> str:
            cond = self.condition.get("0.0", "end")[:-1]
            vars = self.condition_vars.get("0.0", "end")
            return f"{cond} --types{'{'}{vars}{'}'}"
        
        def show_section_info(self, section):
            tkinter.messagebox.showinfo("Section Info", f"Information for {section}")

        def toggle_button(self, entry):
            if entry.winfo_viewable():
                entry.grid_remove()
            else:
                entry.grid(row=2, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky="nsew")
        
    def __init__(self,  master, **kw):
        super().__init__(master, **kw)
        # Bug in the mouse-wheel binding of CTkScrollableFrame.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356#issuecomment-1474104298
        self.bind("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        
        self.propagate(False)
        self.configure(width=500, height=300)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        
        self.conditions: Dict[str, 'CondFrame.CondInputFrame'] = {}
        # Create the conditions inputs for the program
        sketch_inputs = ["Pre-condition", "Post-condition", "Loop-inv"]
        r = -1
        for i, condition_name in enumerate(sketch_inputs):
            c = i % 2
            r += 1 if c == 0 else 0 
            # Frame for each section
            self.conditions[condition_name] = self.CondInputFrame(master=self, condition_name=condition_name, bg_color="transparent", fg_color="transparent")
            self.conditions[condition_name].grid(row=r, column=c, padx=(10,10), pady=(10,10), sticky="nsew")
            self.conditions[condition_name].configure(border_width=1, border_color="gray")
            enable_resizing(self.conditions[condition_name].condition, horizontal=False)

    def insert_conditions(self, 
                         pre_cond: str, pre_cond_vars: str,
                         post_cond: str, post_cond_vars: str,
                         loop_inv: str, loop_inv_vars: str) -> None:
        "Insert the conditions into the GUI"
        self.conditions["Pre-condition"].insert_cond(pre_cond, pre_cond_vars)
        self.conditions["Post-condition"].insert_cond(post_cond, post_cond_vars)
        self.conditions["Loop-inv"].insert_cond(loop_inv, loop_inv_vars)
    
    def get_pre_condition_and_vars(self) -> Tuple[ctk.CTkTextbox, ctk.CTkTextbox]:
        "Return the `pre-condition` TextBox and the pre-condition `vars` TextBox"
        return self.conditions["Pre-condition"].condition, self.conditions["Pre-condition"].condition_vars

    def get_pre_condition_and_vars_str(self) -> Tuple[str, str]:
        "Return the `pre-condition` as string and the pre-condition `vars` as string"
        cond, vars =  self.get_pre_condition_and_vars()
        return (dedent(cond.get("0.0","end-1c")), dedent(vars.get("0.0","end-1c")))

    def get_post_condition_and_vars(self) -> Tuple[ctk.CTkTextbox, ctk.CTkTextbox]:
        return self.conditions["Post-condition"].condition, self.conditions["Post-condition"].condition_vars

    def get_post_condition_and_vars_str(self) -> Tuple[str, str]:
        cond, vars =  self.get_post_condition_and_vars()
        return (dedent(cond.get("0.0","end-1c")), dedent(vars.get("0.0","end-1c")))

    def get_loop_inv_and_vars(self) -> Tuple[ctk.CTkTextbox, ctk.CTkTextbox]:
        return self.conditions["Loop-inv"].condition, self.conditions["Loop-inv"].condition_vars

    def get_loop_inv_and_vars_str(self) -> Tuple[str, str]:
        cond, vars =  self.get_loop_inv_and_vars()
        return (dedent(cond.get("0.0","end-1c")), dedent(vars.get("0.0","end-1c")))

    def clear(self) -> None:
        for condition in self.conditions.values():
            condition.condition.delete("0.0", "end")
            condition.condition_vars.delete("0.0", "end")

class OutPutFrame(ctk.CTkScrollableFrame):
    
    def __init__(self,  master, **kw):
        super().__init__(master, **kw)
        # Bug in the mouse-wheel binding of CTkScrollableFrame.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356#issuecomment-1474104298
        self.bind("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        
        self.propagate(False)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        
        self.output_frame_label = ctk.CTkLabel(self, text="Sketch Output", font=ctk.CTkFont(size=20, weight="bold"))
        self.output_frame_label.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nw")
        
        # FIXME: change `ctk.CTkTextbox` to the correct widget
        self.output_textbox = ctk.CTkTextbox(self, width=600, height=350)
        self.output_textbox.grid(row=1, column=0, columnspan=2, padx=20, sticky="nsew")
        enable_resizing(self.output_textbox)
    
    def clear(self) -> None:
        self.output_textbox.delete("0.0", "end")
    def get_output_textbox(self) -> ctk.CTkTextbox:
        return self.output_textbox

class ProgToSketchFrame(ctk.CTkScrollableFrame):
    
    def __init__(self,  master, **kw):
        super().__init__(master, **kw)
        # Bug in the mouse-wheel binding of CTkScrollableFrame.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356#issuecomment-1474104298
        self.bind("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        
        self.propagate(False)
        self.configure(width=600, height=250)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        
        # section label
        self.prog_to_sketch_label = ctk.CTkLabel(self, text="Program to sketch", compound="left", font=ctk.CTkFont(weight="bold"))
        self.prog_to_sketch_label.grid(row=0, column=0, sticky="nw")
        
        # section info button
        self.info_btn = ctk.CTkButton(self, text="info", width=50,
                                    command = lambda section_info="Program to sketch": self.show_section_info(section_info))
        self.info_btn.grid(row=0, column=1, sticky="nw")

        # section input
        self.prog_to_sketch = ctk.CTkTextbox(self, width=600, height=300)
        self.prog_to_sketch.grid(row=1, column=0, padx=20, columnspan=2, sticky="nsew")
        # self.prog_to_sketch.insert("0.0", "Some example text!") # TODO: place holder
        enable_resizing(self.prog_to_sketch)
    
    def clear(self) -> None:
        self.prog_to_sketch.delete("0.0", "end")

    def insert_program(self, program: str) -> None:
        self.prog_to_sketch.delete("0.0", "end")
        self.prog_to_sketch.insert("0.0", program)
        self.prog_to_sketch.see("end") # scroll to the end of the program
        self.prog_to_sketch.focus() # focus on the program textbox
        self.prog_to_sketch.update() # update the program textbox
        self.prog_to_sketch.update_idletasks() # update the program textbox

    
    def get_program(self) ->  ctk.CTkTextbox:
        return self.prog_to_sketch

    def get_program_str(self) -> str:
        return dedent(self.prog_to_sketch.get("0.0", "end-1c"))
    
    def show_section_info(self, section):
        tkinter.messagebox.showinfo("Section Info", f"Information for {section}")
        
        
class ControlFrame(ctk.CTkFrame):
    
    def __init__(self,  master, **kw):
        super().__init__(master, **kw)
        self.propagate(False)
        self.configure(height=250, width=200)
        self.grid_columnconfigure((0,1,2), weight=1)
        # self.grid_rowconfigure((0,1), weight=0)
        # self.grid_rowconfigure((1,2), weight=1)
        # self.grid_rowconfigure((2), weight=2)
        # enable_resizing(self)
        
        # Add Entrys for timeout, number of unrolls, max number of iterations
        timeout_label = ctk.CTkLabel(self, text="Timeout (ms)", font=ctk.CTkFont(weight="bold", size=10))
        timeout_label.grid(row=0, column=0, padx=(20, 5), pady=(5,5), sticky="nsew")
        self.timeout_entry = ctk.CTkEntry(self, width=15, height=10)
        self.timeout_entry.grid(row=1, column=0, padx=(20, 20), pady=(5,20), sticky="we")
        self.timeout_entry.insert("0", "1000")
        
        unroll_label = ctk.CTkLabel(self, text=" # of loop unrolling", font=ctk.CTkFont(weight="bold", size=10))
        unroll_label.grid(row=0, column=2, padx=(20, 5), pady=(5,0), sticky="nsew")
        self.unroll_entry = ctk.CTkEntry(self, width=15, height=10)
        self.unroll_entry.grid(row=1, column=2, padx=(20, 20), pady=(5,20), sticky="we")
        self.unroll_entry.insert("0", "8")
        
        iterations_label = ctk.CTkLabel(self, text="Max iterations #", font=ctk.CTkFont(weight="bold", size=10))
        iterations_label.grid(row=0, column=1, padx=(20, 5), pady=(5,0), sticky="nsew")
        self.iterations_entry = ctk.CTkEntry(self, width=15, height=10)
        self.iterations_entry.grid(row=1, column=1, padx=(20, 20), pady=(5,20), sticky="we")
        self.iterations_entry.insert("0", "100")
        
        
        buttons: List[ctk.CTkButton] = []
        for i, btn in enumerate(['run', 'clear', 'debug']):
            buttons.append(ctk.CTkButton(self, text=btn, width=50, height=40))
            buttons[-1].grid(row=2, column=i, padx=(20,20), pady=(20,20), sticky="we")
        
        self.run_btn, self.clear_btn, self.debug_btn = buttons
        
        # Add Checkboxes for the debug mode
        self.debug_mode = ctk.BooleanVar(value=True)
        self.debug_mode_checkbox = ctk.CTkCheckBox(self, text="Debug mode", variable=self.debug_mode)
        # self.debug_mode_checkbox.grid(row=3, column=1, columnspan=3, padx=(20,20), pady=(20,20), sticky="we")
        self.debug_mode_checkbox.grid(row=3, column=1, padx=(20,20), pady=(20,20), sticky="news")
        
        

class MainFrame(ctk.CTkScrollableFrame):
    
    def __init__(self,  master, debug: bool = False, **kw):
        super().__init__(master, **kw)
        self.debug = debug
        # Bug in the mouse-wheel binding of CTkScrollableFrame.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356#issuecomment-1474104298
        self.bind("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        
        self.propagate(False)
        self.configure(bg_color="#242424", fg_color="#242424")
        # self.configure(width=1000, height=600)
        # self.grid_columnconfigure((0,1,2), weight=1)
        # self.grid_rowconfigure((0,1,2), weight=1)
        
        # -------- conditions frame --------
        self.conditions_frame = CondFrame(master=self, bg_color="transparent", border_width=1, border_color="gray")
        self.conditions_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=20, pady=(10,10), sticky="nsew")
        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        
        ## -------- main.program_to_sketch frame --------
        self.program_to_sketch = ProgToSketchFrame(self, bg_color="transparent", border_width=1, border_color="gray")
        self.program_to_sketch.grid(row=2, column=0, padx=20, pady=(10,10), columnspan=2, sticky="nsew")


        # --------- inout_examples frame --------
        self.inout_examples_frame = InOutExamplesFrame(master=self, border_width=1, border_color="gray")
        self.inout_examples_frame.grid(row=0, column=2, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")        
        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure(2, weight=1)

        # --------- Output frame --------
        self.output_frame = OutPutFrame(master=self, width=600, height=280, border_width=1, border_color="gray")
        self.output_frame.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure((0,1), weight=1) 
      
        # --------- Control frame -------
        self.control_frame = ControlFrame(master=self, border_width=1, border_color="gray")
        self.control_frame.grid(row=3, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # --------- bind events -------
        self.control_frame.debug_btn.bind("<Button-1>", self.debug_btn_event)
        self.control_frame.run_btn.bind("<Button-1>", self.run_btn_event)
        self.control_frame.clear_btn.bind("<Button-1>", self.clear_btn_event)
    
    def clear_btn_event(self, event):
        print("clear_btn_event")
        self.conditions_frame.clear()
        self.program_to_sketch.clear()
        self.inout_examples_frame.clear()
        self.output_frame.clear()
        
    def run_btn_event(self, event):
        print("run_btn_event")
        pre_cond, pre_vars = self.conditions_frame.get_pre_condition_and_vars_str()
        post_cond, post_vars = self.conditions_frame.get_post_condition_and_vars_str()
        linv, linv_vars = self.conditions_frame.get_loop_inv_and_vars_str()
        program_to_sketch = self.program_to_sketch.get_program_str()
        inout_examples_list = self.inout_examples_frame.get_inout_examples()
        
        timeout = int(self.control_frame.timeout_entry.get())
        unroll = int(self.control_frame.unroll_entry.get())
        iterations = int(self.control_frame.iterations_entry.get())
        
        
        
        output_textbox = self.output_frame.get_output_textbox()
        output_textbox.delete("0.0", "end")
        output_textbox.tag_config("red", foreground="red")
        output_textbox.tag_config("green", foreground="green")
        output_textbox.tag_config("blue", foreground="blue")
        output_textbox.tag_config("magenta", foreground="magenta")
        
        try:
            synthesizer_res = SimpleSketch(
                max_itr_num=iterations, 
                timeout = timeout, 
                num_to_unroll_while_loops = unroll,
                debug = self.control_frame.debug_mode.get()
                ).synthesize(
                program = program_to_sketch,
                input_output_examples = inout_examples_list,
                pre_condition = f"{pre_cond} --types={'{'}{pre_vars}{'}'}",
                post_condition = f"{post_cond} --types={'{'}{post_vars}{'}'}",
                loop_inv = f"{linv} --types={'{'}{linv_vars}{'}'}",
            )
            if synthesizer_res:
                synthesized_program = synthesizer_res[0]
                hole_values = synthesizer_res[1]
                verify_res = synthesizer_res[2] 
                verify_examples_res = synthesizer_res[3]
                output_textbox.insert("end", "The synthesized program is correct.\n", "green")
                output_textbox.insert("end", f"The Holes values are:\n", "blue")
                output_textbox.insert("end", f"{hole_values}\n")
                output_textbox.insert("end", f"The final synthesized program:\n", "blue")
                output_textbox.insert("end", f"{synthesized_program}")            
            else:
                output_textbox.insert("end", "The synthesized program is not correct.\n", "red")
                output_textbox.insert("end", f"You may Try to:\n", "red")
                output_textbox.insert("end", f"     1. If you have `loop inv`, make SURE it CORRECT!!\n", "magenta")
                output_textbox.insert("end", f"     2. Increase the `timeout` and/or the `max_itr_num`\n", "magenta")
                output_textbox.insert("end", f"     3. Increase the `num_to_unroll_while_loops`\n", "magenta")
                output_textbox.insert("end", f"     4. Change the input/output examples\n", "magenta")
                output_textbox.insert("end", f"     5. Change the specification\n", "magenta")
                output_textbox.insert("end", f"     6. Check if the `loop_inv` is correct\n", "magenta")
        except Exception as e:
            output_textbox.insert("end", "ERROR:\n", "red")
            if self.debug:
                output_textbox.insert("end", f"{''.join(traceback.format_exception(e))}")
            else:
                output_textbox.insert("end", f"{''.join(traceback.format_exception_only(e))}")
        
        if self.debug:
            print(dedent(output_textbox.get("0.0", "end")))
   
    def debug_btn_event(self, event):
        "print all the info in the `output_frame.output_text` TextBox"
        print("debug_btn_event")
        
        pre_cond, pre_vars = self.conditions_frame.get_pre_condition_and_vars()
        post_cond, post_vars = self.conditions_frame.get_post_condition_and_vars()
        linv, linv_vars = self.conditions_frame.get_loop_inv_and_vars()
        program_to_sketch = self.program_to_sketch.get_program()
        inout_examples_list = self.inout_examples_frame.get_inout_examples()
        
        output_textbox = self.output_frame.get_output_textbox()
        
        info =  f"pre_condition:\n{pre_cond.get('0.0', 'end-1c')}  --types={'{'}{pre_vars.get('0.0', 'end-1c')}{'}'}\n______________\n" 
        info += f"post_condition:\n{post_cond.get('0.0', 'end-1c')}  --types={'{'}{post_vars.get('0.0', 'end-1c')}{'}'}\n______________\n"
        info += f"loop_inv:\n{linv.get('0.0', 'end-1c')}  --types={'{'}{linv_vars.get('0.0', 'end-1c')}{'}'}\n______________\n"
        info += f"program:\n{program_to_sketch.get('0.0', 'end-1c')}\n______________\n"
        info += f"input_output_examples:\n" + "\n-----\n".join( [f"Example {i+1}:\n{e}" for i,e in enumerate(inout_examples_list)] )
        info += f"\n______________\nProgram Output:\n{output_textbox.get('0.0', 'end-1c')}" 
        
        tkinter.messagebox.showinfo("Program Info", f"{info}")

 
            
            
class App(ctk.CTk):
    width = 1450
    height = 900
    
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Simple Sketch")
        self.geometry(f"{self.width}x{self.height}")
        # self.resizable(False, False)
        
        # --------- sidebar frame --------
        self.sidebar_frame = SideBarFrame(master=self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # --------- main frame --------
        self.main_frame = MainFrame(master=self)
        self.main_frame.grid(row=0, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
       
        self.grid_rowconfigure((0,1,2,3), weight=1)
        self.grid_columnconfigure((1,2,3), weight=1)
    




def simple_sketch_gui():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    simple_sketch_gui()



