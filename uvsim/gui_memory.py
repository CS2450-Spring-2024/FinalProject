import tkinter as tk

from uvsim.constants import MEM_SIZE

ROW_WIDTH = 10
COLS = MEM_SIZE // ROW_WIDTH

class Memory(tk.Frame):
    def __init__(self, memory: list[int], master: tk.Misc | None, vcmd) -> None:
        super().__init__(master)
        self.label = tk.Label(master=self, text="Memory")
        self.label.grid(row=0, column=0)

        self.memory_vars = [tk.IntVar(master=self, value=i) for i in memory]
        self.memory_frames = [tk.Entry(master=self, font=None, validate='key', validatecommand=vcmd, textvariable=var, width=6, borderwidth=1) for var in self.memory_vars]
        for i, frame in enumerate(self.memory_frames):
            frame.grid(row=(i // ROW_WIDTH) + 1, column=(i % ROW_WIDTH) + 1, sticky="nesw", padx=0, pady=0)

        self.vertical_labels = [tk.Label(master=self, text=str(i * ROW_WIDTH)) for i in range(ROW_WIDTH)]
        for i, frame in enumerate(self.vertical_labels):
            frame.grid(row=i + 1, column = 0, sticky="nesw", padx=2, pady=2)

        self.horizontal_labels = [tk.Label(master=self, text=str(i)) for i in range(COLS)]
        for i, frame in enumerate(self.horizontal_labels):
            frame.grid(row=0, column=i + 1, sticky="nesw", padx=2, pady=2)

        self._program_counter = 0
        self._halted = True

        self.program_counter = 0
        self.halted = True

    def __getitem__(self, key):
        if type(key) is int:
            return self.memory_vars[key].get()
        else:
            return self.memory_vars[int(key)].get()

    def __setitem__(self, key: str, value) -> None:
        if type(key) is int:
            return self.memory_vars[key].set(value)
        else:
            return self.memory_vars[int(key)].set(value)

    @property
    def program_counter(self):
        return self._program_counter

    @program_counter.setter
    def program_counter(self, value):
        self.memory_frames[self._program_counter].configure(bg="SystemWindow")
        self.memory_frames[value].configure(bg="#FFAAAA" if self._halted else "SystemWindow")
        self._program_counter = value

    @property
    def halted(self):
        return self._halted

    @halted.setter
    def halted(self, value):
        self._halted = value
        self.memory_frames[self._program_counter].configure(bg="#FFAAAA" if self.halted else "SystemWindow")
