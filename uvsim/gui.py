import re
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

from PIL import Image, ImageTk
from uvsim.constants import FILETYPES, FONT, FOURDP_FILETYPES, MEM_SIZE, UVU_GREEN, WORKING_DIR, SECONDARY

from uvsim.cpu import CPU, ERROR_INVALID_INPUT, OK, error_code_to_text
from uvsim.gui_memory import Memory
from uvsim.tutorial import Tutorial
from uvsim.parse import convert_4dp_file_to_6dp, get_program_from_file, parse_word, save_memory, convert_dialog
from uvsim.editor import Editor

numeric_regex = re.compile(r'[+-]?\d*')
is_numeric = lambda text: numeric_regex.fullmatch(text) is not None

exit_program = lambda: exit() if messagebox.askyesno(title="Exit Application?", message="Do you really want to exit?") else None

def onValidateData(proposed_new_text):
    """
    Purpose:
        Validates user input for the accumulator entry to ensure it is a numeric value.
    Input Parameters:
        proposed_new_text: The text proposed by the user.
    Return Value:
        True if the input is valid, False otherwise.
    Pre-conditions:
        User inputs a value
    Post-conditions:
        Value is validated
    """
    if proposed_new_text in ['', '-', '+']:
        return True

    if is_numeric(proposed_new_text):
        return True

    return False

def onValidateAddress(proposed_new_text):
    """
    Purpose:
        Validates user input for the program counter and address entry to ensure it is a numeric value within a valid range.
    Input Parameters:
        proposed_new_text: The text proposed by the user.
    Return Value:
        True if the input is valid, False otherwise.
    Pre-conditions:
        User inputs a value
    Post-conditions:
        Value is validated
    """
    if proposed_new_text in ['', '-', '+']:
        return True

    if not is_numeric(proposed_new_text):
        return False

    if int(proposed_new_text) < MEM_SIZE and int(proposed_new_text) >= 0:
        return True

    return False


class App(CPU, tk.Tk):
    """
    The App class represents the main application that integrates the
    UVSim simulator with a graphical user interface (GUI).
    It extends both the CPU class and the tk.Tk class to manage the
    CPU state and the GUI.
    """

    def __init__(self, memory: list[int], screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        """
        Purpose:
            Initializes the UVSim application with the specified memory and sets up the GUI.
        Input Parameters:
            memory: An array representing the memory of the CPU.
            screenName, baseName, className, useTk, sync, use: Parameters passed to the tk.Tk constructor.
        Return Value:
            None.
        """
        tk.Tk.__init__(self, screenName, baseName, className, useTk, sync, use)

        ico = Image.open('uvsim/resources/cpu_green.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(True, photo)

        self.geometry("900x730")
        self.title("UVSim") # Set the window title
        self.configure(bg=UVU_GREEN) # Set the window background color

        self.open_file_path = ""

        #differentiates between macOS and other systems for key bindings
        current_os = platform.system()
        if current_os == "Darwin":  # macOS
            open_accelerator = "Cmd+O"
            exit_accelerator = "Cmd+Q"
        else:  # Other systems (e.g., Windows, Linux)
            open_accelerator = "Ctrl+O"
            exit_accelerator = "Ctrl+Q"

        self._halted = tk.BooleanVar(value=True)
        self._program_counter = tk.IntVar(value=0)
        self._accumulator = tk.IntVar(value=0)
        self._address_run_to = tk.IntVar(value=0)

        # Menu Bar
        self.menu_bar = tk.Menu(self) # Create a menu bar

        # File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0) # Create a file menu
        self.file_menu.add_command(label="Exit", command=exit_program, font=FONT, accelerator=exit_accelerator)
        self.bind_all("<Control-q>" if current_os != "Darwin" else "<Command-q>", lambda event: exit_program())
        self.file_menu.add_command(label="Open Editor", command=lambda: self.editors.append(Editor(tk.Toplevel(), self)), font=FONT, accelerator=open_accelerator)
        self.bind_all("<Control-o>" if current_os != "Darwin" else "<Command-o>", lambda event: self.editors.append(Editor(tk.Toplevel(), self)))
        self.menu_bar.add_cascade(menu=self.file_menu, label="File", font=FONT)

        #Edit
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0) # TODO: define and change event_generate to the correct event

        self.edit_menu.add_command(label="Change Color", command=self.change_color, font=FONT)
        self.menu_bar.add_cascade(menu=self.edit_menu, label="Edit", font=FONT)


        # help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Tutorial", command=lambda: Tutorial(tk.Toplevel()), font=FONT)
        self.help_menu.add_command(label="Migrate 4dp Program to 6dp", command=lambda: convert_dialog(), font=FONT)
        self.menu_bar.add_cascade(menu=self.help_menu, label="Help", font=FONT)

        self.config(menu=self.menu_bar) # Add the menu bar to the window

        self.label = tk.Label(self, text="UVSim", font=(None, 12), bg="black", fg="white")
        self.label.pack(padx=20, pady=5)

        # master layout frame
        self.master_frame = tk.Frame(self, bg=SECONDARY)

        self.master_frame.columnconfigure(0, weight=1)
        self.master_frame.columnconfigure(1, weight=4)

        #________ Left Menu Panel _________
        self.left_menu_frame = tk.Frame(self.master_frame, bg= SECONDARY)
        self.left_menu_frame.grid(row=0, column=0, sticky="news", padx=2, pady=2)

        # Left side widgets

        vcmd = (self.register(onValidateData), '%P')
        self.accumulator_entry = tk.Entry(self.left_menu_frame, font=FONT, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._accumulator)

        vcmd = (self.register(onValidateAddress), '%P')
        self.program_counter_entry = tk.Entry(self.left_menu_frame, font=FONT, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._program_counter)

        vcmd = (self.register(onValidateAddress), '%P')
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

        vcmd = (self.register(onValidateData), '%P')
        self.memory = Memory(memory, self.master_frame, vcmd=vcmd)


        #Editors
        self.main_editor = Editor(tk.Toplevel(), self, is_main=True)
        self.editors = [self.main_editor]

        def pc_callback(_a, _b, _c):
            """
            Purpose:
                Callback function for the program counter entry. Updates the program counter value in memory.
            Input Parameters:
                _a, _b, _c: Unused parameters.
            Return Value:
                None.
            Pre-conditions:
                User inputs a value in the program counter entry.
            Post-conditions:
                Program counter value is updated in memory.
            """
            try:
                val = int(self.program_counter)
            except:
                pass
            else:
                self.memory.program_counter = val

        def halted_callback(_a, _b, _c):
            """
            Purpose:
                Callback function for the halted variable. Updates the halted state in memory.
            Input Parameters:
                _a, _b, _c: Unused parameters.
            Return Value:
                None.
            Pre-conditions:
                Halted state changes.
            Post-conditions:
                Halted state is updated in memory.
            """
            self.memory.halted = self.halted

        self._program_counter.trace_add('write', pc_callback)
        self._halted.trace_add('write', halted_callback)
        self._file_path = None

        self.memory.grid(row=0, column=1, sticky="nw", pady=2, padx=2)
        self.master_frame.pack(side="top", fill="both", expand=True) #end of master frame

        self.mainloop()

    def change_color(self):
        """
        Purpose:
            Changes the color of the GUI.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            Change color button is clicked from the menu.
        Post-conditions:
            The color of the GUI is changed.
        """
        top = tk.Toplevel()
        top.geometry('300x300')
        
        
        primary_ent = tk.Entry(top)
        secondary_ent =tk.Entry(top)
        #Goes through everything and sets their bg and forground
    

        def insert_val():


            primary= primary_ent.get()
            secondary = secondary_ent.get()


            if primary and secondary:
                if primary[0] != '#':
                    primary = f'#{primary}'
                if secondary[0] != "#":
                    secondary = f'#{secondary}'
                
                self.config(bg=primary)
                self.label.config(bg=primary)
                self.master_frame.config(bg=secondary)
                self.left_menu_frame.config(bg=secondary)

                for i in self.left_side_elems:
                    if isinstance(i,(tk.Label, tk.Button)):
                        i.config(bg=primary, fg=secondary)

                for i in self.editors:
                    i.master_frame.config(bg=primary)
                    i.upper_frame.config(bg=primary)
                    i.lower_frame.config(bg=primary)

                top.destroy()
            else:
                messagebox.showerror("ERROR", f"Please input color for all fields")
        items = [
        tk.Label(top,text="Enter Primary Color Hex code or Key word 'red' etc :"),
        primary_ent,
        tk.Label(top,text="Enter Secondary Hex code or Key word 'red' etc:"),
        secondary_ent,
        tk.Button(top, command=insert_val, text="Click to Submit")
        ]
        for i in items:
            i.pack()

    def open(self):
        """
        Purpose:
            Opens a file dialog to allow the user to select a file and loads its content into the CPU memory.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            Needs to be selected from the menu.
        Post-conditions:
            The memory content is set to the content of the selected file.
        """
        file_path = filedialog.askopenfilename(title="Open", filetypes=FILETYPES, initialdir=WORKING_DIR)

        # Check if a file was selected
        if file_path:
            self.reset()

            try:
                # Open and read the file, then set the memory to the file content
                program = get_program_from_file(file_path)

                for i, val in enumerate(program):
                    self.memory[i] = val

            except Exception as error:
                messagebox.showerror("Error", f"Error opening file: {error}")

            else:
                self.open_file_path = file_path
                self.title(f"UVSim | {file_path}")

    def save(self):
        """
        Purpose:
            Saves the current memory content to the previously opened or saved file path.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The memory content must be valid.
        Post-conditions:
            The memory content is saved to the previously opened or saved file path.
        """
        if self.open_file_path:
            mem = [self.memory[i] for i in range(MEM_SIZE)]
            try:
                save_memory(mem, self.open_file_path)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file: {error}")
            else:
                self.title(f"UVSim | {self.open_file_path}")
        else:
            self.save_as()

    def save_as(self): # Kevin
        """
        Purpose:
            Opens a file dialog to allow the user to save the current memory content to a new file.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The memory content must be valid.
        Post-conditions:
            The memory content is saved to a new file.
        """
        file = filedialog.asksaveasfile(title="Save As", filetypes=FILETYPES, initialdir=WORKING_DIR, defaultextension='.txt')

        if file:
            mem = [self.memory[i] for i in range(MEM_SIZE)]
            try:
                save_memory(mem, file.name)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file: {error}")
            else:
                self.open_file_path = file.name
                self.title(f"UVSim | {self.open_file_path}")

    def step(self):
        """
        Purpose:
            Executes a single instruction and displays an error message if applicable.
        Input Parameters:
            None.
        Return Value:
            The result of the instruction execution.
        Pre-conditions:
            The CPU is not halted.
        Post-conditions:
            The CPU executes a single instruction.
        """
        result = self.run_one_instruction()
        if result != OK:
            text = error_code_to_text(result, self.program_counter)
            messagebox.showinfo(title="Error", message=text)
        return result

    def run_to_address(self):
        """
        Purpose:
            Executes instructions until the program counter reaches the specified address and displays an error message if applicable.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The CPU is not halted.
        Post-conditions:
            The CPU executes instructions until the program counter reaches the specified address.
        """
        self.halted = False
        address = self._address_run_to.get()
        result = self.step()

        while not self.halted and result == OK and self.program_counter != address:
            result = self.step()

        self.halted = True

    def run_until_halt(self):
        """
        Purpose:
            Executes instructions until the CPU is halted and displays an error message if applicable.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The CPU is not halted.
        Post-conditions:
            The CPU executes instructions until it is halted.
        """
        self.halted = False
        result = self.step()

        while not self.halted and result == OK:
            result = self.step()

        self.halted = True

    def read(self, data, user_input=False):  # Tanner
        """
        Purpose:
            Reads input from the user using a dialog box and stores it in memory.
        Input Parameters:
            data: The memory location where the input will be stored.
            user_input: User-provided input. If not provided, input is obtained through a popup.
        Return Value:
            An error code indicating the result of the operation.
        Pre-conditions:
            None.
        Post-conditions:
            Memory is updated with the user input.
        """
        if not user_input: # if user_input is not set, get input from cli.
            user_input = simpledialog.askstring("Read", "Enter a word: ")

        if not user_input:
            return ERROR_INVALID_INPUT

        try:
            self.memory[data] = parse_word(user_input, self.program_counter)
        except ValueError: # Couldn't parse input
            return ERROR_INVALID_INPUT

        self.program_counter += 1
        return OK

    def write(self, data):  # Tanner
        """
        Purpose:
            Writes a word from memory to a popup.
        Input Parameters:
            data: The memory location of the word that will be written.
        Return Value:
            An error code indicating the result of the operation.
        Pre-conditions:
            None.
        Post-conditions:
            The word is displayed in a popup.
        """
        word_to_write = self.memory[data]

        messagebox.showinfo(title=f"Write", message=f"Value from memory: {word_to_write}")

        self.program_counter += 1
        return OK

    @property
    def accumulator(self):
        """
        Purpose:
            Getter and setter for the accumulator property.
        Input Parameters:
            None.
        Return Value:
            The current value of the accumulator.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        """
        return self._accumulator.get()

    @accumulator.setter
    def accumulator(self, value):
        """
        Purpose:
            Setter for the accumulator property.
        Input Parameters:
            value: The new value of the accumulator.
        Return Value:
            None.
        Pre-conditions:
            None.
        Post-conditions:
            The accumulator value is updated.
        """
        self._accumulator.set(value)

    @property
    def program_counter(self):
        """
        Purpose:
            Getter and setter for the program counter property.
        Input Parameters:
            None.
        Return Value:
            The current value of the program counter.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        """
        return self._program_counter.get()

    @program_counter.setter
    def program_counter(self, value):
        """
        Purpose:
            Setter for the program counter property.
        Input Parameters:
            value: The new value of the program counter.
        Return Value:
            None.
        Pre-conditions:
            None.
        """
        self.memory.program_counter = value
        self._program_counter.set(value)

    @property
    def halted(self):
        """
        Purpose:
            Getter and setter for the halted property.
        Input Parameters:
            None.
        Return Value:
            True if the CPU is halted, False otherwise.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        """
        return self._halted.get()

    @halted.setter
    def halted(self, value):
        """
        Purpose:
            Setter for the halted property.
        Input Parameters:
            value: The new value of the halted property.
        Return Value:
            None.
        Pre-conditions:
            None.
        Post-conditions:
            The halted property is updated.
        """
        self._halted.set(value)
        self.memory.halted = self.halted
