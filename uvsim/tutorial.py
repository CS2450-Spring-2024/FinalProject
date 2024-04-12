import tkinter as tk
from PIL import ImageTk, Image
import os

from uvsim.constants import FONT
 

class Tutorial:
    """
    The Tutorial class will display a tutorial for the UVSim application using images.
    It creates a simple Tkinter GUI with buttons to navigate through the tutorial images.
    """
    def __init__(self, master: tk.Tk) -> None:
        """
        Purpose:
            Initializes the Tutorial class with the provided master widget and sets up the GUI elements for displaying tutorial images.
        Input Parameters:
            master: The master widget of the Tutorial frame.
        Return Value: 
            None.
        """
        width = 13
        self.master = master

        self.master.geometry("1500x800")
        self.master.title("Tutorial")
        self.master.configure()
        

        self.master_frame = tk.Frame(self.master)
        self.master_frame.columnconfigure((0, 4), weight=1)
        self.master_frame.rowconfigure(index=0, weight=3)
        self.master_frame.rowconfigure(index=2, weight=1)

        self.upper_frame = tk.Frame(self.master_frame)
        self.upper_frame.grid(column=0, row=0, sticky="n", padx=3, pady=3)

        self.image_list = self.open_images()
        self.image_count = len(self.image_list)
        self.image_iter = iter(self.image_list)
        self.current_image = tk.Label(self.upper_frame, image=next(self.image_iter))
        self.current_image.grid(column=0, row=0, sticky="n", padx=3, pady=3)

        self.lower_frame = tk.Frame(self.master_frame)
        self.lower_frame.grid(column=0, row=2, sticky="s", padx=3, pady=3)

        self.bttns = [
            tk.Button(
                self.lower_frame,
                font=FONT,
                command=self.get_next,
                width=width,
                text="Next",
            ),
            tk.Button(
                self.lower_frame,
                font=FONT,
                command=self.master.destroy,
                width=width,
                text="Exit",
            ),
        ]

        for idx, ele in enumerate(self.bttns, 2):
            ele.grid(row=4, column=idx, sticky="se", padx=50, pady=20)

        self.master_frame.pack(fill="both", expand=True)

    def get_next(self):
        """
        Purpose:
            Updates the displayed image to the next image in the tutorial when the "Next" button is clicked.
        Input Parameters:
            None.
        Return Value:
            None.
        """
        try:
            self.current_image.config(image=next(self.image_iter))
        except StopIteration:
            self.master.destroy()

    def open_images(self) -> list[str]:
        """
        Purpose:
            Opens tutorial images from a specified directory and converts them into Tkinter PhotoImage objects.
        Input Parameters:
            None.
        Return Value:
            A list of Tkinter PhotoImage objects representing the tutorial images.
        """
        lyst = [
            ImageTk.PhotoImage(
                Image.open(os.path.join(r"uvsim\tutorial_images", filepath))
            )
            for filepath in os.listdir(r"uvsim\tutorial_images")
        ]
        return lyst
