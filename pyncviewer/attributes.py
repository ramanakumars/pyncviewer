import tkinter as tk
from tkinter import ttk
from .util_widgets import Toolbox
import os
import numpy as np


class AttributeWindow(ttk.Frame):
    def __init__(self, parent: tk.Tk, filenames: list[str], attributes: list[dict]):
        super().__init__(parent)

        self.filenames = filenames
        self.attributes = attributes

        self.selected = 0
        filename = self.filenames[self.selected]
        self.selected_fname = os.path.basename(filename)

        self.toolbox = Toolbox(self, filenames)
        self.toolbox.pack(fill='x', padx=10, pady=10, anchor='center')

        self.attributes_info_frame = AttributeInfo(self, attributes)
        self.attributes_info_frame.pack(fill='both', expand='yes')

        self.update()

    def select(self, selected: int):
        self.selected = selected
        self.update()

    def update(self):
        filename = self.filenames[self.selected]

        self.selected_fname = os.path.basename(filename)

        self.attributes_info_frame.update_attributes(self.selected_fname)


class AttributeInfo(tk.Frame):
    def __init__(self, parent: tk.Tk, attributes: list[dict], **kwargs):
        self.parent = parent
        self.attribute_data = attributes
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform=True)
        self.grid_columnconfigure(1, weight=2, uniform=True)

        self.attribute_selector = tk.Frame(self)
        self.info_panel = tk.Frame(self)

        self.attribute_selector.grid(row=0, column=0, padx=5, pady=5, sticky='nws')
        self.info_panel.grid(row=0, column=1, padx=5, pady=5, sticky='news')

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

        self.attribute_list.grid(row=0, column=0, sticky='nsew')

        self.attribute_list.bind('<<TreeviewSelect>>', self.select_attribute)

        self.selected_fname = self.parent.selected_fname

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.attribute_selector, orient=tk.VERTICAL, command=self.attribute_list.yview)
        self.attribute_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nsw')

    def update_attributes(self, selected_fname: str):
        self.selected_fname = selected_fname
        file_attributes = list(self.attribute_data[selected_fname].keys())
        items = []
        for i, itID in enumerate(self.attribute_list.get_children('')):
            items.append(self.attribute_list.item(itID))
        item_attributes = [item['values'][0] for item in items]

        attributes = sorted(set((*file_attributes, *item_attributes)))
        for i, name in enumerate(attributes):
            if (name in file_attributes) and (name not in item_attributes):
                self.attribute_list.insert('', i, values=(name))
            if (name in item_attributes) and (name not in file_attributes):
                item = next(filter(lambda it: it['values'][0] == name), items)
                self.attribute_list.delete(item)

        self.select_attribute(None)

    def select_attribute(self, event: tk.Event):
        for selected_item in self.attribute_list.selection():
            item = self.attribute_list.item(selected_item)
            attr = item['values'][0]
            self.display_attribute(attr)

    def display_attribute(self, attribute: str):
        for widgets in self.info_panel.winfo_children():
            widgets.destroy()
        attribute_value = self.attribute_data[self.selected_fname][attribute]

        if isinstance(attribute_value, str):
            self.show_string_attribute(attribute, attribute_value)
        elif isinstance(attribute_value, float) or isinstance(attribute_value, int):
            self.show_numeric_attribute(attribute, attribute_value)
        elif isinstance(attribute_value, bool):
            self.show_boolean_attribute(attribute, attribute_value)
        elif isinstance(attribute_value, list) or isinstance(attribute_value, np.ndarray):
            self.show_list_attribute(attribute, attribute_value)
        else:
            self.show_string_attribute(attribute, attribute_value)

    def show_string_attribute(self, attribute: str, value: str):
        attribute_data = ttk.Label(self.info_panel, text=value)
        attribute_data.pack(padx=10, pady=10, fill='x', expand='yes', anchor=tk.NW)

    def show_numeric_attribute(self, attribute: str, value: float | int):
        attribute_data = ttk.Label(self.info_panel, text=str(value))
        attribute_data.pack(padx=10, pady=10, fill='x', expand='yes', anchor=tk.NW)

    def show_boolean_attribute(self, attribute: str, value: bool):
        attribute_data = ttk.Label(self.info_panel, text='True' if value else 'False')
        attribute_data.pack(padx=10, pady=10, fill='x', expand='yes', anchor=tk.NW)

    def show_list_attribute(self, attribute: str, value: list | np.ndarray):
        columns = ('index', 'value')

        tree = ttk.Treeview(self.info_panel, columns=columns, show='headings')

        self.info_panel.rowconfigure(0, weight=1)
        self.info_panel.grid_columnconfigure(0, weight=25, uniform=True)
        self.info_panel.grid_columnconfigure(1, weight=1, uniform=True)

        # define headings
        tree.heading('index', text='Index')
        tree.heading('value', text='Value')

        for i, val in enumerate(value):
            tree.insert('', tk.END, values=(str(i), str(val)))

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_panel, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nsw')
