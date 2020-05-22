from tkinter import *
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
from database import Database


class Client(object):
    """A class that creates a client. A tkinter box that allows users to make actions."""

    def __init__(self, tk_window):
        self.window = tk_window
        tk_window.geometry("900x600")
        self.window.wm_title("CSV to Database converter")

        # Adding a horizontal scrollbar to a frame where csv file content is being read.
        frame = Frame(tk_window, bd=2, relief=GROOVE)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.grid(row=1, column=0, sticky=E + W)
        self.display_file_content = Text(frame, wrap=NONE, bd=0, xscrollcommand=x_scrollbar.set, height=10, width=40)
        self.display_file_content.grid(row=0, column=0, sticky=N + S + E + W)
        x_scrollbar.config(command=self.display_file_content.xview)
        frame.grid(column=10, row=20)

        import_file_button = Button(tk_window, text="Import CSV File", command=self.import_csv_file)
        import_file_button.grid(column=0, row=5)

        db_name_label = Label(tk_window, text="Enter Database Name:")
        db_name_label.grid(column=0, row=15)
        self.db_name = StringVar()
        db_name_field = Entry(tk_window, textvariable=self.db_name)
        db_name_field.grid(column=0, row=16)

        confirm_db_button = Button(tk_window, text="Confirm Database", command=self.confirm_database)
        confirm_db_button.grid(column=0, row=17)

    def import_csv_file(self):
        # A method that imports a csv file and outputs its content in a frame. (Text widget)
        self.display_file_content.delete(1.0, END)
        csv_file_path = filedialog.askopenfilename(title="Select a .csv file", filetypes=(("CSV Files", "*.csv"),))
        try:
            df_data = pd.read_csv(csv_file_path)
            content_to_display = "Preview: \n {} \n \n Total Columns:{} \n Total Rows: {}".format(
                df_data.head().to_string(),
                len(df_data.columns),
                len(df_data)
            )
            self.display_file_content.insert(INSERT, content_to_display)
        except FileExistsError:
            messagebox.showerror("File Do Not Exit", "Unable to find requested file. Please check if file exists.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "File could not be opened. Choose a valid .csv type file.")

    def confirm_database(self):
        # Creates a database out of csv file with given name.
        print(self.db_name.get())
        database = Database(self.db_name.get())


window = Tk()
Client(window)
window.mainloop()
