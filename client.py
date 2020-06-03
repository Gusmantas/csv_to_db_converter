from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pandas.errors import EmptyDataError
import pandas as pd


class Client(object):
    """
    A class that creates a client with
    tkinter box that allows users to convert a csv file to a local database
    using sql alchemy and sqlite3 libraries.
    """

    def __init__(self, tk_window):
        self.window = tk_window
        tk_window.geometry("495x255")
        self.window.wm_title("CSV-to-Database converter")
        self.df_data = None
        # returns a metaclass, so that entities can inherit from it. After definition
        # database table and mapper will generate automatically
        self.Base = declarative_base()

        import_file_button = Button(tk_window, text="Import File", command=self.import_csv_file)
        import_file_button.grid(column=0, row=0, sticky=W, pady=(0, 10), padx=(5, 0))

        db_name_label = Label(tk_window, text="Database Name:")
        db_name_label.grid(column=6, row=0, pady=(0, 10))
        self.db_name = StringVar()
        self.db_name_field = Entry(tk_window, textvariable=self.db_name)
        self.db_name_field.grid(column=7, row=0, pady=(0, 10))

        self.convert_button = Button(tk_window, text="Convert File", command=self.create_database)
        self.convert_button.grid(column=14, row=0, columnspan=2, pady=(0, 10))
        # Button state is set to normal after csv file is chosen and can be converted to db
        self.convert_button["state"] = DISABLED

        # Adding a horizontal scrollbar to Text widget, where csv file content is displayed.
        # Wrapping it all in a Frame for better looks.
        content_frame = Frame(tk_window, bd=2, relief=SOLID)
        content_frame.grid(column=0, row=2, columnspan=15, rowspan=15, padx=(5, 0))
        x_scrollbar = Scrollbar(content_frame, orient=HORIZONTAL)
        x_scrollbar.grid(row=1, column=0, sticky=E + W)
        self.csv_preview = Text(content_frame, wrap=NONE, bd=0, xscrollcommand=x_scrollbar.set, height=12, width=60)
        self.csv_preview.grid(row=0, column=0)
        self.important_information = " " * 25 + "NOTE! \n" + \
                                     "- .csv file must be clean, without additional content.  \n" \
                                     "- make sure .csv file only includes columns and rows. \n" \
                                     "- specify a name for database before converting. \n" \
                                     "- to open .db file use software such as SQLite Studio.\n" \
                                     "- choose a .csv file to see a preview of it in this field.\n" \
                                     "- empty .csv files won't be converted"

        self.reset_preview_field(self.important_information)
        x_scrollbar.config(command=self.csv_preview.xview)

    def import_csv_file(self):
        # Method for importing .csv file, assigning it to pandas DataFrame. And displaying it to
        # Text widget using display_file_content method.
        try:
            csv_file_path = filedialog.askopenfilename(title="Select a .csv file", filetypes=(("CSV Files", "*.csv"),))
            self.df_data = pd.read_csv(csv_file_path)
            self.display_file_content(self.df_data)
            self.convert_button["state"] = NORMAL
            return self.df_data
        except FileExistsError:
            messagebox.showerror("File Do Not Exit", "Unable to find requested file. Please check if file exists.")
            self.reset_preview_field(self.important_information)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "File could not be opened. Choose a valid .csv type file.")
            self.reset_preview_field(self.important_information)
        except EmptyDataError:
            messagebox.showerror("Empty File", "No columns to parse from file")
            self.reset_preview_field(self.important_information)

    def display_file_content(self, df_data):
        # A method that displays a preview of imported .csv file content with
        #  total numbers of all rows and columns in file.
        content_to_display = "Preview: \n \n {} \n \n Total Columns:{} \n Total Rows: {}".format(
            df_data.head().to_string(),
            len(df_data.columns),
            len(df_data)
        )
        self.reset_preview_field(content_to_display)

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
            self.db_name_field.delete(0, END)
            self.reset_preview_field(self.important_information)
            self.convert_button['state'] = DISABLED
            info = "Database was converted successfully! To open database use an appropriate" \
                   " database managing tool, such as SQLite Studio, HeidiSQL or MySQL Workbench."
            messagebox.showinfo(title='Converted Successfully!', message=info)

    def reset_preview_field(self, content):
        # Method for resetting preview field and displaying another content in it.
        self.csv_preview.config(state=NORMAL)
        self.csv_preview.delete(1.0, END)
        self.csv_preview.insert(INSERT, content)
        self.csv_preview.config(state=DISABLED)


window = Tk()
Client(window)
window.mainloop()
