from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import pandas as pd
from tkinter import messagebox
from pandas.errors import EmptyDataError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Client(object):
    """
    A class that creates a client.
    A tkinter box that allows users to convert a csv file to a local database
    using sql alchemy and sqlite3 libraries.
    """

    def __init__(self, tk_window):
        self.window = tk_window
        tk_window.geometry("495x255")
        self.window.wm_title("CSV-to-Database converter")
        self.df_data = None
        self.Base = declarative_base()

        import_file_button = Button(tk_window, text="Import File", command=self.import_csv_file)
        import_file_button.grid(column=0, row=0, sticky=W, pady=(0, 10), padx=(5, 0))

        db_name_label = Label(tk_window, text="Database Name:")
        db_name_label.grid(column=6, row=0, pady=(0, 10))
        self.db_name = StringVar()
        db_name_field = Entry(tk_window, textvariable=self.db_name)
        db_name_field.grid(column=7, row=0, pady=(0, 10))

        self.confirm_db_button = Button(tk_window, text="Confirm Database", command=self.create_database)
        self.confirm_db_button.grid(column=14, row=0, columnspan=2, pady=(0, 10))
        self.confirm_db_button["state"] = DISABLED

        # Adding a horizontal scrollbar to a frame where csv file content is written.
        content_frame = Frame(tk_window, bd=2, relief=GROOVE)
        content_frame.grid(column=0, row=2, columnspan=15, rowspan=15, padx=(5, 0))
        x_scrollbar = Scrollbar(content_frame, orient=HORIZONTAL)
        x_scrollbar.grid(row=1, column=0, sticky=E + W)
        self.csv_preview = Text(content_frame, wrap=NONE, bd=0, xscrollcommand=x_scrollbar.set, height=12, width=60)
        self.csv_preview.grid(row=0, column=0)
        x_scrollbar.config(command=self.csv_preview.xview)

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
        # A method that displays a preview of imported .csv file content and
        #  calculates all rows and columns in file.
        self.csv_preview.delete(1.0, END)
        content_to_display = "Preview: \n \n {} \n \n Total Columns:{} \n Total Rows: {}".format(
            df_data.head().to_string(),
            len(df_data.columns),
            len(df_data)
        )
        self.csv_preview.insert(INSERT, content_to_display)
        self.csv_preview.config(state=DISABLED)

    def create_database(self):
        # Creates a database from imported csv file with given name.
        if self.db_name.get() == '':
            messagebox.showerror("Empty name field", "Enter a valid database name.")
        else:
            # Creating a custom save directory
            chosen_directory = askdirectory(title='Choose Where To Export Database')
            file_path = "sqlite:///" + chosen_directory + "/" + self.db_name.get() + ".db"
            # Establishing connection with save directory and converting csv to db
            engine = create_engine(file_path)
            self.Base.metadata.create_all(engine)
            self.df_data.to_sql(self.db_name.get(), con=engine, index=True, if_exists='replace')
            info = "Database was converted and exported successfully! To review database use an appropriate" \
                   " database tool, such as SQLite Studio, HeidiSQL or MySQL Workbench."
            messagebox.showinfo(title='Converted Successfully!', message=info)


window = Tk()
Client(window)
window.mainloop()
