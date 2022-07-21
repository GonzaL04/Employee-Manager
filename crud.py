#Import library
from cProfile import label
from cgitb import text
from logging import root
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkinter.tix import Tree

from django.db import connection

#Graphical interphase development
root=Tk()
root.title("CRUD")
root.geometry("600x350")

myId = StringVar()
myName = StringVar()
myPosition = StringVar()
mySalary = StringVar()

def BBDDconnection():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()

    try:
        myCursor.execute("""CREATE TABLE employee 
        (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        NAME VARCHAR(50) NOT NULL, 
        POSITION VARCHAR(50) NOT NULL, 
        SALARY INT NOT NULL)
        """)
        messagebox.info("CONNECTION","Database created successfully")
    except:
        messagebox.showinfo("CONNECTION","Successfully connection with database")

def deleteBBDD():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()
    if messagebox.askyesno(message = "Data will be permanently lost, do you want to continue?", title = "WARNING"):
        myCursor.execute("DROP TABLE employee")
    else:
        pass
    cleanFields()
    show()


def exitApp():
    value = messagebox.askquestion("Exit", "Are you sure you want to exit the aplication?")
    if value == "yes":
        root.destroy()
    
def cleanFields():
    myId.set("")
    myName.set("")
    myPosition.set("")
    mySalary.set("")

def message():
    about = '''
    CRUD App
    Project by Gonzalo López
    Python Technology
    '''
    messagebox.showinfo(title = "INFORMATION", message = about)

######################################### Metodos CRUD ########################################

def create():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()

    try:
        date = myName.get(), myPosition.get(), mySalary.get()
        myCursor.execute("INSERT INTO employee VALUES(NULL,?,?,?)",(date))
        myConnection.commit()
    except:
        messagebox.showwarning("WARNING", "An error occurred while creating the record, check the connection with the database")
        pass
    cleanFields()
    show()

def show():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()
    register = tree.get_children()
    for element in register:
        tree.delete(element)

    try:
        myCursor.execute("SELECT * FROM employee")
        for row in myCursor:
            tree.insert("",0,text = row[0], values = (row[1],row[2],row[3]))    
    except:
        pass

###################################### TABLE ##############################################

tree = ttk.Treeview(height = 10, columns = ('#0','#1','#2'))
tree.place(x = 0, y = 130)
tree.column('#0', width = 100)
tree.heading('#0', text="ID", anchor = CENTER)
tree.heading('#1', text="Employee's name", anchor = CENTER)
tree.heading('#2', text="Position", anchor = CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Salary", anchor = CENTER)

def selectUsingClick (event):
    item = tree.identify('item', event.x, event.y)
    myId.set(tree.item(item, "text"))
    myName.set(tree.item(item, "values")[0])
    myPosition.set(tree.item(item, "values")[1])
    mySalary.set(tree.item(item, "values")[2])

tree.bind("<Double-1>", selectUsingClick)


def update():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()

    try:
        date = myName.get(), myPosition.get(), mySalary.get()
        myCursor.execute("UPDATE employee SET NAME=?, POSITION=?, SALARY=? WHERE ID="+myId.get(), (date))
        myConnection.commit()
    except:
        messagebox.showwarning("WARNING", "An error occurred while updating the record")
        pass
    cleanFields()
    show()

def delete():
    myConnection = sqlite3.connect("BBDD")
    myCursor = myConnection.cursor()
    try:
        if messagebox.askyesno(message = "Do you want delete the record?", title = "WARNING"):
            myCursor.execute("DELETE FROM employee WHERE ID="+myId.get())
            myConnection.commit()
    except:
        messagebox.showwarning("WARNING", "An error occurred while deleting the record")
        pass
    cleanFields()
    show()


########################################## PLACE WIDGETS IN VIEW #######################################
########################### CREATING MENUS ###############################

menubar = Menu(root)
menudatabase = Menu(menubar, tearoff = 0)
menudatabase.add_command(label="Create/Connect Database", command = BBDDconnection)
menudatabase.add_command(label="Delete Database", command = deleteBBDD)
menudatabase.add_command(label="Exit Database", command = exitApp)
menubar.add_cascade(label = "Start", menu = menudatabase)

helpMenu = Menu(menubar, tearoff = 0)
helpMenu.add_command(label="Reset Fields", command = cleanFields)
helpMenu.add_command(label="About", command = message)
menubar.add_cascade(label="Help", menu = helpMenu)

############################### CREATING LABELS AND TEXT BOXES #############################

i1 = Entry(root, textvariable = myId)

l2 = Label(root, text = "Name")
l2.place(x = 50,y = 10)
i2 = Entry(root, textvariable = myName, width = 50)
i2.place(x = 100, y = 10)

l3 = Label(root, text="Position")
l3.place(x = 50, y = 40)
i3 = Entry(root, textvariable = myPosition)
i3.place(x = 100, y = 40)

l4 = Label(root, text="Salary")
l4.place(x = 280, y = 40)
i4 = Entry(root, textvariable = mySalary, width = 10)
i4.place(x = 320, y = 40)

l5 = Label(root, text="USD")
l5.place(x = 380, y = 40)

##################################### CREATING BUTTONS ########################################

b1 = Button(root, text = "Create Record", command = create)
b1.place(x = 50, y = 90)
b2 = Button(root, text = "Update Record", command = update)
b2.place(x = 180, y = 90)
b3 = Button(root, text = "Show List", command = show)
b3.place(x = 320, y = 90)
b4 = Button(root, text = "Delete Record", bg = "#E32F2F", fg = "#242323", command = delete)
b4.place(x = 450, y = 90)

root.config(menu = menubar)

root.mainloop()