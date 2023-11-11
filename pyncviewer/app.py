import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from .attributes import AttributeWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('My app')
        self.geometry('600x600')
        self.minsize(600, 600)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.menu.entryconfigure('Inspect', state=tk.DISABLED)

        self.info_panel = InfoFrame(self)
        self.info_panel.pack(padx=10, pady=10, fill='x')

    def set_filename(self, filenames):
        self.filenames = filenames
        self.info_panel.update_filenames(self.filenames)
        self.menu.entryconfigure('Inspect', state="normal")

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

        self.inspect_menu = tk.Menu(self, tearoff=False)
        self.inspect_menu.add_command(
            label='View filenames',
            command=self.parent.view_filenames
        )
        self.inspect_menu.add_command(
            label='View attributes',
            command=self.parent.view_attributes
        )
        self.inspect_menu.add_command(
            label='View variables',
            command=self.parent.view_variables
        )

        # add these options under the file menu
        self.add_cascade(
            label='File',
            menu=self.file_menu
        )
        self.add_cascade(
            label='Inspect',
            menu=self.inspect_menu
        )

    def open_file(self):
        filetypes = (
            ("netCDF4 files", "*.nc"),
            ("All files", "*.*")
        )
        filenames = sorted(fd.askopenfilenames(
            filetypes=filetypes
        ))
        self.parent.set_filename(filenames)
        return


class InfoFrame(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        self.file_info = tk.StringVar()

        self.entry = ttk.Label(self, textvariable=self.file_info)
        self.entry.pack(padx=10, pady=10, fill='x')

    def update_filenames(self, filenames):
        self.file_info.set(f'Loaded {len(filenames)} files')


if __name__ == "__main__":
    app = App()

    app.mainloop()
