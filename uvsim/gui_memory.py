import tkinter as tk

class Memory(tk.Frame):
    def __init__(self, memory: list[int], master: tk.Misc | None, vcmd) -> None:
        super().__init__(master)
        self.label = tk.Label(master=self, text="Memory")
        self.frame = tk.Frame(master=self)
        self.memory_vars = [tk.IntVar(master=self, value=i) for i in memory]
        self.memory_frames = [tk.Entry(master=self.frame, font=None, validate='key', validatecommand=vcmd, textvariable=var, width=6) for var in self.memory_vars]
        self.label.pack(side="top", anchor="nw")
        self.frame.pack(side="left")

        for i, frame in enumerate(self.memory_frames):
            frame.grid(row=i // 10, column=i % 10, sticky="nesw", padx=2, pady=2)

        self.current_address = 0
        self.halted = True
        self.set_address(0)

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

    def set_address(self, address):
        self.memory_frames[self.current_address].configure(bg="SystemWindow")
        self.memory_frames[address].configure(bg="#FFAAAA" if self.halted else "SystemWindow")
        self.current_address = address

    def set_halted(self, halted):
        self.halted = halted
        self.memory_frames[self.current_address].configure(bg="#FFAAAA" if self.halted else "SystemWindow")
