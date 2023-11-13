import tkinter as tk
from tkinter import ttk
from .util_widgets import Toolbox
import netCDF4 as nc
import os
import numpy as np


class VariableWindow(ttk.Frame):
    def __init__(self, parent: tk.Tk, filenames: list[str]):
        self.parent = parent
        super().__init__(parent)

        self.filenames = filenames

        self.selected = 0

        self.toolbox = Toolbox(self, filenames)
        self.toolbox.pack(fill=tk.X, padx=10, pady=10, anchor=tk.CENTER)

        self.variable_info_frame = VariableInfo(self)
        self.variable_info_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.update()

    def select(self, selected: int):
        self.selected = selected
        self.update()

    def update(self):
        filename = self.filenames[self.selected]

        with nc.Dataset(filename, 'r') as indset:
            variables = [{'name': key, **get_variable_info(indset.variables[key])} for key in indset.variables.keys()]

        self.variable_info_frame.update_variable(variables)


class VariableInfo(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        self.parent = parent
        super().__init__(parent)

    def update_variables(self, variables):
        return


def get_variable_info(variable):
    attrs = {key: getattr(variable, key) for key in variable.ncattrs()}
    return {
        'shape': variable.shape,
        **attrs
    }


class Variable():
    def __init__(self, variable: nc.Variable, fname: str, grid_data: dict):
        self.filename = fname
        self.name = variable.name
        self.shape = variable.shape
        for key in variable.ncattrs():
            setattr(self, key, getattr(variable, key))

        if len(variable.dimensions) == 4:
            self.x = grid_data[variable.dimensions[3]]
            self.y = grid_data[variable.dimensions[2]]
            self.z = grid_data[variable.dimensions[1]]
        else:
            self.x = grid_data[variable.dimensions[2]]
            self.y = grid_data[variable.dimensions[1]]
            self.z = grid_data[variable.dimensions[0]]

    def get_value(self) -> np.ndarray:
        with open(self.filename, 'r') as indset:
            value = indset.variables[self.name][:]

        return value

    def __repr__(self):
        return f'{self.name} {self.shape} from {os.path.basename(self.filename)}'
