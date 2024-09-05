from tkinter import *
from tkinter import messagebox
import mysql.connector


def get_password():
    return ''.join([chr(ord(char) - 2) for char in 'pgyrcuuyqtf'])




def insertData():
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()
    
    if id == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Insert", "All fields are required!")
    else:
        myDB = mysql.connector.connect(host="localhost", user="root", passwd=get_password(), database="employee")
        myCur = myDB.cursor()
        sql = "INSERT INTO empDetails (empID, empName, empDept) VALUES (%s, %s, %s)"
        val = (id, name, dept)
        myCur.execute(sql, val)
        myDB.commit()
        enterId.delete(0, "end")
        enterName.delete(0, "end")
        enterDept.delete(0, "end")
        show()
        messagebox.showinfo("Insert Status", "Data Inserted Successfully")
        myDB.close()

def updateData():
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()
    
    if id == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Update", "All fields are required!")
    else:
        myDB = mysql.connector.connect(host="localhost", user="root", passwd=get_password(), database="employee")
        myCur = myDB.cursor()
        sql = "UPDATE empDetails SET empName = %s, empDept = %s WHERE empID = %s"
        val = (name, dept, id)
        myCur.execute(sql, val)
        myDB.commit()
        enterId.delete(0, "end")
        enterName.delete(0, "end")
        enterDept.delete(0, "end")
        show()
        messagebox.showinfo("Update Status", "Data Updated Successfully")
        myDB.close()

def getData():
    if enterId.get() == "":
        messagebox.showwarning("Fetch Status", "Please provide the Emp ID to fetch the data:")
    else:
        myDB = mysql.connector.connect(host="localhost", user="root", passwd=get_password(), database="employee")
        myCur = myDB.cursor()
        sql = "SELECT * FROM empDetails WHERE empID = %s"
        val = (enterId.get(),)
        myCur.execute(sql, val)
        rows = myCur.fetchall()
        if rows:
            enterName.delete(0, "end")
            enterDept.delete(0, "end")
            for row in rows:
                enterName.insert(0, row[1])
                enterDept.insert(0, row[2])
        else:
            messagebox.showinfo("Fetch Status", "No data found for the given Emp ID")
        myDB.close()

def deleteData():
    if enterId.get() == "":
        messagebox.showwarning("Cannot Delete", "Please provide the Emp ID to delete the data")
    else:
        myDB = mysql.connector.connect(host="localhost", user="root", passwd=get_password(), database="employee")
        myCur = myDB.cursor()
        sql = "DELETE FROM empDetails WHERE empID = %s"
        val = (enterId.get(),)
        myCur.execute(sql, val)
        myDB.commit()
        enterId.delete(0, "end")
        enterName.delete(0, "end")
        enterDept.delete(0, "end")
        show()
        messagebox.showinfo("Delete Status", "Data Deleted Successfully")
        myDB.close()

def show():
    myDB = mysql.connector.connect(host="localhost", user="root", passwd=get_password(), database="employee")
    myCur = myDB.cursor()
    myCur.execute("SELECT * FROM empDetails")
    rows = myCur.fetchall()
    showData.delete(0, showData.size())
    for row in rows:
        addData = str(row[0]) + ' ' + row[1] + ' ' + row[2]  # Convert row[0] to string
        showData.insert(showData.size() + 1, addData)
    myDB.close()


def resetFields():
    enterId.delete(0, "end")
    enterName.delete(0, "end")
    enterDept.delete(0, "end")

window = Tk()
window.geometry("600x270")
window.title("Employee CRUD App")

empId = Label(window, text="Employee ID", font=('Serif', 12))
empId.place(x=20, y=30)
empName = Label(window, text="Employee Name", font=('Serif', 12))
empName.place(x=20, y=60)
empDept = Label(window, text="Employee Dept", font=("Serif", 12))
empDept.place(x=20, y=90)
enterId = Entry(window)
enterId.place(x=170, y=30)
enterName = Entry(window)
enterName.place(x=170, y=60)
enterDept = Entry(window)
enterDept.place(x=170, y=90)

insertBtn = Button(window, text="Insert", font=('Serif', 12), bg="white", command=insertData)
insertBtn.place(x=20, y=160)
updateBtn = Button(window, text="Update", font=('Serif', 12), bg="white", command=updateData)
updateBtn.place(x=80, y=160)
getBtn = Button(window, text="Fetch", font=('Serif', 12), bg="white", command=getData)
getBtn.place(x=150, y=160)
deleteBtn = Button(window, text="Delete", font=('Serif', 12), bg="white", command=deleteData)
deleteBtn.place(x=210, y=160)
resetBtn = Button(window, text="Reset", font=('Serif', 12), bg="white", command=resetFields)
resetBtn.place(x=20, y=210)

showData = Listbox(window)
showData.place(x=330, y=30)

show()

window.mainloop()
