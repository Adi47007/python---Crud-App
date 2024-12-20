# python---Crud-App
Employee CRUD Application
This Python Project is a Graphical User Interface (GUI) Employee Management System built using tkinter and mysql.connector. It allows CRUD (Create, Read, Update, Delete) operations on employee data stored in a MySQL database. Below is a breakdown of its key features and functions:

Features
Database Connection:

Connects to a MySQL database using credentials retrieved from an obfuscated password function get_password.
Data Operations:

Insert: Add new employee records to the database.
Update: Modify existing employee details.
Fetch (Get): Retrieve details of a specific employee by their ID.
Delete: Remove an employee record from the database.
Search: Search for employees by name or department using a case-insensitive query.
Export: Save all employee data into a CSV file for offline use.
Distribution Chart: Plot a bar chart to visualize employee distribution by department using matplotlib.
GUI Elements:

Designed using tkinter widgets such as Label, Entry, Button, and Treeview.
Includes search fields, a listbox, and a treeview to display records.
Data Display:

Shows employee records dynamically in a Treeview widget and a search listbox for better visualization.
Functions Description
get_password: Retrieves the database password securely by decoding an obfuscated string.

db_connect: Establishes a connection to the MySQL database.

CRUD Operations:

insertData: Adds a new employee to the database.
updateData: Updates an employee's details.
getData: Fetches details of a specific employee by ID and displays them in input fields.
deleteData: Deletes an employee from the database by ID.
Search and Export:

searchData: Performs a search query on the database using the provided term.
exportData: Exports all employee records into a CSV file.
Visualization:

show_distribution_by_department: Generates a bar chart to analyze employee distribution across departments.
Utility Functions:

resetFields: Clears input fields.
show: Fetches and displays all employee records in the GUI.
GUI Layout:

Widgets for inputs (ID, name, department), buttons for operations, and a Treeview with a scrollbar for displaying database records.
Responsive to user actions like clicks, with visual feedback through messages.
Tools Used
Tkinter: For creating the GUI.
MySQL Connector: To interact with the database.
Matplotlib: For plotting bar charts.
CSV Module: To export data to CSV files.
This script provides a comprehensive way to manage and visualize employee data with a user-friendly interface.

<img width="678" alt="Result" src="https://github.com/user-attachments/assets/50ace4a4-d19b-46d5-a4de-881b5a3319d7" />
