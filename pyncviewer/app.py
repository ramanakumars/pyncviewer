import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from .attributes import AttributeWindow
from .util_widgets import LabelString


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('My app')
        self.geometry('600x600')
        self.minsize(600, 600)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.info_panel = InfoFrame(self)

    def set_filename(self, filenames):
        self.info_panel.pack_forget()
        self.filenames = filenames
        self.info_panel.update_filenames(self.filenames)
        self.info_panel.pack(padx=10, pady=10, fill='x')

    def view_filenames(self):
        return

    def view_attributes(self):
        window = AttributeWindow('View Attributes', self.filenames)
        window.mainloop()

    def view_variables(self):
        return


class Menu(tk.Menu):
    def __init__(self, parent):
        self.parent = parent

        super().__init__(self.parent)

        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(
            label='Open',
            command=self.open_file
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label='Exit',
            command=self.parent.destroy
        )
        # add these options under the file menu
        self.add_cascade(
            label='File',
            menu=self.file_menu
        )
        # self.add_cascade(
        #     label='Inspect',
        #     menu=self.inspect_file
        # )

    def open_file(self):
        filetypes = (
            ("netCDF4 files", "*.nc"),
            ("All files", "*.*")
        )
        filenames = sorted(fd.askopenfilenames(
            filetypes=filetypes
        ))
        self.parent.set_filename(filenames)


class InfoFrame(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        self.entry = ttk.Label(self)
        self.entry.pack(padx=10, pady=10, fill='x', expand=True)

        self.file_info = LabelString(self.entry)

        self.inspect_file = tk.Frame(self)
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

        view_fnames.grid(row=0, column=0, padx=10, pady=10)
        view_attributes.grid(row=0, column=1, padx=10, pady=10)
        view_variables.grid(row=0, column=2, padx=10, pady=10)

        self.inspect_file.pack(padx=5, pady=5, fill=tk.X, expand=tk.YES)

    def update_filenames(self, filenames):
        self.file_info.set(f'Loaded {len(filenames)} files')


if __name__ == "__main__":
    app = App()

    app.mainloop()
