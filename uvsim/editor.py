import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from tkinter import scrolledtext as scrolledtext
from constants import *
from parse import get_program_from_file, parse_word, save_memory


class Editor:
    def __init__(self, master:tk.Tk, parent: tk.Tk) -> None:
        width = 13 
        self.master = master

        self.master.geometry("350x550")
        self.open_file_path =""

        #initialize Master frame 
        self.master_frame = tk.Frame(self.master)
        self.master_frame.configure(bg=UVU_GREEN)
        self.master_frame.columnconfigure((0, 4), weight=1)
        self.master_frame.rowconfigure(index=0, weight=3)
        self.master_frame.rowconfigure(index=2, weight=1)

        #Create menu bar
        self.menu_bar= tk.Menu(self.master)
        
        #Save, Save as, Open 
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command= self.open_file, font=FONT)
        self.file_menu.add_command(label="Save", command= self.save, font=FONT)
        self.file_menu.add_command(label="Save As", command= self.save_as, font=FONT) 
        self.menu_bar.add_cascade(menu= self.file_menu, label="File", font=FONT)

        self.master.config(menu=self.menu_bar)

        #Upper Frame 
        self.upper_frame = tk.Frame(self.master_frame, bg= UVU_GREEN)
        self.upper_frame.grid(column=0, row=0, sticky="n", padx=3, pady=3)

        #Text Box 
        self.text_box = scrolledtext.ScrolledText(self.upper_frame, undo=True)
        self.text_box['font'] = FONT
        self.text_box['width'] = 30
        self.text_box.grid(row=0, column=0, sticky="n", padx=50, pady=20)

        self.lower_frame = tk.Frame(self.master_frame, bg= UVU_GREEN)
        self.lower_frame.grid(column=0, row=2, sticky="s", padx=3, pady=3)

        self.bttn = tk.Button(self.lower_frame, font=FONT, text="RUN", width=width)

        self.bttn.grid(row=4, column=2, sticky="se", padx=50, pady=20)
        self.master_frame.pack(fill="both", expand=True)

    def run(self):
        pass

    def open_file(self):
        """
        Purpose:
            Opens a file dialog to allow the user to select a file and loads its content into the CPU memory.
        Input Parameters:
            None.
        Return Value:
            None.
        """
        file_path = filedialog.askopenfilename(title="Open", filetypes=FILETYPES, initialdir=WORKING_DIR)

        # Check if a file was selected
        if file_path:
            self.text_box.delete("1.0", tk.END) # Reset text box
            try:
                # Open and read the file, then set the memory to the file content
                program = get_program_from_file(file_path)

                for idx, val in enumerate(program):
                    self.text_box.insert(str(float(idx+1)), f"{str(val)}\n")

            except Exception as error:
                messagebox.showerror("Error", f"Error opening file: {error}")

            else:
                self.open_file_path = file_path
                self.master.title(f"UVSim Editor | {file_path.split('/')[-1]}") 

    def save(self):
        if self.open_file_path:
            output = self.text_box.get(0, tk.END)
            try:
                save_memory(output, self.open_file_path)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file: {error}")
            else:
                self.master.title(f"UVSim Editor | {self.open_file_path.split('/')[-1]}") 
        else:
            self.save_as()


    def save_as(self):
        """
        Purpose:
            Opens a file dialog to allow the user to save the current memory content to a new file.
        Input Parameters:
            None.
        Return Value:
            None.
        """
        file = filedialog.asksaveasfile(title="Save As", filetypes=FILETYPES, initialdir=WORKING_DIR, defaultextension='.txt')

        if file:
            output = self.text_box.get(0, tk.END)
            try:
                save_memory(output, file.name)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file: {error}")
            else:
                self.open_file_path = file.name
                self.title(f"UVSim | {self.open_file_path}")


                

if __name__ == "__main__":
    mast = tk.Tk()
    test = Editor(mast, None)
    mast.mainloop()