import tkinter as tk
from tkinter import messagebox
from uvsim.constants import WORD_SIZE

ROW_WIDTH = 10
COLS = WORD_SIZE // ROW_WIDTH


class Memory(tk.Frame):
    """
    The Memory class represents the memory of the UVSim CPU in a GUI.
    It inherits from the tk.Frame class.
    It gives a visual representation of the memory by crating a grid of memory cells.
    """

    def __init__(self, memory: list[int], master: tk.Misc | None, vcmd) -> None:
        """
        Purpose:
            Initializes the Memory class with the provided memory array and sets up the GUI elements to represent the memory.
        Input Parameters:
            memory: An array representing the memory content.
            master: The master widget of the memory frame.
            vcmd: The validation command for memory entries.
        Return Value:
            None.
        """
        super().__init__(master)
        self.label = tk.Label(master=self, text="Memory")
        self.label.grid(row=0, column=0)

        self.memory_vars = [tk.IntVar(master=self, value=i) for i in memory]
        self.memory_frames = [
            tk.Entry(
                master=self,
                font=None,
                validate="key",
                validatecommand=vcmd,
                textvariable=var,
                width=6,
                borderwidth=1,
            )
            for var in self.memory_vars
        ]
        for i, frame in enumerate(self.memory_frames):
            frame.grid(
                row=(i // ROW_WIDTH) + 1,
                column=(i % ROW_WIDTH) + 1,
                sticky="nesw",
                padx=0,
                pady=0,
            )

        self.vertical_labels = [
            tk.Label(
                master=self,
                text=f"{i * ROW_WIDTH:04}",
                bg="lightgrey",
                font=("Arial", 10, "bold"),
            )
            for i in range(COLS)
        ]
        for i, label in enumerate(self.vertical_labels):
            label.grid(row=i + 1, column=0, sticky="nesw", padx=2, pady=2)

        self.horizontal_labels = [
            tk.Label(
                master=self, text=f"{i:02}", bg="lightgrey", font=("Arial", 10, "bold")
            )
            for i in range(ROW_WIDTH)
        ]
        for i, label in enumerate(self.horizontal_labels):
            label.grid(row=0, column=i + 1, sticky="nesw", padx=2, pady=2)

        self.defaultbg = self.memory_frames[0].cget("bg")

        self._program_counter = 0
        self._halted = True

        self.program_counter = 0
        self.halted = True

        self.selected_frames = set()
        self.clipboard_content = None
        self.start_cell = None
        self.end_cell = None



    def handle_click(self, event):
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
                self.memory_frames[frame_index].configure(bg="blue")

    def get_frame_index(self, x, y):
        col = x // self.memory_frames[0].winfo_width()
        row = y // self.memory_frames[0].winfo_height()
        if 0 <= row < ROW_WIDTH and 0 <= col < COLS:
            return row * ROW_WIDTH + col
        else:
            return None

    def deselect_frames(self):
        for index in self.selected_frames:
            self.memory_frames[index].configure(bg=self.defaultbg)
        self.selected_frames.clear()


    def handle_drag(self, event):
        x = event.x_root - self.memory_frames[0].winfo_rootx()
        y = event.y_root - self.memory_frames[0].winfo_rooty()
        frame_index = self.get_frame_index(x, y)
        if frame_index is not None:
            if frame_index not in self.selected_frames:
                self.selected_frames.add(frame_index)
                self.memory_frames[frame_index].configure(bg="blue")


    def cut(self):
        if self.selected_frames:
            self.clipboard = [self.memory_vars[i].get() for i in self.selected_frames]
            for i in self.selected_frames:
                self.memory_vars[i].set(0)
            self.deselect_frames()

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
            self.memory_vars[start_index + i].set(value)


    def shift_memory(self, start_index):
        """
        Shifts memory contents starting from start_index to the right to make space.
        """
        for i in range(WORD_SIZE - 2, start_index - 1, -1):
            self.memory_vars[i + 1].set(self.memory_vars[i].get())
        self.memory_vars[start_index].set(0)



    def __getitem__(self, key):
        """
        Purpose:
            Allows accessing the memory content.
        Input Parameters:
            key: Index or slice to access the memory content.
        Return Value:
            The value at the index or slice.
        """
        if type(key) is int:
            return self.memory_vars[key].get()
        else:
            return self.memory_vars[int(key)].get()

    def __setitem__(self, key: str, value) -> None:
        """
        Purpose:
            Allows setting the memory content.
        Input Parameters:
            key: Index or slice to set the memory content.
            value: The value that will be set.
        Return Value:
            None.
        """
        if type(key) is int:
            return self.memory_vars[key].set(value)
        else:
            return self.memory_vars[int(key)].set(value)

    @property
    def program_counter(self):
        """
        Purpose:
            Getter and setter for the program counter property.
            It updates the GUI to highlight the current program counter cell.
        Input Parameters:
            None.
        Return Value:
            The current value of the program counter.
        """
        return self._program_counter

    @program_counter.setter
    def program_counter(self, value):
        self.memory_frames[self._program_counter].configure(bg=self.defaultbg)
        self.memory_frames[value].configure(
            bg="#FFAAAA" if self._halted else self.defaultbg
        )
        self._program_counter = value

    @property
    def halted(self):
        """
        Purpose:
            Getter and setter for the halted property.
            It updates the GUI to highlight the current program counter cell with a different color if the CPU is halted.
        Input Parameters:
            None.
        Return Value:
            True if the CPU is halted, False otherwise.
        """
        return self._halted

    @halted.setter
    def halted(self, value):
        self._halted = value
        self.memory_frames[self._program_counter].configure(
            bg="#FFAAAA" if self.halted else self.defaultbg
        )
