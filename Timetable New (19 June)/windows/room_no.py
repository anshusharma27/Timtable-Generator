import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

# inputs in this window
room_no = room_type = None


# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('one', 'two')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=200, stretch=tk.NO)
    tree.column("two", width=200, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Room No.")
    tree.heading('two', text="Room Type")


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM ROOMS")
    for row in cursor:
        # print(row[0], row[1], row[2])
        if row[1] == 'LH':
            t = 'Lecture Hall'
        elif row[1] == 'CR':
            t = 'Classroom'
        elif row[1] == 'L':
            t = 'Lab'
        tree.insert(
            "",
            0,
            values=(row[0],t)
        )
    tree.place(x=500, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    room_no = str(room_no_entry.get())
    room_type = str(radio_var.get()).upper()

    if room_no=="":
        room_no = None

    if room_no is None :
        messagebox.showerror("Bad Input", "Please fill up Room No.")
        room_no_entry.delete(0, tk.END)
        return

    conn.execute(f"REPLACE INTO ROOMS (ROOM_NO, ROOM_TYPE)\
        VALUES ('{room_no}','{room_type}')")
    conn.commit()
    update_treeview()
    
    room_no_entry.delete(0, tk.END)


# update a row in the database
def update_data():
    room_no_entry.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one room at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        room_no_entry.insert(0, row[0])
        if row[1][0] == "LH":
            R1.select()
        elif row[1][0] == "CR":
            R2.select()
        elif row[1][0] == "L":
            R3.select()

        conn.execute(f"DELETE FROM ROOMS WHERE ROOM_NO = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a room from the list first!")
        return

# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a room from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM ROOMS WHERE ROOM_NO = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()



# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS ROOMS\
    (ROOM_NO CHAR(3) NOT NULL PRIMARY KEY,\
    ROOM_TYPE CHAR(2) NOT NULL)')

    # TKinter Window
    roomtk = tk.Tk()
    roomtk.geometry('1000x450')
    roomtk.title('Add/Update Rooms')

    # Label1
    tk.Label(
        roomtk,
        text='List of Rooms',
        font=('Consolas', 20, 'bold')
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        roomtk,
        text='Add/Update Rooms',
        font=('Consolas', 20, 'bold')
    ).place(x=100, y=50)

    # Label3
    tk.Label(
        roomtk,
        text='Add information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        roomtk,
        text='Room No.: ',
        font=('Consolas', 15)
    ).place(x=100, y=150)

    # Entry1
    room_no_entry = tk.Entry(
        roomtk,
        font=('Consolas', 15),
        width=11
    )
    room_no_entry.place(x=270, y=150)

    # Label5
    tk.Label(
        roomtk,
        text='Room Type:',
        font=('Consolas', 15)
    ).place(x=100, y=240)

    radio_var = tk.StringVar()

    # RadioButton1
    R1 = tk.Radiobutton(
        roomtk,
        text='Lecture Hall',
        font=('Consolas', 12),
        variable=radio_var,
        value="LH"
    )
    R1.place(x=270, y=240)
    R1.select()

    # RadioButton2
    R2 = tk.Radiobutton(
        roomtk,
        text='ClassRoom',
        font=('Consolas', 12),
        variable=radio_var,
        value="CR"
    )
    R2.place(x=270, y=270)
    R2.select()

    # RadioButton3
    R3 = tk.Radiobutton(
        roomtk,
        text='Lab',
        font=('Consolas', 12),
        variable=radio_var,
        value="L"
    )
    R3.place(x=270, y=300)
    R3.select()

    # Button1
    B1 = tk.Button(
        roomtk,
        text='Add Room',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=150,y=350)

    # Button2
    B2 = tk.Button(
        roomtk,
        text='Update Room',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=410,y=350)

    # Treeview1
    tree = ttk.Treeview(roomtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        roomtk,
        text='Delete Room(s)',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=650,y=350)

    # looping Tkiniter window
    roomtk.state('zoomed')
    roomtk.mainloop()
    conn.close() # close database ad=fter all operations