import tkinter as tk
from tkinter import ttk
from .util_widgets import Toolbox, ScrollableCanvas, LabelString, ATTR_BUTTON_SIZE
import netCDF4 as nc
import os
import numpy as np


class AttributeWindow(tk.Tk):
    def __init__(self, title, filenames):
        super().__init__()
        self.title(title)
        self.geometry('600x300')
        self.minsize(600, 300)

        self.filenames = filenames

        self.selected = 0

        self.toolbox = Toolbox(self)
        self.toolbox.pack(padx=10, pady=10)

        self.filename_label = ttk.Label(self)
        self.filename_label.pack(pady=10, padx=10, fill='x', anchor=tk.N)

        self.selected_filename = LabelString(self.filename_label)
        self.selected_filename.set('No files loaded')

        self.canvas = ScrollableCanvas(self)
        self.update()

    def select_previous(self):
        self.selected = max([0, self.selected - 1])
        self.update()

    def select_next(self):
        self.selected = min([self.selected + 1, len(self.filenames) - 1])
        self.update()

    def update(self):
        filename = self.filenames[self.selected]
        self.selected_filename.set(f'Showing attributes for {os.path.basename(filename)}')

        with nc.Dataset(filename, 'r') as indset:
            attributes = {key: getattr(indset, key) for key in indset.ncattrs()}

        img = tk.PhotoImage(master=self, width=ATTR_BUTTON_SIZE)

        for widget in self.canvas.container.winfo_children():
            widget.destroy()

        btns = []
        for i, attr in enumerate(attributes.keys()):
            btns.append(ttk.Button(self.canvas.container, text=attr, image=img, compound='c', command=lambda attr=attr: self.open_attribute(attr)))

        self.canvas.add_buttons(btns)

    def open_attribute(self, attr_name):
        filename = self.filenames[self.selected]
        with nc.Dataset(filename, 'r') as indset:
            attr_value = getattr(indset, attr_name)

        window = AttributeInfo({'name': attr_name, 'value': attr_value})
        window.mainloop()


class AttributeInfo(tk.Tk):
    def __init__(self, attribute_data):
        self.attribute_data = attribute_data
        super().__init__()
        self.title(attribute_data['name'])
        self.geometry('600x300')
        self.minsize(600, 300)

        attribute_value = attribute_data['value']

        self.info_frame = ttk.Frame(self)
        if isinstance(attribute_value, str):
            self.show_string_attribute()
        elif isinstance(attribute_value, float) or isinstance(attribute_value, int):
            self.show_numeric_attribute()
        elif isinstance(attribute_value, list) or isinstance(attribute_value, np.ndarray):
            self.show_list_attribute()
        else:
            self.show_string_attribute()

        self.info_frame.pack(padx=5, pady=5, fill='both', expand='yes')

    def show_string_attribute(self):
        self.attribute_data = ttk.Label(self.info_frame, text=self.attribute_data['value'])
        self.attribute_data.pack(padx=10, pady=10, fill='x')

    def show_numeric_attribute(self):
        self.attribute_data = ttk.Label(self.info_frame, text=str(self.attribute_data['value']))
        self.attribute_data.pack(padx=10, pady=10, fill='x')

    def show_list_attribute(self):
        columns = ('index', 'value')

        tree = ttk.Treeview(self.info_frame, columns=columns, show='headings')

        # define headings
        tree.heading('index', text='Index')
        tree.heading('value', text='Value')

        for i, value in enumerate(self.attribute_data['value']):
            tree.insert('', tk.END, values=(str(i), str(value)))

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
