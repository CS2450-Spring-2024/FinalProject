import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

from PIL import Image, ImageTk
from pathlib import Path
from uvsim.constants import MEM_SIZE

from uvsim.cpu import CPU, ERROR_INVALID_INPUT, OK
from uvsim.gui_memory import Memory
from uvsim.tutorial import Tutorial
from uvsim.parse import parse_word, validate_program

WORKING_DIR = Path(os.path.realpath(__file__)).parent.parent

numeric_regex = re.compile('[+-]?\d*')
is_numeric = lambda text: numeric_regex.fullmatch(text) is not None

FILETYPES = [("Text files", "*.txt"), ("All files", "*.*")]
FONT = None
# FONT = ("Arial", 12)
UVU_GREEN = "#275D38"

class App(CPU, tk.Tk):
    def __init__(self, memory: list[int], screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        tk.Tk.__init__(self, screenName, baseName, className, useTk, sync, use)

        ico = Image.open('uvsim/resources/cpu_green.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(True, photo)

        self.geometry("1000x1000")#  "585x315")
        self.title("UVSim") # Set the window title
        self.configure(bg=UVU_GREEN) # Set the window background color

        self.open_file_path = ""

        self._halted = tk.BooleanVar(value=True)
        self._program_counter = tk.IntVar(value=0)
        self._accumulator = tk.IntVar(value=0)
        self._address_run_to = tk.IntVar(value=0)

        # Menu Bar
        self.menu_bar = tk.Menu(self) # Create a menu bar

        # File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0) # Create a file menu
        self.file_menu.add_command(label="Open", command=self.open_file, font=FONT)
        self.file_menu.add_command(label="Save", command=exit, font=FONT)
        self.file_menu.add_command(label="Save As", command=self.save_as, font=FONT)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Tutorial", command=self.open_tutorial, font=FONT)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_program, font=FONT)
        self.menu_bar.add_cascade(menu=self.file_menu, label="File", font=FONT)


        self.config(menu=self.menu_bar) # Add the menu bar to the window

        self.label = tk.Label(self, text="UVSim", font=(None, 12), bg=UVU_GREEN, fg="white")
        self.label.pack(padx=20, pady=5)

        # master layout frame
        self.master_frame = tk.Frame(self)


        self.master_frame.columnconfigure(0, weight=1)
        self.master_frame.columnconfigure(1, weight=4)
        #________ Left Menu Panel _________
        self.left_menu_frame = tk.Frame(self.master_frame)
        self.left_menu_frame.grid(row=0, column=0, sticky="news", padx=2, pady=2)

        # Left side widgets

        vcmd = (self.register(self.onValidateData), '%P')
        self.accumulator_entry = tk.Entry(self.left_menu_frame, font=FONT, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._accumulator)

        vcmd = (self.register(self.onValidateAddress), '%P')
        self.program_counter_entry = tk.Entry(self.left_menu_frame, font=FONT, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._program_counter)

        vcmd = (self.register(self.onValidateAddress), '%P')
        self.address_run_to_entry = tk.Entry(self.left_menu_frame, font=FONT, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._address_run_to, )

        self.left_side_elems = [
            tk.Label(self.left_menu_frame, font=FONT, justify=tk.CENTER, text="Accumulator"),
            self.accumulator_entry,
            tk.Label(self.left_menu_frame, font=FONT, justify=tk.CENTER, text="Program Counter"),
            self.program_counter_entry,
            ttk.Separator(self.left_menu_frame),
            tk.Button(self.left_menu_frame, font=FONT, command=self.run_until_halt, text="Run"),
            tk.Button(self.left_menu_frame, font=FONT, command=self.run_to_address, text="Run Until Address"),
            self.address_run_to_entry,
            tk.Button(self.left_menu_frame, font=FONT, command=self.step, text="Step"),
            tk.Button(self.left_menu_frame, font=FONT, command=self.reset, text="Reset")
        ]

        for i, element in enumerate(self.left_side_elems):
            element.grid(row=i, column=0, sticky="ew", pady=2)

                    #________ End Left Menu Panel _________


        vcmd = (self.register(self.onValidateData), '%P')
        self.memory = Memory(memory, self.master_frame, vcmd=vcmd)

        def pc_callback(_a, _b, _c):
            try:
                val = int(self.program_counter)
            except:
                pass
            else:
                self.memory.program_counter = val

        def halted_callback(_a, _b, _c):
            self.memory.halted = self.halted

        self._program_counter.trace_add('write', pc_callback)
        self._halted.trace_add('write', halted_callback)

        self.memory.grid(row=0, column=1, sticky="nw", pady=2, padx=2)
        self.master_frame.pack(side="top", fill="both", expand=True) #end of master frame

        self.mainloop()

    def onValidateData(self, proposed_new_text):
        if proposed_new_text in ['', '-', '+']:
            return True

        if is_numeric(proposed_new_text):
            return True

        self.bell()
        return False

    def onValidateAddress(self, proposed_new_text):
        if proposed_new_text in ['', '-', '+']:
            return True

        if not is_numeric(proposed_new_text):
            self.bell()
            return False

        if int(proposed_new_text) < MEM_SIZE and int(proposed_new_text) >= 0:
            return True

        self.bell()
        return False

    def open_tutorial(self):
        self.new_window = tk.Toplevel()
        Tutorial(self.new_window)


    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=FILETYPES, initialdir=WORKING_DIR)

        # Check if a file was selected
        if file_path:
            self.reset()
            self.open_file_path = file_path
            self.title(f"UVSim | {file_path}")
            # Open and read the file, then set the memory to the file content
            with open(file_path, 'r') as file:
                content = []
                for i in file:
                    content.append(i)

                for i in range(len(content)):
                    #validate_program(content)
                    self.memory[i] = int(content[i])

    def exit_program(self): #Kevin
        if messagebox.askyesno(title="Exit Application?", message="Do you really want to exit?"):
            exit()

    def save_as(self): # Kevin
        file_path = filedialog.asksaveasfile(title="Save As", filetypes=FILETYPES, initialdir=WORKING_DIR, defaultextension='.txt')

        if file_path:
            end_idx = False
            mem = [self.memory[i] for i in range(MEM_SIZE)]
            for idx in range(len(mem)-1 ,-1 ,-1):
                if mem[idx] != 0:
                    end_idx= idx
                    break

            try:
                file_path.writelines([f"{str(i)}\n" for i in mem[:end_idx]])
                file_path.write(f"{str(mem[end_idx])}")

            except Exception as error_info:
                messagebox.showerror("Error", f"Error saving file: {error_info}")

    def step(self):
        result = self.run_one_instruction()
        if result != OK:
            text = self.error_code_to_text(result)
            messagebox.showinfo(title="Error", message=text)
        return result

    def run_to_address(self):
        self.halted = False
        address = self._address_run_to.get()
        result = self.step()

        while not self.halted and result == OK and self.program_counter != address:
            result = self.step()

        self.halted = True

    def run_until_halt(self):
        self.halted = False
        result = self.step()

        while not self.halted and result == OK:
            result = self.step()

        self.halted = True

    def read_popup(self):

        user_input = simpledialog.askstring("Input", "Enter a word: ")

        # Check if the user clicked 'Cancel'
        if user_input is not None:
            #print("User input:", user_input)
            return user_input

    def write_popup(self, value):
       messagebox.showinfo(title=f"Output", message=f"Value pulled from memory: {value}")

    def read(self, data, user_input=False):  # Tanner
        if not user_input:  # if user_input is not set, get input from cli.
            user_input = self.read_popup()
        try:
            self.memory[data] = parse_word(user_input, self.program_counter)

        except ValueError:
            # Couldn't parse input
            return ERROR_INVALID_INPUT

        self.program_counter += 1
        return OK

    def write(self, data):  # Tanner
        word_to_write = self.memory[data]

        self.write_popup(word_to_write)  # write to gui
        self.program_counter += 1

        return OK

    @property
    def accumulator(self):
        return self._accumulator.get()

    @accumulator.setter
    def accumulator(self, value):
        self._accumulator.set(value)

    @property
    def program_counter(self):
        return self._program_counter.get()

    @program_counter.setter
    def program_counter(self, value):
        self.memory.program_counter = value
        self._program_counter.set(value)

    @property
    def halted(self):
        return self._halted.get()

    @halted.setter
    def halted(self, value):
        self._halted.set(value)
        self.memory.halted = self.halted
