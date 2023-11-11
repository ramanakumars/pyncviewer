import tkinter as tk
from tkinter import ttk
from .util_widgets import Toolbox
import netCDF4 as nc
import numpy as np


class AttributeWindow(ttk.Frame):
    def __init__(self, parent, filenames):
        super().__init__(parent)

        self.filenames = filenames

        self.selected = 0

        self.toolbox = Toolbox(self, filenames)
        self.toolbox.pack(fill='x', padx=10, pady=10, anchor='center')

        self.attributes_info_frame = AttributeInfo(self)
        self.attributes_info_frame.pack(fill='both', expand='yes')

        self.update()

    def select(self, selected):
        self.selected = selected
        self.update()

    def update(self):
        filename = self.filenames[self.selected]

        with nc.Dataset(filename, 'r') as indset:
            attributes = {key: getattr(indset, key) for key in indset.ncattrs()}

        self.attributes_info_frame.update_attributes(attributes)

    def open_attribute(self, attr_name):
        filename = self.filenames[self.selected]
        with nc.Dataset(filename, 'r') as indset:
            attr_value = getattr(indset, attr_name)

        window = AttributeInfo({'name': attr_name, 'value': attr_value})
        window.mainloop()


class AttributeInfo(tk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform=True)
        self.grid_columnconfigure(1, weight=2, uniform=True)

        self.attribute_selector = tk.Frame(self)
        self.info_panel = tk.Frame(self)

        self.attribute_selector.grid(row=0, column=0, padx=5, pady=5, sticky='nws')
        self.info_panel.grid(row=0, column=1, padx=5, pady=5, sticky='news')

    def update_attributes(self, attribute_data):
        self.attribute_data = attribute_data

        columns = ('attribute')

        for widgets in self.attribute_selector.winfo_children():
            widgets.destroy()
        for widgets in self.info_panel.winfo_children():
            widgets.destroy()

        self.attribute_selector.rowconfigure(0, weight=1)
        self.attribute_selector.grid_columnconfigure(0, weight=10, uniform=True)
        self.attribute_selector.grid_columnconfigure(1, weight=1, uniform=True)

        self.attribute_list = ttk.Treeview(self.attribute_selector, columns=columns, show='headings', selectmode="browse")

        # define headings
        self.attribute_list.heading('attribute', text='Attribute')

        for attr in self.attribute_data.keys():
            self.attribute_list.insert('', tk.END, values=(attr))

        self.attribute_list.grid(row=0, column=0, sticky='nsew')

        self.attribute_list.bind('<<TreeviewSelect>>', self.select_attribute)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.attribute_selector, orient=tk.VERTICAL, command=self.attribute_list.yview)
        self.attribute_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nsw')

    def select_attribute(self, event):
        for selected_item in self.attribute_list.selection():
            item = self.attribute_list.item(selected_item)
            attr = item['values'][0]
            self.display_attribute(attr)

    def display_attribute(self, attribute):
        for widgets in self.info_panel.winfo_children():
            widgets.destroy()
        attribute_value = self.attribute_data[attribute]

        if isinstance(attribute_value, str):
            self.show_string_attribute(attribute)
        elif isinstance(attribute_value, float) or isinstance(attribute_value, int):
            self.show_numeric_attribute(attribute)
        elif isinstance(attribute_value, list) or isinstance(attribute_value, np.ndarray):
            self.show_list_attribute(attribute)
        else:
            self.show_string_attribute(attribute)

    def show_string_attribute(self, attribute):
        attribute_data = ttk.Label(self.info_panel, text=self.attribute_data[attribute])
        attribute_data.pack(padx=10, pady=10, fill='x', expand='yes', anchor=tk.NW)

    def show_numeric_attribute(self, attribute):
        attribute_data = ttk.Label(self.info_panel, text=str(self.attribute_data[attribute]))
        attribute_data.pack(padx=10, pady=10, fill='x', expand='yes', anchor=tk.NW)

    def show_list_attribute(self, attribute):
        columns = ('index', 'value')

        tree = ttk.Treeview(self.info_panel, columns=columns, show='headings')

        self.info_panel.rowconfigure(0, weight=1)
        self.info_panel.grid_columnconfigure(0, weight=25, uniform=True)
        self.info_panel.grid_columnconfigure(1, weight=1, uniform=True)

        # define headings
        tree.heading('index', text='Index')
        tree.heading('value', text='Value')

        for i, value in enumerate(self.attribute_data[attribute]):
            tree.insert('', tk.END, values=(str(i), str(value)))

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_panel, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nsw')
