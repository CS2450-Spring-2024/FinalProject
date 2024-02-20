import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from uvsim.cpu import CPU, OK
from uvsim.gui_memory import Memory

numeric_regex = re.compile('[+-]?\d*')
is_numeric = lambda text: numeric_regex.fullmatch(text) is not None

FONT = None
# FONT = ("Arial", 12)P

class App(CPU, tk.Tk):
    def __init__(self, memory: list[int], screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        tk.Tk.__init__(self, screenName, baseName, className, useTk, sync, use)

        self.geometry("1000x1000")
        self.title("UVSim") # Set the window title
        self.configure(bg="light blue") # Set the window background color

        # Menu Bar
        self.menu_bar = tk.Menu(self) # Create a menu bar

        # File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0) # Create a file menu
        self.file_menu.add_command(label="Open", command=self.open_file, font=FONT) # Add an open file option ## TODO implement the open function.
        self.file_menu.add_command(label="Save", command=exit, font=FONT) # Add an open file option ## TODO implement the Save AS function.
        self.file_menu.add_command(label="Save As", command=self.save_as, font=FONT) # Add an open file option ## TODO implement the Save AS function.
        self.file_menu.add_separator()  
        self.file_menu.add_command(label="Exit", command=self.exit_program, font=FONT) # Add an open file option ## TODO implement the Save AS function.
        self.menu_bar.add_cascade(menu=self.file_menu, label="File", font=FONT)


        self.config(menu=self.menu_bar) # Add the menu bar to the window

        self.label = tk.Label(self,  text="UVSim", font=FONT)
        self.label.pack(padx=20, pady=5)

        # master layout frame
        self.master_frame = tk.Frame(self)#, bg="blue")


        self.master_frame.columnconfigure(0, weight=1) # Set the column weight to 1
        self.master_frame.columnconfigure(1, weight=1) # Set the column weight to 1
        # self.master_frame.rowconfigure(0, weight=1)
        # self.master_frame.rowconfigure(1, weight=1)


        #________ Left Menu Panel _________
        self.left_menu_frame = tk.Frame(self.master_frame, bg="green")
        self.left_menu_frame.grid(row=0, column=0, sticky="nw", padx=3, pady=3)

        # Left side widgets
        width = 15

        self._program_counter = tk.IntVar(value=0)
        self._accumulator = tk.IntVar(value=0)

        vcmd = (self.register(self.onValidateData), '%P')
        self.accumulator_entry = tk.Entry(self.left_menu_frame, font=FONT, width=width, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._accumulator)

        vcmd = (self.register(self.onValidateProgramCounter), '%P')
        self.program_counter_entry = tk.Entry(self.left_menu_frame, font=FONT, width=width, justify=tk.CENTER, validate='key', validatecommand=vcmd, textvariable=self._program_counter)

        self.left_side_elems = [
            tk.Label(self.left_menu_frame, font=FONT, width=width, justify=tk.CENTER, text="Accumulator"),
            self.accumulator_entry,
            tk.Label(self.left_menu_frame, font=FONT, width=width, justify=tk.CENTER, text="Program Counter"),
            self.program_counter_entry,
            ttk.Separator(self.left_menu_frame),
            tk.Button(self.left_menu_frame, font=FONT, width=width, command=exit, text="Run"),
            tk.Button(self.left_menu_frame, font=FONT, width=width, command=exit, text="Run Until Address"),
            tk.Button(self.left_menu_frame, font=FONT, width=width, command=self.step, text="Step"),
            tk.Button(self.left_menu_frame, font=FONT, width=width, command=exit, text="Halt"),
            tk.Button(self.left_menu_frame, font=FONT, width=width, command=self.reset_gui, text="Reset")
        ]

        for i, element in enumerate(self.left_side_elems):
            element.grid(row=i, column=0, sticky="ew", pady=2)

                    #________ End Left Menu Panel _________

                    #________ Bottom Frame Start ________

        # self.memory = tk.Frame(self.master_frame, bg="blue")
        # self.memory.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


        # self.output_text = tk.Text(self.master_frame, wrap="word")
        # self.output_text.grid(row=0, column=1, sticky="nsew", pady=2)

                    #________ Bottom Frame End ________
        vcmd = (self.register(self.onValidateData), '%P')
        self.memory = Memory(memory, self.master_frame, vcmd=vcmd)
        self.memory.grid(row=0, column=1, sticky="nsew", pady=2)
        self.master_frame.pack(side="top", fill="both", expand=True) #end of master frame

        self.mainloop()

    def onValidateData(self, proposed_new_text):
        if proposed_new_text in ['', '-', '+']:
            return True

        if is_numeric(proposed_new_text):
            return True

        self.bell()
        return False

    def onValidateProgramCounter(self, proposed_new_text):
        if proposed_new_text in ['', '-', '+']:
            return True

        if not is_numeric(proposed_new_text):
            self.bell()
            return False

        if int(proposed_new_text) < 100 and int(proposed_new_text) >= 0:
            return True

        self.bell()
        return False

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        # Check if a file was selected
        if file_path:
            # Open and read the file, then set the memory to the file content
            with open(file_path, 'r') as file:
                content = []
                for i in file:
                    content.append(i)

                for i in range(len(content)):
                    self.memory.__setitem__(i, int(content[i]))

    def reset_gui(self): #Kevin
        for idx, ele in enumerate([0]*100):
            self.memory.__setitem__(idx, ele)

        self.reset()


    def exit_program(self): #Kevin
        if messagebox.askyesno(title="Exit Application?", message="Do you really want to exit?"):
            exit()

    def save_as(self): # Kevin
        files =[("All Files", "*.*"),
                ("Text Document","*.txt")]
        filepath = filedialog.asksaveasfile(filetypes=files, defaultextension='.txt')
        
        try:
            end_idx = False
            mem = [self.memory.__getitem__(i) for i in range(100)]
            for idx in range(len(mem)-1 ,-1 ,-1):
                print(len(mem),idx)
                if mem[idx] != 0:
                    end_idx= idx
                    break
            filepath.writelines([f"{str(i)}\n" for i in mem[:end_idx]])
            filepath.write(f"{str(mem[end_idx])}")
            messagebox.showinfo(":)","Succesfully Saved!")
        
        except Exception as error_info:
            messagebox.showerror("Uh Oh", f"Error: {error_info}")


    def step(self):
        result = self.run_one_instruction()

        if result != OK:
            text = self.error_code_to_text(result)
            messagebox.showinfo(title="Error", message=text)

    @property
    def program_counter(self):
        return self._program_counter.get()

    @program_counter.setter
    def program_counter(self, value):
        self._program_counter.set(value)

    @property
    def accumulator(self):
        return self._accumulator.get()

    @accumulator.setter
    def accumulator(self, value):
        self._accumulator.set(value)
