from tkinter import *
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import os
import csv
import matplotlib.pyplot as plt


def get_password():
    return ''.join([chr(ord(char) - 2) for char in 'pgyrcuuyqtf'])

# Function to connect to the database
def db_connect():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=get_password(),
            database="employee",
            auth_plugin='mysql_native_password'
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to insert data into the database
def insertData():
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()

    if not id.isdigit():
        messagebox.showwarning("Invalid Input", "Employee ID must be numeric!")
    elif id == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Insert", "All fields are required!")
    else:
        myDB = db_connect()
        if myDB:
            myCur = myDB.cursor()
            try:
                sql = "INSERT INTO empDetails (empID, empName, empDept) VALUES (%s, %s, %s)"
                val = (id, name, dept)
                myCur.execute(sql, val)
                myDB.commit()
                resetFields()
                show()
                messagebox.showinfo("Insert Status", "Data Inserted Successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Insert Error", f"Error: {err}")
            finally:
                myDB.close()

# Function to update data in the database
def updateData():
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()

    if not id.isdigit():
        messagebox.showwarning("Invalid Input", "Employee ID must be numeric!")
    elif id == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Update", "All fields are required!")
    else:
        myDB = db_connect()
        if myDB:
            myCur = myDB.cursor()
            try:
                sql = "UPDATE empDetails SET empName = %s, empDept = %s WHERE empID = %s"
                val = (name, dept, id)
                myCur.execute(sql, val)
                myDB.commit()
                resetFields()
                show()
                messagebox.showinfo("Update Status", "Data Updated Successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Update Error", f"Error: {err}")
            finally:
                myDB.close()

# Function to fetch data from the database
def getData():
    id = enterId.get()
    if not id.isdigit():
        messagebox.showwarning("Invalid Input", "Employee ID must be numeric!")
    elif id == "":
        messagebox.showwarning("Fetch Status", "Please provide the Emp ID to fetch the data:")
    else:
        myDB = db_connect()
        if myDB:
            myCur = myDB.cursor()
            try:
                sql = "SELECT * FROM empDetails WHERE empID = %s"
                val = (id,)
                myCur.execute(sql, val)
                rows = myCur.fetchall()
                enterName.delete(0, "end")
                enterDept.delete(0, "end")
                if rows:
                    for row in rows:
                        enterName.insert(0, row[1])
                        enterDept.insert(0, row[2])
                else:
                    messagebox.showinfo("Fetch Status", "No data found for the given Emp ID")
            except mysql.connector.Error as err:
                messagebox.showerror("Fetch Error", f"Error: {err}")
            finally:
                myDB.close()

# Function to delete data from the database
def deleteData():
    id = enterId.get()
    if not id.isdigit():
        messagebox.showwarning("Invalid Input", "Employee ID must be numeric!")
    elif id == "":
        messagebox.showwarning("Cannot Delete", "Please provide the Emp ID to delete the data")
    else:
        myDB = db_connect()
        if myDB:
            myCur = myDB.cursor()
            try:
                sql = "DELETE FROM empDetails WHERE empID = %s"
                val = (id,)
                myCur.execute(sql, val)
                myDB.commit()
                resetFields()
                show()
                messagebox.showinfo("Delete Status", "Data Deleted Successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Delete Error", f"Error: {err}")
            finally:
                myDB.close()

#Function to Search entry by name or department
def searchData():
    searchTerm = searchEntry.get()
    myDB = db_connect()
    if myDB:
        myCur = myDB.cursor()
        try:
            sql = "SELECT * FROM empDetails WHERE empName LIKE %s OR empDept LIKE %s"
            val = (f"%{searchTerm}%", f"%{searchTerm}%")
            myCur.execute(sql, val)
            rows = myCur.fetchall()
            showData.delete(0, END)
            showData.insert(0, "ID | Name | Dept")
            for row in rows:
                showData.insert(END, f"{row[0]:<10} {row[1]:<20} {row[2]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Search Error", f"Error: {err}")
        finally:
            myDB.close()

#Function for exporting data in a csv file 
def exportData():
    myDB = db_connect()
    if myDB:
        myCur = myDB.cursor()
        try:
            myCur.execute("SELECT * FROM empDetails")
            rows = myCur.fetchall()
            with open('employee_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Department"])
                writer.writerows(rows)
            messagebox.showinfo("Export Status", "Data exported successfully to 'employee_data.csv'")
        except mysql.connector.Error as err:
            messagebox.showerror("Export Error", f"Error: {err}")
        finally:
            myDB.close()

#Function for plotting the graph for distribution of employees by department
def show_distribution_by_department():
    myDB = db_connect()
    if myDB:
        myCur = myDB.cursor()
        try:
            sql = "SELECT empDept, COUNT(*) FROM empDetails GROUP BY empDept"
            myCur.execute(sql)
            rows = myCur.fetchall()
            departments = [row[0] for row in rows]
            counts = [row[1] for row in rows]

            plt.figure(figsize=(8, 5))
            plt.bar(departments, counts, color='skyblue')
            plt.title('Employee Distribution by Department')
            plt.xlabel('Department')
            plt.ylabel('Number of Employees')
            plt.show()
        except mysql.connector.Error as err:
            messagebox.showerror("Chart Error", f"Error: {err}")
        finally:
            myDB.close()            
# Function to display data in the listbox
def show():
    myDB = db_connect()
    if myDB:
        myCur = myDB.cursor()
        try:
            myCur.execute("SELECT * FROM empDetails")
            rows = myCur.fetchall()

            # Clear Treeview
            for item in empTable.get_children():
                empTable.delete(item)

            # Insert new rows into Treeview
            for row in rows:
                empTable.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Display Error", f"Error: {err}")
        finally:
            myDB.close()

# Function to reset entry fields
def resetFields():
    enterId.delete(0, "end")
    enterName.delete(0, "end")
    enterDept.delete(0, "end")

# GUI Setup
window = Tk()
window.geometry("900x400")
window.title("Employee CRUD App")

style = ttk.Style(window)
style.theme_use("clam")

empId = Label(window, text="Employee ID", font=('Serif', 12))
empId.place(x=20, y=30)
enterId = Entry(window)
enterId.place(x=150, y=30)

empName = Label(window, text="Employee Name", font=('Serif', 12))
empName.place(x=20, y=80)
enterName = Entry(window)
enterName.place(x=150, y=80)

empDept = Label(window, text="Employee Dept", font=("Serif", 12))
empDept.place(x=20, y=130)
enterDept = Entry(window)
enterDept.place(x=150, y=130)

searchLabel = Label(window, text="Search:", font=('Serif', 12))
searchLabel.place(x=20, y=250)
searchEntry = Entry(window)
searchEntry.place(x=100, y=250)
searchBtn = Button(window, text="Search", font=('Serif', 12), bg="lightblue", command=searchData)
searchBtn.place(x=260, y=240)

insertBtn = Button(window, text="Insert", font=('Serif', 12), bg="lightblue", command=insertData)
insertBtn.place(x=20, y=200)
updateBtn = Button(window, text="Update", font=('Serif', 12), bg="lightblue", command=updateData)
updateBtn.place(x=100, y=200)
getBtn = Button(window, text="Fetch", font=('Serif', 12), bg="lightblue", command=getData)
getBtn.place(x=180, y=200)
deleteBtn = Button(window, text="Delete", font=('Serif', 12), bg="lightblue", command=deleteData)
deleteBtn.place(x=260, y=200)
resetBtn = Button(window, text="Reset", font=('Serif', 12), bg="lightblue", command=resetFields)
resetBtn.place(x=280, y=350)

exportBtn = Button(window, text="Export", font=('Serif', 12), bg="lightblue", command=exportData)
exportBtn.place(x=20, y=280)

deptChartBtn = Button(window, text="Dept Distribution", font=('Serif', 12), bg="lightgreen", command=show_distribution_by_department)
deptChartBtn.place(x=20, y=320)

showData = Listbox(window, width=70)
showData.place(x=400, y=30, height=280)

columns = ("ID", "Name", "Department")
empTable = ttk.Treeview(window, columns=columns, show="headings", height=10)
empTable.heading("ID", text="ID")
empTable.heading("Name", text="Name")
empTable.heading("Department", text="Department")
empTable.column("ID", width=100, anchor="center")
empTable.column("Name", width=200, anchor="center")
empTable.column("Department", width=150, anchor="center")
empTable.place(x=350, y=30, width=500, height=350)

scrollbar = ttk.Scrollbar(window, orient="vertical", command=empTable.yview)
empTable.configure(yscroll=scrollbar.set)
scrollbar.place(x=850, y=30, height=350)

show()

window.mainloop()
