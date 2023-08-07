import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
l=[1,2,3]
days = 5
periods = 8
# periods = 6
# recess_break_aft = 3 # recess after 3rd Period
section = None
butt_grid = []


period_names = list(map(lambda x: str((8+x))+"-"+str((9+x)), range(1, 3+1))) + list(map(lambda x: "12-1", range(4, 5)))+list(map(lambda x: str((8+x)%12)+"-"+str((9+x)%12), range(5, 8+1)))
# period_names = list(map(lambda x: 'Period ' + str(x), range(1, 6+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']


def update_p(d, p, tree, tree1,tree2, parent):
    # print(section, d, p, str(sub.get()))

    try:
        if len(tree.selection()) > 1 or len(tree1.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject and room at a time!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        row1 = tree1.item(tree1.selection()[0])['values']
        row2=tree2.item(tree2.selection()[0])['values']
        if row[0] == 'NULL' and row[1] == 'NULL' and row1[0] == 'NULL' and row2[0]=='NULL':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{section+str((d*periods)+p)}'")
            conn.commit()
            update_table()
            parent.destroy()
            return

        conn.commit()
        print(row)

        conn.execute(f"REPLACE INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI, ROOMNO, GID)\
            VALUES ('{section+str((d*periods)+p)}', {d}, {p}, '{row[1]}','{section}', '{row[0]}', '{row1[0]}', {row2[0]})")
        
        # conn.execute(f"REPLACE INTO SCHEDULE1 (ROOMNO))\
        #     VALUES ('{row1[0]}')")
        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select all entries from the list!")
        parent.destroy()
        return

    parent.destroy()



def process_button(d, p):
    print(d, p)
    add_p = tk.Tk()
    # add_p.geometry('200x500')

    # get subject code list from the database
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        add_p,
        text='Select Subject and Room',
        font=('Antique Olive', 12, 'bold')
    ).pack()

    tk.Label(
        add_p,
        text=f'Day: {day_names[d]}',
        font=('Antique Olive', 12)
    ).pack()

    tk.Label(
        add_p,
        text=f'Period: {p+1}',
        font=('Antique Olive', 12)
    ).pack()
   
    tree = ttk.Treeview(add_p)
    tree.pack(side='left')
    tree1 = ttk.Treeview(add_p)
    tree1.pack(side='left')
    tree2=ttk.Treeview(add_p)
    tree2.pack(side='left')
    tree['columns'] = ('one', 'two')
    tree1['columns'] = ('one', 'two')
    tree2['columns'] = ('one')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Faculty")
    tree.heading('two', text="Subject Code")
    tree1.column("#0", width=0, stretch=tk.NO)
    tree1.column("one", width=70, stretch=tk.NO)
    tree1.column("two", width=80, stretch=tk.NO)
    tree1.heading('#0', text="")
    tree1.heading('one', text="Room No.")
    tree1.heading('two', text="Room Type")
    tree2.column("#0", width=0, stretch=tk.NO)
    tree2.column("one", width=70, stretch=tk.NO)
    tree2.heading('#0', text="")
    tree2.heading('one', text="Group No.")
    
    cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBCODE\
    FROM FACULTY, SUBJECTS\
    WHERE FACULTY.SUBCODE1=SUBJECTS.SUBCODE OR FACULTY.SUBCODE2=SUBJECTS.SUBCODE")
    for row in cursor:
        print(row)
        tree.insert(
            "",
            0,
            values=(row[0],row[-1])
        )
    tree.insert("", 0, value=('NULL', 'NULL'))
    tree.pack(pady=10, padx=30)
    
    cursor = conn.execute("SELECT *\
    FROM ROOMS")
    for row in cursor:
        print(row)
        tree1.insert(
            "",
            0,
            values=(row[0],row[-1])
        )
    tree1.insert("", 0, value=('NULL', 'NULL'))
    tree1.pack(pady=10, padx=30)
    
    
    for i in l:
        print(i)
        tree2.insert(
            "",
            0,
            values=i)
    tree2.insert("", 0, value=('NULL'))
    tree2.pack(pady=10, padx=30)
    
    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, w=tree1, q=tree2, d=add_p: update_p(x, y, z, w, q, d)
    ).pack(pady=20)

    add_p.mainloop()


def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table()


def update_table():
    l=[1,2,3]
    for i in range(days):
        for j in range(periods):
     
                cursor = conn.execute(f"SELECT SUBCODE, FINI, ROOMNO,GID FROM SCHEDULE\
                    WHERE DAYID={i} AND PERIODID={j} AND SECTION='{section}' ")
                cursor = list(cursor)
                print(cursor)
#                 if cursor[0][3]=='NULL':
                if len(cursor) != 0:
                        
                        if str(cursor[0][3])!='NULL'and str(cursor[0][3])!='None' :
                            butt_grid[i][j]['text'] = str(cursor[0][0]) + '(G' + str(cursor[0][3]) + ')' + '\n' + str(cursor[0][1]) + '\n' + str(cursor[0][2]) 
                        else:
                            butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1]) + '\n' + str(cursor[0][2]) 
                        butt_grid[i][j].update()
                        print(i, j, cursor[0][0])
                        
                else:
                            butt_grid[i][j]['text'] = "-"
                            butt_grid[i][j].update()
#                 else:
                    
#                     if len(cursor) != 0:
#                         butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1]) + '\n' + str(cursor[0][2]) 
#                         butt_grid[i][j].update()
#                         print(i, j, cursor[0][0])
#                     else:
#                         butt_grid[i][j]['text'] = "-"
#                         butt_grid[i][j].update()
                    

# connecting database
conn = sqlite3.connect(r'files/timetable.db')

conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
(ID CHAR(10) NOT NULL PRIMARY KEY,\
DAYID INT NOT NULL,\
GID INT ,\
PERIODID INT NOT NULL,\
SUBCODE CHAR(10) NOT NULL,\
ROOMNO CHAR(3) NOT NULL,\
SECTION CHAR(5) NOT NULL,\
FINI CHAR(10) NOT NULL)')
# creating Tabe in the database
# conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
# (ID CHAR(10) NOT NULL PRIMARY KEY,\
# DAYID INT NOT NULL,\
# PERIODID INT NOT NULL,\
# SUBCODE CHAR(10) NOT NULL,\
# SECTION CHAR(5) NOT NULL,\
# FINI CHAR(10) NOT NULL)')
# DAYID AND PERIODID ARE ZERO INDEXED


tt = tk.Tk()

tt.title('Scheduler')

title_lab = tk.Label(
    tt,
    text='T  I  M  E  T  A  B  L  E',
    font=('Antique Olive', 20, 'bold'),
    pady=5
)
title_lab.pack()


table = tk.Frame(tt)
table.pack()

first_half = tk.Frame(table)
first_half.pack(side='left')

# recess_frame = tk.Frame(table)
# recess_frame.pack(side='left')

second_half = tk.Frame(table)
second_half.pack(side='left')


for i in range(days):
    b = tk.Label(
        first_half,
        text=day_names[i],
        font=('Antique Olive', 12, 'bold'),
        width=9,
        height=2,
        bd=5,
        relief='raised'
    )
    b.grid(row=i+1, column=0)

for i in range(periods):
    if i < 5:
        b = tk.Label(first_half)
        b.grid(row=0, column=i+1)
    else:
        b = tk.Label(second_half)
        b.grid(row=0, column=i)

    b.config(
        text=period_names[i],
        font=('Antique Olive', 12, 'bold'),
        width=9,
        height=1,
        bd=5,
        relief='raised'
    )

for i in range(days):
    b = []
    for j in range(periods):
        if j < 5:
            bb = tk.Button(first_half)
            bb.grid(row = 0, column=0)

            bb.config(
            text='Hello World!',
            font=('Antique Olive', 10),
            width=13,
            height=1,
            bd=5,
            relief='raised',
            wraplength=80,
            justify='center',
            command=lambda x=0, y=0: process_button(0, 0)
        )
            bb.grid(row=i+1, column=j+1)
        else:
            bb = tk.Button(second_half)
            bb.grid(row=i+1, column=j)

        bb.config(
            # text='Hello World!',
            font=('Antique Olive', 10),
            width=13,
            height=3,
            bd=5,
            relief='raised',
            wraplength=80,
            justify='center',
            command=lambda x=i, y=j: process_button(x, y)
        )
        b.append(bb)

    # bb1 = tk.Button(first_half)
    # bb1.grid(row=1, column=1)
    # bb1.config(
    #         text='Hello World!',
    #         font=('Antique Olive', 10),
    #         width=13,
    #         height=1,
    #         bd=5,
    #         relief='raised',
    #         wraplength=80,
    #         justify='center',
    #         command=lambda x=0, y=0: process_button(0, 0)
    # )
    # b[0] = bb1

    butt_grid.append(b)
    # print(b)
    b = []
sec_select_f = tk.Frame(tt, pady=15)
sec_select_f.pack()

tk.Label(
    sec_select_f,
    text='Select section:  ',
    font=('Antique Olive', 12, 'bold')
).pack(side=tk.LEFT)

cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
sec_li = [row[0] for row in cursor]
# sec_li.insert(0, 'NULL')
print(sec_li)
combo1 = ttk.Combobox(
    sec_select_f,
    values=sec_li,
)
combo1.pack(side=tk.LEFT)
combo1.current(0)

b = tk.Button(
    sec_select_f,
    text="OK",
    font=('Antique Olive', 12, 'bold'),
    padx=10,
    command=select_sec,
    # height= 40
)
b.pack(side=tk.LEFT, padx=10)
b.invoke()


print(butt_grid[0][1], butt_grid[1][1])
update_table()

tt.state('zoomed')
tt.mainloop()