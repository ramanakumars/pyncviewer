import tkinter as tk
from tkinter import ttk
import os


ATTR_BUTTON_SIZE = 120


class LabelString(tk.StringVar):
    def __init__(self, label):
        self.label = label
        super().__init__()

    def set(self, text):
        super().set(text)
        self.label['text'] = text


class Toolbox(ttk.Frame):
    def __init__(self, parent, filenames):
        self.parent = parent
        self.filenames = filenames

        super().__init__(parent)

        self.selected = 0
        self.nfiles = len(self.filenames)

        self.left_button = ttk.Button(
            self, text='Previous', command=self.select_previous
        )
        self.filename_label = ttk.Label(
            self, text=''
        )
        self.right_button = ttk.Button(
            self, text='Next', command=self.select_next
        )

        self.check_button_state()

        self.selected_filename = LabelString(self.filename_label)
        self.update_label(self.filenames[self.selected])

        self.left_button.grid(row=0, column=0, padx=5, pady=5)
        self.filename_label.grid(row=0, column=1, padx=5, pady=5)
        self.right_button.grid(row=0, column=2, padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1, uniform=True)
        self.grid_columnconfigure(1, weight=2, uniform=True)
        self.grid_columnconfigure(2, weight=1, uniform=True)

    def check_button_state(self):
        if self.selected == 0:
            self.left_button.config(state=tk.DISABLED)
        if self.selected < self.nfiles - 1:
            self.right_button.config(state=tk.NORMAL)
        if self.selected > 0:
            self.left_button.config(state=tk.NORMAL)
        if self.selected == self.nfiles - 1:
            self.right_button.config(state=tk.DISABLED)

    def select_previous(self):
        self.selected = max([0, self.selected - 1])
        self.update_label(self.filenames[self.selected])
        self.parent.select(self.selected)
        self.check_button_state()

    def select_next(self):
        self.selected = min([len(self.filenames) - 1, self.selected + 1])
        self.update_label(self.filenames[self.selected])
        self.parent.select(self.selected)
        self.check_button_state()

    def update_label(self, filename):
        self.selected_filename.set(f'{os.path.basename(filename)} [{self.selected + 1}/{self.nfiles}]')


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
