from tkinter import *
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
from pandas.errors import EmptyDataError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Client(object):
    """A class that creates a client. A tkinter box that allows users to make actions."""

    def __init__(self, tk_window):
        self.window = tk_window
        tk_window.geometry("900x600")
        self.window.wm_title("CSV-to-Database converter")
        self.df_data = None
        self.Base = declarative_base()

        # Adding a horizontal scrollbar to a frame where csv file content is being read.
        frame = Frame(tk_window, bd=2, relief=GROOVE)
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.grid(row=1, column=0, sticky=E + W)
        self.display_file_content = Text(frame, wrap=NONE, bd=0, xscrollcommand=x_scrollbar.set, height=12, width=40)
        self.display_file_content.grid(row=0, column=0, sticky=N + S + E + W)
        x_scrollbar.config(command=self.display_file_content.xview)
        frame.grid(column=40, row=0)

        import_file_button = Button(tk_window, text="Import CSV File", command=self.import_csv_file)
        import_file_button.grid(column=0, row=0)

        db_name_label = Label(tk_window, text="Enter Database Name:")
        db_name_label.grid(column=0, row=15)
        self.db_name = StringVar()
        db_name_field = Entry(tk_window, textvariable=self.db_name)
        db_name_field.grid(column=0, row=16)

        self.confirm_db_button = Button(tk_window, text="Confirm Database", command=self.confirm_database)
        self.confirm_db_button.grid(column=0, row=17)
        self.confirm_db_button["state"] = DISABLED

    def import_csv_file(self):
        # Imports a .csv file and reads it as pandas dataframe
        csv_file_path = filedialog.askopenfilename(title="Select a .csv file", filetypes=(("CSV Files", "*.csv"),))
        try:
            self.df_data = pd.read_csv(csv_file_path)
            self.display_dataframe(self.df_data)
            self.confirm_db_button["state"] = NORMAL
            return self.df_data
        except FileExistsError:
            messagebox.showerror("File Do Not Exit", "Unable to find requested file. Please check if file exists.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "File could not be opened. Choose a valid .csv type file.")
        except EmptyDataError:
            messagebox.showerror("Empty File", "No columns to parse from file")

    def display_dataframe(self, df_data):
        # A method that displays a preview of imported .csv file. (Output in a text widget)
        self.display_file_content.delete(1.0, END)
        content_to_display = "Preview: \n \n {} \n \n Total Columns:{} \n Total Rows: {}".format(
            df_data.head().to_string(),
            len(df_data.columns),
            len(df_data)
        )
        self.display_file_content.insert(INSERT, content_to_display)
        self.display_file_content.config(state=DISABLED)

    def confirm_database(self):
        # Creates a database from imported csv file with given name.
        print(self.db_name.get())
        engine = create_engine("sqlite:///" + self.db_name.get() + ".db")
        self.Base.metadata.create_all(engine)
        self.df_data.to_sql(self.db_name.get(), con=engine, index=True, if_exists='replace')


window = Tk()
Client(window)
window.mainloop()
