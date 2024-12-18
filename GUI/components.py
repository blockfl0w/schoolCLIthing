import tkinter as tk
from tkinter import ttk


# create a custom widget for input fields renders a Entry widget with a label
class Input(tk.Frame):
    def __init__(self, master, label, show=None):
        super().__init__(master)
        self.label = ttk.Label(self, text=label, anchor=tk.W)
        self.entry = ttk.Entry(self, show=show if show else "")
        self.label.grid(column=0, row=0)
        self.entry.grid(column=0, row=1, pady=(5, 10))
        self.grid(column=0, row=0)


# A widget for shwoing errors in forms
class Infomation(tk.Frame):
    def __init__(self, master, label):
        super().__init__(master)

        # Create a label with the image as the background
        self.label = ttk.Label(
            self,
            text=label,
            anchor=tk.W,
            borderwidth=2,
            relief="solid",
        )
        self.label.grid(column=0, row=0, pady=10)

        self.grid(column=0, row=5)


# A Widget for all the buttons in the sidebar
class NavButton(tk.Frame):
    def __init__(self, master, text, command):
        super().__init__(master)
        self.button = tk.Button(
            self,
            text=text,
            command=command,
            font=("Arial", 12),
            justify="center",
            width="19",
            cursor="hand2",
            pady=10,
            border=0,
            background="#2e2e2e",
        )
        self.button.grid(column=0, row=0)
        self.grid(column=0, row=0)


# Widget for the sidebar
class Navigation(tk.Frame):
    def __init__(self, master, user, commands, currentFrame):
        super().__init__(master)

        self.config(width="200", background="#2e2e2e", height="600", padx=10)
        self.grid_propagate(False)

        self.homeButton = NavButton(
            self, text="Home", command=lambda: commands[0](currentFrame)
        )
        self.reportsButton = NavButton(
            self, text="New report", command=lambda: commands[1](currentFrame)
        )

        self.usersButton = NavButton(
            self, text="Users", command=lambda: commands[3](currentFrame)
        )
        self.teacherButton = NavButton(
            self, text="Teachers", command=lambda: commands[4](currentFrame)
        )

        self.accountButton = NavButton(
            self, text="Account", command=lambda: commands[2](currentFrame)
        )

        # Display admin buttons if the user is admin
        if user["role"] == "admin":
            self.homeButton.grid(row=0, column=0, pady=5)
            self.reportsButton.grid(row=1, column=0, pady=5)
            self.usersButton.grid(row=3, column=0, pady=5)
            self.teacherButton.grid(row=4, column=0, pady=5)
            self.accountButton.grid(row=2, column=0, pady=5)
        else:
            self.teacherButton.grid_forget()
            self.usersButton.grid_forget()
            self.homeButton.grid(row=0, column=0, pady=5)
            self.reportsButton.grid(row=1, column=0, pady=5)
            self.accountButton.grid(row=2, column=0, pady=5)

        self.grid(row=0, column=0, sticky="nsew")


# A preview for reports shows title and the teacher
class ReportPreview(tk.Frame):
    def __init__(self, master, report, collumn):
        super().__init__(master)

        self.config(
            background="#2e2e2e",
            padx=10,
            pady=10,
        )

        self.reportLabel = ttk.Label(
            self,
            text=report["name"],
            font=("Arial", 12, "bold"),
            background="#2e2e2e",
        )
        self.teacherLabel = ttk.Label(
            self,
            text=report["teacher"],
            font=("Arial", 10),
            foreground="#e0e0e0",
            background="#2e2e2e",
        )
        self.reportLabel.grid(column=0, row=0, pady=5)
        self.teacherLabel.grid(column=0, row=1, pady=5)

        # place the widget in the correct collumn and row so all content on screen
        if collumn < 7:
            self.grid(row=1, column=collumn, padx=10, pady=10)
        else:
            self.grid(row=2, column=collumn - 7, padx=10, pady=10)


# Preview for users shows the username
class UserPreview(tk.Frame):
    def __init__(self, master, user, collumn):
        super().__init__(master)

        self.config(
            background="#2e2e2e",
            padx=10,
            pady=10,
        )

        self.reportLabel = ttk.Label(
            self,
            text=user["username"],
            font=("Arial", 12, "bold"),
            background="#2e2e2e",
        )

        self.reportLabel.grid(column=0, row=0, pady=5)

        # place the widget in the correct collumn and row so all content on screen
        if collumn < 7:
            self.grid(row=1, column=collumn, padx=10, pady=10)
        else:
            self.grid(row=2, column=collumn - 7, padx=10, pady=10)


# Preview for teachers shows the name
class TeacherPreview(tk.Frame):
    def __init__(self, master, teacher, collumn):
        super().__init__(master)

        self.config(
            background="#2e2e2e",
            padx=10,
            pady=10,
        )

        self.reportLabel = ttk.Label(
            self, text=teacher, font=("Arial", 12, "bold"), background="#2e2e2e"
        )

        self.reportLabel.grid(column=0, row=0, pady=5)

        # place the widget in the correct collumn and row so all content on screen
        if collumn < 5:
            self.grid(row=1, column=collumn, padx=10, pady=10)
        else:
            self.grid(row=2, column=collumn - 5, padx=10, pady=10)
