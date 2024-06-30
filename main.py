import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Register")
        self.geometry("300x300")

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Email ID").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        register_button = tk.Button(self, text="Register", command=self.register)
        register_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.register_successful = False

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or not email or not password:
            messagebox.showinfo("Empty Fields", "Please fill all the fields before registering.")
            return

        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my@password1",
            database="contactmdb"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Username In Use",
                                "The username you entered is already in use. Please use a different username.")
            return

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Email In Use",
                                "The email you entered is already in use. Please use a different email.")
            return

        # Insert the username, email, and password into the database
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        conn.commit()

        cursor.close()
        conn.close()

        self.register_successful = True
        self.parent.destroy()  # Destroy the LoginWindow
        root.deiconify()

        self.destroy()

    def on_closing(self):
        if not self.register_successful:
            self.master.destroy()


class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Login")
        self.geometry("300x200")

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack()

        register_button = tk.Button(self, text="Register", command=self.open_register_window)
        register_button.pack()

        self.login_successful = False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showinfo("Empty Fields", "Please fill both the fields before logging in.")
            return

        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my@password1",
            database="contactmdb"
        )

        cursor = conn.cursor()

        # Check if the username and password match a record in the database
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        if cursor.fetchone() is None:
            messagebox.showinfo("Invalid Credentials",
                                "The username or password you entered did not match our records. Please double-check and try again.")
            return

        self.login_successful = True
        self.destroy()

        cursor.close()
        conn.close()

        self.destroy()

    def on_closing(self):
        if not self.login_successful:
            self.master.destroy()

    def open_register_window(self):
        self.withdraw()
        register_window = RegisterWindow(self)
        self.wait_window(register_window)

def center_window(root):
    window_width = 1000
    window_height = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

def add_contact():
    name = name_entry.get()
    contact = contact_entry.get()
    city = city_entry.get()

    if not name or not contact or not city:
        messagebox.showinfo("Empty Fields", "Please fill all the fields before adding a contact.")
        return

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my@password1",
        database="contactmdb"
    )

    cursor = conn.cursor()
    query = "INSERT INTO contacts (name, contact, city) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, contact, city))
    conn.commit()

    messagebox.showinfo("Contact Added", f"Name: {name}\nContact: {contact}\nCity: {city}")

    cursor.close()
    conn.close()

    # Empty the entry fields
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)

    view_contacts()

def view_contacts():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my@password1",
        database="contactmdb"
    )

    cursor = conn.cursor()
    query = "SELECT * FROM contacts"
    cursor.execute(query)

    rows = cursor.fetchall()

    # Clear the treeview
    for i in tree.get_children():
        tree.delete(i)

    # Insert new rows
    for row in rows:
        tree.insert('', 'end', values=row)

    cursor.close()
    conn.close()


def delete_contact():
    if not tree.selection():
        messagebox.showinfo("No Selection", "No contact selected to delete")
        return

    selected_contact = tree.item(tree.selection())['values']
    contact_id = selected_contact[0]

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my@password1",
        database="contactmdb"
    )

    cursor = conn.cursor()
    query = "DELETE FROM contacts WHERE id = %s"
    cursor.execute(query, (contact_id,))
    conn.commit()

    messagebox.showinfo("Contact Deleted", f"Deleted contact {contact_id}")

    cursor.close()
    conn.close()

    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)

    view_contacts()

def update_contact():
    if not tree.selection():
        messagebox.showinfo("No Selection", "No contact selected to update")
        return

    selected_contact = tree.item(tree.selection())['values']
    contact_id = selected_contact[0]

    new_name = name_entry.get()
    new_contact = contact_entry.get()
    new_city = city_entry.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my@password1",
        database="contactmdb"
    )

    cursor = conn.cursor()
    query = "UPDATE contacts SET name = %s, contact = %s, city = %s WHERE id = %s"
    cursor.execute(query, (new_name, new_contact, new_city, contact_id))
    conn.commit()

    messagebox.showinfo("Contact Updated", f"Updated contact {contact_id}")

    cursor.close()
    conn.close()

    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)

    view_contacts()

def fill_entries(event):
    if not tree.selection():
        return

    selected_contact = tree.item(tree.selection())['values']
    contact_id, name, contact, city = selected_contact

    # Clear the entry fields
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)

    # Fill the entry fields with the selected contact details
    name_entry.insert(0, name)
    contact_entry.insert(0, contact)
    city_entry.insert(0, city)



root = tk.Tk()
root.title("Contact Management System")
root.configure(bg="lightgrey")

center_window(root)

tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Contact Number").grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="City").grid(row=2, column=0, padx=10, pady=10)

name_entry = tk.Entry(root)
contact_entry = tk.Entry(root)
city_entry = tk.Entry(root)

name_entry.grid(row=0, column=1, padx=10, pady=10)
contact_entry.grid(row=1, column=1, padx=10, pady=10)
city_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text='Add Contact', command=add_contact).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
tk.Button(root, text='View Contacts', command=view_contacts).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
tk.Button(root, text='Delete Contact', command=delete_contact).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
tk.Button(root, text='Update Contact', command=update_contact).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Create a treeview widget
tree = ttk.Treeview(root, columns=('ID', 'Name', 'Contact', 'City'), show='headings')

# Set the column headings
tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Contact', text='Contact')
tree.heading('City', text='City')

tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
tree.bind('<<TreeviewSelect>>', fill_entries)

root.withdraw()

login_window = LoginWindow(root)
root.wait_window(login_window)

if login_window.login_successful:
    root.deiconify()
else:
    sys.exit()

root.deiconify()


root.mainloop()