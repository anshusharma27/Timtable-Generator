import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import *
import tkinter.filedialog as filedialog
from reportlab.pdfgen import canvas
import pyautogui
import os
from reportlab.lib.pagesizes import landscape
import pygetwindow as gw

days = 5
periods = 8
fini = None
butt_grid = []


period_names = list(map(lambda x: str((8+x))+"-"+str((9+x)), range(1, 3+1))) + list(map(lambda x: "12-1", range(4, 5)))+list(map(lambda x: str((8+x)%12)+"-"+str((9+x)%12), range(5, 8+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']



def select_fac():
    global fini
    fini = str(combo1.get())
    print(fini)
    update_table(fini)



def update_table(fini):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SECTION, SUBCODE, ROOMNO FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND FINI='{fini}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subcode = cursor[0][1]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'black'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'white'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = 'light blue'

                sec_li = [x[0] for x in cursor]
                sec_2=[x[1] for x in cursor]
                room=[x[2] for x in cursor]
                n = ', '.join(sec_2)
                t = ', '.join(sec_li)
                r = ', '.join(room)
                butt_grid[i][j]['text'] = n + "\nSec: " + t + '\n' + r
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['text'] = "-"
                butt_grid[i][j].update()



def process_button(d, p):
    print(d, p, fini)
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SECTION, SUBCODE FROM SCHEDULE\
                WHERE DAYID={d} AND PERIODID={p} AND FINI='{fini}'")
    cursor = list(cursor)
    print("section", cursor)
    if len(cursor) != 0:
        sec_li = [x[0] for x in cursor]
        t = ', '.join(sec_li)
        subcode = cursor[0][1]
        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    #     print(subcode, fini, subname, subtype, fname, femail)
    else:
        sec_li = subcode = subname = subtype = t = 'None'

    tk.Label(details, text='Class Details', font=('Antique Olive', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+day_names[d], font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Period: '+str(p+1), font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: '+subname, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: '+fini, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Sections: '+t, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Antique Olive'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def fac_tt_frame(tt, f):
    title_lab = tk.Label(
        tt,
        text='T  I  M  E  T  A  B  L  E',
        font=('Antique Olive', 20, 'bold'),
        pady=5
    )
    title_lab.pack()

    legend_f = tk.Frame(tt)
    legend_f.pack(pady=15)
    tk.Label(
        legend_f,
        text='Legend: ',
        font=('Antique Olive', 10, 'italic')
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Theory Classes',
        bg='white',
        fg='black',
        relief='raised',
        font=('Antique Olive', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    tk.Label(
        legend_f,
        text='Practical Classes',
        bg='light blue',
        fg='black',
        relief='raised',
        font=('Antique Olive', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    global butt_grid
    global fini
    fini = f

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

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
                bb.grid(row=i+1, column=j+1)
            else:
                bb = tk.Button(second_half)
                bb.grid(row=i+1, column=j)

            bb.config(
                text='Hello World!',
                font=('Antique Olive', 10),
                width=13,
                height=3,
                bd=5,
                relief='raised',
                wraplength=80,
                justify='center',
                # command=lambda x=i, y=j: process_button(x, y)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(fini)

def save_as_pdf():
    window_title = "Faculty Timetable"  # Specify the title of your Tkinter window
    image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    # directory = 'd:\Project\Timetable\Timetable_pdf'
    # filename = 
    if image_path:
        directory, filename = os.path.split(image_path)
        filename = filename[:-4] + '.pdf'
        pdf_path = os.path.join(directory, filename)
        # print(directory, filename)
    # Find the window by title
    window = gw.getWindowsWithTitle(window_title)[0]
    
    # Get the window position and dimensions
    x, y = window.left, window.top
    width, height = window.width, window.height

    # Adjust the coordinates to exclude the top ribbon
    ribbon_height = 30  # Adjust this value according to your system's title bar height
    y += ribbon_height
    height -= ribbon_height

    # Take a screenshot of the Tkinter window without the top ribbon
    pyautogui.screenshot(image_path, region=(x, y, width, height-120))

    pdf_width = width  # Width in points (8.27 inches)
    pdf_height = height-120  # Height in points (11.69 inches)

    c = canvas.Canvas(pdf_path, pagesize=(pdf_width, pdf_height))
    c.drawImage(image_path, 0, 0, pdf_width, pdf_height)
    c.save()

conn = sqlite3.connect(r'files/timetable.db')
if __name__ == "__main__":
    
    # connecting database

    tt = tk.Tk()
    tt.title('Faculty Timetable')

    fac_tt_frame(tt, fini)

    fac_select_f = tk.Frame(tt, pady=15)
    fac_select_f.pack()

    tk.Label(
        fac_select_f,
        text='Select Faculty:  ',
        font=('Antique Olive', 12, 'bold')
    ).pack(side=tk.LEFT)

    cursor = conn.execute("SELECT DISTINCT INI FROM FACULTY")
    fac_li = [row[0] for row in cursor]
    print(fac_li)
    combo1 = ttk.Combobox(
        fac_select_f,
        values=fac_li,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    b = tk.Button(
        fac_select_f,
        text="OK",
        font=('Antique Olive', 12, 'bold'),
        padx=10,
        command=select_fac
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()

    save_button = tk.Button(tt, text="Save as PDF", command=save_as_pdf)
    save_button.pack()
    tt.state('zoomed')
    tt.mainloop()