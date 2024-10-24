import tkinter as tk
from tkinter import ttk

import datetime

from helpers import createAuthForm, getUserReports, createReport

from components import Input, Infomation, NavButton, Navigation, ReportPreview

# modules that makes tkinter look good
import sv_ttk
import pywinstyles, sys
import darkdetect


def showLogin():
    wellcomeFrame.grid_forget()
    loginFrame.grid(column=0, row=0, sticky="nsew")


def showSignUp():
    wellcomeFrame.grid_forget()
    signUpFrame.grid(column=0, row=0, sticky="nsew")


def openMainWindow(pastFrame):
    pastFrame.grid_forget()

    homeFrame = ttk.Frame(contentFrame)
    # set current frame
    currentFrame = homeFrame
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, showSignUp, showSignUp, showSignUp],
        currentFrame,
    )

    homeLabel = ttk.Label(homeFrame, text="Home", font=("Arial", 20, "bold"))

    recentReportsFrame = ttk.Frame(homeFrame)
    recentReports = ttk.Label(recentReportsFrame, text="Recent reports")

    userReports = getUserReports(user)

    for i in userReports:
        ReportPreview(recentReportsFrame, i, userReports.index(i))

    recentReports.grid(row=0, column=0)
    recentReportsFrame.grid(row=2, column=0)
    homeLabel.grid(row=0, column=0)
    homeFrame.grid(row=0, column=0)
    contentFrame.grid(row=0, column=1, padx=10, pady=10)

    mainWindowFrame.grid(row=0, column=0, sticky="nsew")


def openCreateReport(prev):
    # close the previous frame
    prev.grid_forget()

    createReportFrame = ttk.Frame(contentFrame)

    currentFrame = createReportFrame
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, showSignUp, showSignUp, showSignUp],
        currentFrame,
    )
    # all inputs needed to create a report
    name = Input(createReportFrame, "Name")
    teacher = Input(createReportFrame, "Teacher")
    subject = Input(createReportFrame, "Subject")
    room = Input(createReportFrame, "Room")
    stars = Input(createReportFrame, "Stars")
    message = Input(createReportFrame, "Message")
    date = datetime.date.today()

    # submit button
    submitButton = ttk.Button(
        createReportFrame,
        text="Submit",
        command=lambda: createReport(
            name.entry.get(),
            teacher.entry.get(),
            subject.entry.get(),
            room.entry.get(),
            stars.entry.get(),
            message.entry.get(),
            user["username"],
            date,
        ),
    )

    # display all relevant content
    name.grid(column=0, row=0)
    teacher.grid(column=0, row=1)
    subject.grid(column=0, row=2)
    room.grid(column=0, row=3)
    stars.grid(column=0, row=4)
    message.grid(column=0, row=5)
    submitButton.grid(column=0, row=6)
    createReportFrame.grid(column=2, row=0)
    mainWindowFrame.grid(column=0, row=0)


# The current user
user = {
    "username": "",
    "role": "",
}

# The main window
root = tk.Tk()
root.geometry("1000x600")

# The frame for the sign up form
signUpFrame = ttk.Frame(root)

# create the form for the signUp
createAuthForm(signUpFrame, user, openMainWindow, "signUp")

# The frame for the login form
loginFrame = ttk.Frame(root)

# create the form for the login
createAuthForm(loginFrame, user, openMainWindow, "login")

# A wellcome screen for the app
wellcomeFrame = ttk.Frame(root)

# Some wellcome text
wellcomeLabel = ttk.Label(
    wellcomeFrame, text="Wellcome to reportr", font=("Arial", 20, "bold")
)
wellcomeSubtext = ttk.Label(
    wellcomeFrame,
    text="To continue using repotr you will need to login with your account. If you do not have one you can create one for free.",
    foreground="#e0e0e0",
)

# container for buttons
buttonsFrame = ttk.Frame(wellcomeFrame)

# Button for the users to select wether to login or create an account
loginButton = ttk.Button(buttonsFrame, text="Login", command=showLogin)
createAccountButton = ttk.Button(
    buttonsFrame, text="Create Account", command=showSignUp
)

# render all widgets in grid
wellcomeLabel.grid(row=0, column=0, columnspan=2, pady=10)
wellcomeSubtext.grid(row=1, column=0, columnspan=2, pady=10)
buttonsFrame.grid(row=2, column=0, columnspan=2)
loginButton.grid(row=0, column=0, padx=10)
createAccountButton.grid(row=0, column=1, padx=10)
wellcomeFrame.grid(row=3, column=0, columnspan=2, pady=20)

# Main window
mainWindowFrame = ttk.Frame(root)

# global variable to keep track of the current frame
global currentFrame

# The main content frame
contentFrame = tk.Frame(mainWindowFrame, width=800, height=600)
contentFrame.grid_propagate(False)


# Sets the theme to dark
sv_ttk.set_theme(darkdetect.theme())
pywinstyles.change_header_color(
    root, "#141414" if sv_ttk.get_theme() == "dark" else "#141414"
)

# Prevent the window from being resized
root.resizable(False, False)

root.mainloop()
