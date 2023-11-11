import tkinter as tk
from tkinter import ttk
from .attributes import AttributeWindow
from .util_widgets import LabelString


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

    def view_filenames(self):
        return

    def view_attributes(self):
        self.main_panel.destroy()
        self.main_panel = AttributeWindow(self, self.filenames)
        self.main_panel.pack(padx=5, pady=10, fill='both', expand='yes', anchor='n')

    def view_variables(self):
        return


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
        self.inspect_file.grid_columnconfigure(2, weight=1, uniform=True)
        view_fnames = ttk.Button(
            self.inspect_file,
            text='View filenames',
            command=self.parent.view_filenames
        )
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

        view_fnames.grid(row=0, column=0, padx=10, pady=5)
        view_attributes.grid(row=0, column=1, padx=10, pady=5)
        view_variables.grid(row=0, column=2, padx=10, pady=5)

        self.inspect_file.pack(padx=5, pady=5, fill=tk.X, expand=tk.YES)

    def update_filenames(self, filenames):
        self.file_info.set(f'Loaded {len(filenames)} files')
