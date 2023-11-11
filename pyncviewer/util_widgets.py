import tkinter as tk
from tkinter import ttk


ATTR_BUTTON_SIZE = 120


class LabelString(tk.StringVar):
    def __init__(self, label):
        self.label = label
        super().__init__()

    def set(self, text):
        super().set(text)
        self.label['text'] = text


class Toolbox(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent

        super().__init__(parent)

        self.left_button = ttk.Button(
            self, text='Previous', command=self.parent.select_previous
        )
        self.right_button = ttk.Button(
            self, text='Next', command=self.parent.select_next
        )

        self.left_button.grid(row=0, column=0, padx=5, pady=5)
        self.right_button.grid(row=0, column=1, padx=5, pady=5)


class ScrollableCanvas(tk.Canvas):
    buttons: list = []

    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.scrollbar = ttk.Scrollbar(self.parent, command=self.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        self.configure(yscrollcommand=self.scrollbar.set)
        self.bind("<Configure>", lambda event: self.update())

        self.container = ttk.Frame(self)

        self.create_window((0, 0), window=self.container, anchor=tk.NW)

    def on_configure(self):
        self.configure(scrollregion=self.bbox('all'))

    def add_buttons(self, buttons):
        self.buttons = buttons
        self.update()

    def update(self):
        pad_size = 5
        width = self.winfo_width() - 10 - self.scrollbar.winfo_width()

        ncols = max([1, width // (ATTR_BUTTON_SIZE + pad_size) - 1])

        for j in range(ncols):
            self.container.grid_columnconfigure(j, weight=1)

        for i, btn in enumerate(self.buttons):
            row = i // ncols
            col = i % ncols
            btn.grid(row=row, column=col, padx=pad_size, pady=5)

        self.on_configure()
