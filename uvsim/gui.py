import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from uvsim.cpu import CPU

numeric_regex = re.compile('\d+')
is_numeric = lambda text: numeric_regex.fullmatch(text) is not None

FONT = None

class App(tk.Tk):
    def __init__(self, cpu: CPU, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.cpu = cpu

        self.geometry("1000x1000")
        self.title("UVSim") # Set the window title
        self.configure(bg="light blue") # Set the window background color

        self.menu_bar = tk.Menu(self) # Create a menu bar

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0) # Create a file menu
        self.file_menu.add_command(label="Open", command=self.open_file) # Add an open file option ## TODO implement the open function.
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=exit) # Add an open file option ## TODO implement the Save AS function.
        self.file_menu.add_command(label="Save As", command=exit) # Add an open file option ## TODO implement the Save AS function.
        self.file_menu.add_command(label="Exit", command=exit) # Add an open file option ## TODO implement the Save AS function.

        self.menu_bar.add_cascade(menu=self.file_menu, label="File")

        self.config(menu=self.menu_bar) # Add the menu bar to the window

        self.label = tk.Label(self, text="UVSim", font=FONT)
        self.label.pack(padx=20, pady=20)

        # master layout frame
        self.master_frame = tk.Frame(self)#, bg="blue")


        self.master_frame.columnconfigure(0, weight=0) # Set the column weight to 1
        self.master_frame.columnconfigure(1, weight=1) # Set the column weight to 1
        self.master_frame.rowconfigure(0, weight=1)
        self.master_frame.rowconfigure(1, weight=1)


        #________ Left Menu Panel _________
        self.menu_frame = tk.Frame(self.master_frame)#, bg="light green")
        self.menu_frame.grid(row=0, rowspan=1, column=0, sticky="new", padx=3, pady=3)

        # Left side widgets
        width = 15

        vcmd = (self.register(self.onValidateAccumulator), '%P')
        self.accumulator = tk.Entry(self.menu_frame, font=FONT, width=width, justify=tk.CENTER, validate=tk.ALL, validatecommand=vcmd, name="acc")

        vcmd = (self.register(self.onValidateProgramCounter), '%P')
        self.program_counter = tk.Entry(self.menu_frame, font=FONT, width=width, justify=tk.CENTER, validate=tk.ALL, validatecommand=vcmd, name="pc")

        self.left_side_elems = [
            tk.Label(self.menu_frame, font=FONT, width=width, justify=tk.CENTER, text="Accumulator"),
            self.accumulator,
            tk.Label(self.menu_frame, font=FONT, width=width, justify=tk.CENTER, text="Program Counter"),
            self.program_counter,
            ttk.Separator(self.menu_frame),
            tk.Button(self.menu_frame, font=FONT, width=width, command=exit, text="Run"),
            tk.Button(self.menu_frame, font=FONT, width=width, command=exit, text="Run Until Address"),
            tk.Button(self.menu_frame, font=FONT, width=width, command=exit, text="Step"),
            tk.Button(self.menu_frame, font=FONT, width=width, command=exit, text="Halt"),
            tk.Button(self.menu_frame, font=FONT, width=width, command=exit, text="Reset")
        ]

        for i, element in enumerate(self.left_side_elems):
            element.grid(row=i, column=0, sticky="ew", pady=2)

        #________ End Left Menu Panel _________

        #________ Top Frame Start ________
        self.top_frame = tk.Frame(self.master_frame, bg="green")
        for i in range(3):
            self.top_frame.columnconfigure(i, weight=1)

        self.top_frame.rowconfigure(0, weight=1)

                    #________ Top Left Frame Start ________
        self.open_section = tk.Frame(self.top_frame, bg="red")
        self.label_top_left = tk.Label(self.open_section, text="Updates Submission", font=FONT)
        self.label_top_left.pack()
        self.submit_button = tk.Button(self.open_section, text="Submit Change", font=FONT) # Create a button widget
        self.submit_button.pack(padx=5, pady=5)
        self.open_section.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)


                    #________ Top Middle Frame Start ________

        self.console_section = tk.Frame(self.top_frame, bg="purple")
        self.label_top_mid = tk.Label(self.console_section, text="Console Output", font=FONT)
        self.label_top_mid.pack()
        self.run_in_entry = tk.Entry(self.console_section, font=FONT)
        self.run_in_entry.pack(padx=10, pady=5)

        # Create a Button for submitting the text
        sub_read_button = tk.Button(self.console_section, text="Submit", command=self.submit_text)
        sub_read_button.pack(padx=10, pady=5)
        # self.run_until_address.grid(row=1, column=0, sticky="news") # Place the button in the frame
        self.console_section.grid(row=0, column=1, columnspan=1, sticky="nsew", padx=5, pady=5)

        self.write_text = tk.Entry(self.console_section, state=tk.DISABLED)
        self.write_text.pack(padx=10, pady=10)


                    #________ Top Right Frame Start ________
        self.accum_section = tk.Frame(self.top_frame, bg="orange")
        self.label_top_right = tk.Label(self.accum_section, text="Accumulator", font=FONT)
        self.label_top_right.pack()
        self.accum_text = tk.Entry(self.accum_section, state=tk.DISABLED)
        self.accum_text.pack(padx=10, pady=10)
        self.accum_section.grid(row=0, column=2, columnspan=1, sticky="nsew", padx=5, pady=5)


        self.top_frame.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)
        #________ Top Frame End ________

        #________ Bottom Frame Start ________
        self.bottom_frame = tk.Frame(self.master_frame, bg="yellow")
        self.bottom_frame.grid(row=1, rowspan=1, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.output_text = tk.Text(self.bottom_frame, wrap="word")
        self.output_text.pack(padx=10, pady=10)

        #________ Bottom Frame End ________

        self.master_frame.pack(side="top", fill="both", expand=True) #end of master frame


        self.mainloop()

    def onValidateProgramCounter(self, proposed_new_text):
        if proposed_new_text == '':
            return True

        if not is_numeric(proposed_new_text):
            self.bell()
            return False

        if int(proposed_new_text) < 100 and int(proposed_new_text) >= 0:
            return True

        self.bell()
        return False

    def onValidateAccumulator(self, proposed_new_text):
        if proposed_new_text == '':
            return True

        if is_numeric(proposed_new_text):
            return True

        self.bell()
        return False

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get("1.0", "end-1c"))

        else:
            messagebox.showinfo(title="Message", message=self.textbox.get("1.0", "end-1c"))


    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        # Check if a file was selected
        if file_path:
            # Open and read the file
            with open(file_path, 'r') as file:
                content = file.read()

            self.output_text.delete("1.0", tk.END)

            # Insert the file content into the Text widget
            self.output_text.insert(tk.END, content)

    def submit_text(self):
        # Get the text from the Entry widget
        input_text = self.run_in_entry.get()

        # Clear existing content in the Text widget
        self.output_text.delete("1.0", tk.END)

        # Display the submitted text in the Text widget
        self.output_text.insert(tk.END, "Submitted Text: " + input_text)

    def accumulator_output(self):
                # Enable the Text widget to insert content from the CPU
                #
        message = "Accumulator: " + str(self.accumulator) + "\n" # not real message, just a placeholder


        self.output_text.config(state=tk.NORMAL)

        # Clear existing content in the Text widget
        self.output_text.delete("1.0", tk.END)

        # Display the message in the Text widget
        self.output_text.insert(tk.END, message)

        # Disable the Text widget to make it non-editable again
        self.output_text.config(state=tk.DISABLED)
