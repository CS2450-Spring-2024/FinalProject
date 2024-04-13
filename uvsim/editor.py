import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from tkinter import scrolledtext as scrolledtext
from uvsim.constants import *
from uvsim.parse import get_program_from_file, parse_word, save_memory
import platform


class Editor:
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
        #self.edit_menu.add_command(label="Undo", command=lambda: self.memory.undo(), font=FONT, accelerator=undo_accelerator)
        # self.bind_all("<Control-z>" if current_os != "Darwin" else "<Command-z>", lambda event: self.memory.undo())
        # self.edit_menu.add_command(label="Redo", command=lambda: self.memory.redo(), font=FONT, accelerator=redo_accelerator)
        # self.bind_all("<Control-y>" if current_os != "Darwin" else "<Command-Shift-Z>", lambda event: self.memory.redo())
        # self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.cut(), font=FONT, accelerator=cut_accelerator)
        self.master.bind_all("<Control-x>" if current_os != "Darwin" else "<Command-x>", lambda event: self.cut())
        self.edit_menu.add_command(label="Copy", command=lambda: self.copy(), font=FONT, accelerator=copy_accelerator)
        self.master.bind_all("<Control-c>" if current_os != "Darwin" else "<Command-c>", lambda event: self.copy())
        self.edit_menu.add_command(label="Paste", command=lambda: self.paste(), font=FONT, accelerator=paste_accelerator)
        self.master.bind_all("<Control-v>" if current_os != "Darwin" else "<Command-v>", lambda event: self.paste())
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
        self.text_box.event_generate("<<Copy>>")

    def cut(self):
        self.text_box.event_generate("<<Cut>>")

    def paste(self):
        self.text_box.event_generate("<<Paste>>")





if __name__ == "__main__":
    mast = tk.Tk()
    test = Editor(mast, None)
    mast.mainloop()
    
    
    
    
# CODE GRAVEYARD

'''    def handle_click(self, event):
        x = event.x_root - self.memory_frames[0].winfo_rootx()
        y = event.y_root - self.memory_frames[0].winfo_rooty()
        frame_index = self.get_frame_index(x, y)
        if frame_index is not None:
            if frame_index in self.selected_frames:
                self.selected_frames.remove(frame_index)
                self.memory_frames[frame_index].configure(bg=self.defaultbg)
            else:
                for i in self.selected_frames:
                    self.memory_frames[i].configure(bg=self.defaultbg)
                self.selected_frames.clear()
                self.selected_frames.add(frame_index)
                self.memory_frames[frame_index].configure(bg="blue")'''

'''    def get_frame_index(self, x, y):
        col = x // self.memory_frames[0].winfo_width()
        row = y // self.memory_frames[0].winfo_height()
        if 0 <= row < ROW_WIDTH and 0 <= col < COLS:
            return row * ROW_WIDTH + col
        else:
            return None

    def deselect_frames(self):
        for index in self.selected_frames:
            self.memory_frames[index].configure(bg=self.defaultbg)
        self.selected_frames.clear()'''


'''    def handle_drag(self, event):
        x = event.x_root - self.memory_frames[0].winfo_rootx()
        y = event.y_root - self.memory_frames[0].winfo_rooty()
        frame_index = self.get_frame_index(x, y)
        if frame_index is not None:
            if frame_index not in self.selected_frames:
                self.selected_frames.add(frame_index)
                self.memory_frames[frame_index].configure(bg="blue")'''



"""def cut(self):
        '''        if self.selected_frames:
            self.clipboard = [self.memory_vars[i].get() for i in self.selected_frames]
            for i in self.selected_frames:
                self.memory_vars[i].set(0)
            self.deselect_frames()'''
            
        print("this runs")

    def copy(self):
        if self.selected_frames:
            self.clipboard = [self.memory_vars[i].get() for i in self.selected_frames]
            self.deselect_frames()

    def paste(self):
        if not self.clipboard:
            messagebox.showinfo("Info", "Clipboard is empty.")
            return
        if not self.selected_frames:
            messagebox.showinfo("Info", "No selected fields to paste into.")
            return

        sorted_selected_frames = sorted(self.selected_frames)
        start_index = sorted_selected_frames[0]
        shift_amount = len(self.clipboard) - len(sorted_selected_frames)

        if shift_amount > 0:
            for i in range(WORD_SIZE - 1, start_index + len(sorted_selected_frames) - 1, -1):
                if (i - shift_amount) < 0:

                    messagebox.showerror("Error", "Not enough space to paste.")
                    return
                self.memory_vars[i].set(self.memory_vars[i - shift_amount].get())

        for i, value in enumerate(self.clipboard):
            if start_index + i >= WORD_SIZE:
                messagebox.showwarning("Warning", "Reached end of memory. Cannot paste further.")
                break
            self.memory_vars[start_index + i].set(value)"""


''' def shift_memory(self, start_index):
        """
        Shifts memory contents starting from start_index to the right to make space.
        """
        for i in range(WORD_SIZE - 2, start_index - 1, -1):
            self.memory_vars[i + 1].set(self.memory_vars[i].get())
        self.memory_vars[start_index].set(0)'''

