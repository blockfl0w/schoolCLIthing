from tkinter import ttk
import tkinter as tk

root = tk.Tk()

root.title("Reportr")


# login screen
def login():
    login_frame = ttk.Frame(root, padding="30 15 30 15")
    login_frame.grid(row=0, column=0, sticky="nsew")

    username = tk.StringVar()
    password = tk.StringVar()

    ttk.Label(login_frame, text="Username:").grid(row=0, column=0)
    ttk.Entry(login_frame, textvariable=username).grid(row=0, column=1)

    ttk.Label(login_frame, text="Password:").grid(row=1, column=0)
    ttk.Entry(login_frame, textvariable=password, show="*").grid(row=1, column=1)

    def submit():
        print("Username:", username.get())
        print("Password:", password.get())

    ttk.Button(login_frame, text="Login", command=submit).grid(row=2, column=0, columnspan=2)

    root.mainloop()
    
login()