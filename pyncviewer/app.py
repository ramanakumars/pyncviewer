import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from .viewer import FileViewer


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('PyNCViewer')
        self.geometry('300x100')
        self.minsize(300, 100)

        button_frame = ttk.Frame(self)
        browse_button = ttk.Button(
            button_frame,
            text='Browse',
            command=self.open_file,
            width=20
        )
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        browse_button.grid(row=0, column=0, padx=10, pady=10)
        button_frame.pack(padx=5, pady=5, fill='both', expand='true')

    def open_file(self):
        filetypes = (
            ("netCDF4 files", "*.nc"),
            ("All files", "*.*")
        )
        filenames = sorted(fd.askopenfilenames(
            filetypes=filetypes
        ))
        if len(filenames) > 0:
            self.set_filename(filenames)

    def set_filename(self, filenames):
        file_window = FileViewer(filenames)
        file_window.mainloop()


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


if __name__ == "__main__":
    app = App()

    app.mainloop()
