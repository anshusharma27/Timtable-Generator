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
# recess_break_aft = 3 # recess after 3rd Period
section = None
butt_grid = []


period_names = list(map(lambda x: str((8+x))+"-"+str((9+x)), range(1, 3+1))) + list(map(lambda x: "12-1", range(4, 5)))+list(map(lambda x: str((8+x)%12)+"-"+str((9+x)%12), range(5, 8+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']



def select_sec():
    global section
    section = str(combo1.get())
    print('this',section)
    global sec1
    sec1 = section
    update_table(section)
    



def update_table(sec):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI, ROOMNO FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{sec}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subcode = cursor[0][0]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'black'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'white'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = 'light blue'

                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1]) + '\n' + str(cursor[0][2])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['bg'] = 'light grey'
                butt_grid[i][j]['text'] = "-"
                butt_grid[i][j].update()



def process_button(d, p, sec):
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SUBCODE, FINI, ROOMNO FROM SCHEDULE\
                WHERE ID='{section+str((d*periods)+p)}'")
    cursor = list(cursor)
    if len(cursor) != 0:
        subcode = str(cursor[0][0]) 
        fini =  str(cursor[0][1])
        room = str(cursor[0][2])

        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        cur2 = conn.execute(f"SELECT NAME, EMAIL FROM FACULTY\
            WHERE INI='{fini}'")
        cur2 = list(cur2)
        fname = str(cur2[0][0])
        femail = str(cur2[0][1]) 

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    else:
        subcode = fini = room = subname = subtype = fname = femail = 'None'

    print(subcode, fini, subname, subtype, fname, femail)
    tk.Label(details, text='Class Details', font=('Antique Olive', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+day_names[d], font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Period: '+str(p+1), font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: '+subname, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Room: '+room, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: '+fini, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Name: '+fname, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Email: '+femail, font=('Antique Olive'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Consolas'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def student_tt_frame(tt, sec):
    global butt_grid
    global section
    global sec1
    section = sec
    title_lab = tk.Label(
        tt,
        text='T  I  M  E  T  A  B  L  E' + '\n' + 'SEMESTER - 6',
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
        font=('Consolas', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

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
                # command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []
    print(butt_grid[0][1], butt_grid[1][1])
    update_table(sec)

def save_as_pdf():
    window_title = "Student Timetable"  # Specify the title of your Tkinter window
    image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    
    if image_path:
        directory, filename = os.path.split(image_path)
        filename = filename[:-4] + '.pdf'
        pdf_path = os.path.join(directory, filename)
        
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
    tt.title('Student Timetable')


    student_tt_frame(tt, section)

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
        command=select_sec
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()

    # Create a button to save as PDF
    save_button = tk.Button(tt, text="Save as PDF", command=save_as_pdf)
    save_button.pack()

    # screen_width = tt.winfo_screenwidth()
    # screen_height = tt.winfo_screenheight()

    # # Set the window width and height
    # window_width = screen_width
    # window_height = screen_height
    # tt.geometry(f"{window_width}x{window_height}")
    tt.state('zoomed')
    tt.mainloop()