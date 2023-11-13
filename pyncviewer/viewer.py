import tkinter as tk
from tkinter import ttk
from .attributes import AttributeWindow
from .variables import Variable, GridVariable, VariableWindow
from .util_widgets import LabelString
import netCDF4 as nc
import os
from collections import defaultdict


class FileViewer(tk.Tk):
    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames

        self.title('PyNCViewer file explorer')
        self.geometry('600x600')
        self.minsize(600, 600)

        self.info_panel = InfoFrame(self)
        self.info_panel.update_filenames(self.filenames)
        self.info_panel.pack(padx=10, pady=5, fill='x')

        self.main_panel = ttk.Frame()

        self.get_attributes()
        self.get_variables()

    def get_attributes(self):
        self.attributes = defaultdict(dict)
        for fname in self.filenames:
            with nc.Dataset(fname, 'r') as indset:
                self.attributes[os.path.basename(fname)] = {key: getattr(indset, key) for key in indset.ncattrs()}

    def get_variables(self):
        self.variables = defaultdict(list)

        self.grid_variables = defaultdict(list)

        self.time = defaultdict(float)

        for fname in self.filenames:
            with nc.Dataset(fname, 'r') as indset:
                # get the dimensions first
                for dimension in indset.dimensions.keys():
                    var_data = indset.variables[dimension]
                    # store time data right now
                    if dimension == 'time':
                        self.time[os.path.basename(fname)] = var_data[:][0]
                        continue
                    else:
                        self.grid_variables[os.path.basename(fname)].append(GridVariable(var_data, fname))

                # get all the other variable info
                for var, var_data in indset.variables.items():
                    # parse the other metadata
                    if len(var_data.shape) >= 3:
                        self.variables[os.path.basename(fname)].append(Variable(var_data, fname))

    def view_attributes(self):
        self.main_panel.destroy()
        self.main_panel = AttributeWindow(self, self.filenames, self.attributes)
        self.main_panel.pack(padx=5, pady=10, fill='both', expand='yes', anchor='n')

    def view_variables(self):
        self.main_panel.destroy()
        self.main_panel = VariableWindow(self, self.filenames, self.variables)
        self.main_panel.pack(padx=5, pady=10, fill='both', expand='yes', anchor='n')


class InfoFrame(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        self.entry = ttk.Label(self)
        self.entry.pack(padx=10, pady=10, fill='x', anchor=tk.N, expand=True)

        self.file_info = LabelString(self.entry)

        self.inspect_file = tk.Frame(self)
        self.inspect_file.grid_columnconfigure(0, weight=1, uniform=True)
        self.inspect_file.grid_columnconfigure(1, weight=1, uniform=True)
        view_attributes = ttk.Button(
            self.inspect_file,
            text='View attributes',
            command=self.parent.view_attributes
        )
        view_variables = ttk.Button(
            self.inspect_file,
            text='View variables',
            command=self.parent.view_variables
        )

        view_attributes.grid(row=0, column=0, padx=10, pady=5)
        view_variables.grid(row=0, column=1, padx=10, pady=5)

        self.inspect_file.pack(padx=5, pady=5, fill=tk.X, expand=tk.YES)

    def update_filenames(self, filenames):
        self.file_info.set(f'Loaded {len(filenames)} files')


def get_variable_info(variable):
    attrs = {key: getattr(variable, key) for key in variable.ncattrs()}
    return {
        'shape': variable.shape,
        **attrs
    }
