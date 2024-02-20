import tkinter as tk

class Memory(tk.Frame):
    def __init__(self, memory: list[int], master: tk.Misc | None, vcmd) -> None:
        super().__init__(master)
        self.memory_vars = [tk.IntVar(master=self, value=i) for i in memory]
        self.memory_frames = [tk.Entry(master=self, font=None, validate='key', validatecommand=vcmd, textvariable=var, width=6) for var in self.memory_vars]

        for i, frame in enumerate(self.memory_frames):
            frame.grid(row=i // 10, column=i % 10, sticky="nesw", padx=2, pady=2)

    def __getitem__(self, key):
        if type(key) is int:
            return self.memory_vars[key].get()
        else:
            return self.memory_vars[key.get()].get()

    def __setitem__(self, key: str, value) -> None:
        if type(key) is int:
            return self.memory_vars[key].set(value)
        else:
            return self.memory_vars[key.get()].set(value)
