import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# create a custom widget
class Input(tk.Frame):
    def __init__(self, master, label):
        super().__init__(master)
        self.label = ttk.Label(self, text=label, anchor=tk.W)
        self.entry = ttk.Entry(
            self,
        )
        self.label.pack(anchor="w")
        self.entry.pack(pady=(5, 10))
        self.pack()


class Infomation(tk.Frame):
    def __init__(self, master, label):
        super().__init__(master)

        # Create an image with a semi-transparent background
        width, height = 200, 50  # Adjust the size as needed
        background_color = (255, 247, 0, 12)  # RGBA: light blue with 50% opacity
        image = Image.new("RGBA", (width, height), background_color)
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label with the image as the background
        self.label = ttk.Label(
            self, text=label, anchor=tk.W, borderwidth=2, relief="solid"
        )
        self.label.pack(anchor="w")

        # Create a canvas to place the label on top of the image
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.create_window(0, 0, anchor=tk.NW, window=self.label)
        self.canvas.pack()

        self.pack()
