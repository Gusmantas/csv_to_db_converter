import sqlite3


class Database:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name + ".db")
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} "
            "(id INTEGER PRIMARY KEY, name text, level integer, power_level integer)".format(db_name))
        self.connect.commit()

    # def insert(self, name, level, power_level):
    #     self.cursor.execute("INSERT INTO characters VALUES (NULL, ?, ?, ?)", (name, level, power_level))
    #     self.connect.commit()
    #
    # def view(self):
    #     self.cursor.execute("SELECT * FROM characters")
    #     rows = self.cursor.fetchall()
    #     return rows

#
# database = Database("dragonball.db")
#
#
# def add_command():
#     database.insert(name_var.get(), level_var.get(), power_level_var.get())
#
#
# def view_command():
#     list_box.delete(0, END)
#     for row in database.view():
#         list_box.insert(END, row)
#
#
# window = Tk()
# name_label = Label(window, text="Name")
# name_label.grid(column=1, row=0)
# name_var = StringVar()
# name_entry = Entry(window, textvariable=name_var)
# name_entry.grid(column=2, row=0)
#
# level_label = Label(window, text="Level")
# level_label.grid(column=1, row=1)
# level_var = StringVar()
# level_entry = Entry(window, textvariable=level_var)
# level_entry.grid(column=2, row=1)
#
# power_level_label = Label(window, text="Power Level")
# power_level_label.grid(column=1, row=2)
# power_level_var = StringVar()
# power_level_entry = Entry(window, textvariable=power_level_var)
# power_level_entry.grid(column=2, row=2)
#
# add_button = Button(window, text="Add entry", width=12, command=add_command)
# add_button.grid(column=5, row=4)
#
# list_box = Listbox(window, height=6, width=35)
# list_box.grid(column=0, row=10)
#
# view_button = Button(window, text="View All", width=12, command=view_command)
# view_button.grid(column=4, row=12)
#
# window.mainloop()
