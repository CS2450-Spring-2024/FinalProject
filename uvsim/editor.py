import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from tkinter import scrolledtext as scrolledtext
from uvsim.constants import *
from uvsim.parse import get_program_from_file, parse_word, save_memory
import platform


class Editor:
    """
    Editor Class
    Purpose of the Class:
        The Editor class is used to create a GUI for the UVSim Editor. In the editor the user can write and edit programs. 
        The editor also allows the user to save and open files.
    """
    def __init__(self, master:tk.Tk, parent: tk.Tk, is_main:bool=False) -> None:
        width = 13 
        self.master = master
        self.parent = parent

        #self.master.wm_attributes("-toolwindow", 't')  

        self.master.geometry("350x450")
        self.open_file_path =""
        
        
        #differentiates between macOS and other systems for key bindings
        current_os = platform.system()
        if current_os == "Darwin":  # macOS
            save_accelerator = "Cmd+S"
            save_as_accelerator = "Cmd+Shift+S"
            open_accelerator = "Cmd+O"
            exit_accelerator = "Cmd+Q"
            undo_accelerator = "Cmd+Z"
            redo_accelerator = "Cmd+Shift+Z"
            cut_accelerator = "Cmd+X"
            copy_accelerator = "Cmd+C"
            paste_accelerator = "Cmd+V"
        else:  # Other systems (e.g., Windows, Linux)
            save_accelerator = "Ctrl+S"
            save_as_accelerator = "Ctrl+Shift+S"
            open_accelerator = "Ctrl+O"
            exit_accelerator = "Ctrl+Q"
            undo_accelerator = "Ctrl+Z"
            redo_accelerator = "Ctrl+Y"
            cut_accelerator = "Ctrl+X"
            copy_accelerator = "Ctrl+C"
            paste_accelerator = "Ctrl+V"

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
        
        
        #edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=lambda: self.cut(), font=FONT, accelerator=cut_accelerator)
        self.master.bind_all("<Control-x>" if current_os != "Darwin" else "<Command-x>", lambda event: self.cut())
        self.edit_menu.add_command(label="Copy", command=lambda: self.copy(), font=FONT, accelerator=copy_accelerator)
        self.master.bind_all("<Control-c>" if current_os != "Darwin" else "<Command-c>", lambda event: self.copy())
        self.edit_menu.add_command(label="Paste", command=lambda: self.paste(), font=FONT, accelerator=paste_accelerator)
        self.master.bind_all("<Control-v>" if current_os != "Darwin" else "<Command-v>",  lambda event: self.paste)
        self.edit_menu.add_separator()
        self.menu_bar.add_cascade(menu= self.edit_menu, label="Edit", font=FONT)

        self.master.config(menu=self.menu_bar)

        #Upper Frame 
        self.upper_frame = tk.Frame(self.master_frame, bg= UVU_GREEN)
        self.upper_frame.grid(column=0, row=0, sticky="n", padx=3, pady=3)

        #Text Box 
        self.text_box = scrolledtext.ScrolledText(self.upper_frame, undo=True)
        self.text_box['font'] = FONT
        self.text_box['width'] = 30
        self.text_box.grid(row=0, column=0, sticky="n", padx=50, pady=30)

        #Label 
        self.label = tk.Label(self.upper_frame, text="UVSIM | EDITOR")
        self.label.grid(row=0, column=0, sticky="n")

        self.lower_frame = tk.Frame(self.master_frame, bg= UVU_GREEN)
        self.lower_frame.grid(column=0, row=2, sticky="s", padx=3, pady=3)

        self.bttn = tk.Button(self.lower_frame, command=self.run , text="Load to CPU", width=width, font=FONT)
        self.bttn.grid(row=4, column=2, sticky="se", padx=50, pady=20)
        self.master_frame.pack(fill="both", expand=True)

    def run(self):
        """
        Purpose:
            Loads the content of the text box into the CPU memory.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            Text box must have content.
        Post-conditions:
            The CPU memory is set to the content of the text box.
        """
        self.parent.reset()
        self.program = [i for i in self.text_box.get("1.0", "251.0").split('\n') if i != ""]
        for idx, val in enumerate(self.program):
            self.parent.memory[idx] = val

    def open_file(self):
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
            self.text_box.delete("1.0", tk.END) # Reset text box
            try:
                # Open and read the file, then set the memory to the file content
                program = get_program_from_file(file_path)

                for idx, val in enumerate(program):
                    self.text_box.insert(str(float(idx+1)), f"{str(val)}\n")

            except Exception as error:
                messagebox.showerror("Error", f"Error opening file:\n{error}")

            else:
                self.open_file_path = file_path
                self.master.title(f"UVSim Editor | {file_path.split('/')[-1]}") 

    def save(self):
        """
        Purpose:
            Opens a file dialog to allow the user to save the current memory content to an existing file.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            The memory content must be valid.
        Post-conditions:
            The memory content is saved to an existing file.
        """
        if self.open_file_path:
            output = [int(i) for i in self.text_box.get("1.0", tk.END).split("\n") if i != ""]
            try:
                save_memory(output, self.open_file_path)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file:\n{error}")
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
        Pre-conditions:
            The memory content must be valid.
        Post-conditions:
            The memory content is saved to a new file.
        """
        file = filedialog.asksaveasfile(title="Save As", filetypes=FILETYPES, initialdir=WORKING_DIR, defaultextension='.txt')

        if file:
            output = [int(i) for i in self.text_box.get("1.0", tk.END).split("\n") if i != "" and i != "\n"]
            try:
                save_memory(output, file.name)
            except Exception as error:
                messagebox.showerror("Error", f"Error saving file:\n{error}")
            else:
                self.open_file_path = file.name
                self.master.title(f"UVSim Editor | {self.open_file_path.split('/')[-1]}")

    def copy(self):
        """
        Purpose:
            Add the copy event to the text box.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            the text box must exist. there must be text in the text box.
        Post-conditions:
            the text in the text box is copied to the clipboard.
        """
        self.text_box.event_generate("<<Copy>>")

    def cut(self):
        """
        Purpose:
            Add the cut event to the text box.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            the text box must exist. there must be text in the text box.
        Post-conditions:
            the text in the text box is cut to the clipboard. The text is removed from the text box.
        """
        self.text_box.event_generate("<<Cut>>")

    def paste(self, event=None):
        """
        Purpose:
            Add the paste event to the text box.
        Input Parameters:
            None.
        Return Value:
            None.
        Pre-conditions:
            the clipboard must have text in it.
        Post-conditions:
            the text in the clipboard is pasted into the text box.
        """
        self.text_box.event_generate("<<Paste>>")
        return "break"
        





if __name__ == "__main__":
    mast = tk.Tk()
    test = Editor(mast, None)
    mast.mainloop()
    
    


