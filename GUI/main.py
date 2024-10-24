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
        report = ReportPreview(recentReportsFrame, i, userReports.index(i))
        report.bind("<Button-1>", lambda e, i=i: openReport(homeFrame, i))

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
    date = datetime.date.today().strftime("%d/%m/%Y")

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
            reportSuccsess,
            currentFrame,
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


def reportSuccsess(prev, report):
    prev.grid_forget()

    reportSuccsessFrame = ttk.Frame(contentFrame)
    currentFrame = reportSuccsessFrame
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, showSignUp, showSignUp, showSignUp],
        currentFrame,
    )

    titleReport = ttk.Label(
        reportSuccsessFrame,
        text="Report created successfully",
        font=("Arial", 20, "bold"),
        justify="center",
    )

    homeButton = ttk.Button(
        reportSuccsessFrame,
        text="Home",
        command=lambda: openMainWindow(reportSuccsessFrame),
    )
    viewReportButton = ttk.Button(
        reportSuccsessFrame,
        text="View report",
        command=lambda: openReport(reportSuccsessFrame, report),
    )

    titleReport.grid(row=0, column=0, columnspan=2)
    homeButton.grid(row=1, column=0)
    viewReportButton.grid(row=1, column=1)
    reportSuccsessFrame.grid(row=0, column=0)


def openReport(prev, report):
    prev.grid_forget()

    reportFrame = ttk.Frame(contentFrame)
    currentFrame = reportFrame
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, showSignUp, showSignUp, showSignUp],
        currentFrame,
    )

    title = ttk.Label(
        reportFrame, text=report["name"], font=("Arial", 20, "bold"), justify="left"
    )
    credit = ttk.Label(
        reportFrame,
        text=f"By {report['reporter']} on {report['date']}",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )
    teacher = ttk.Label(
        reportFrame,
        text=f"Teacher: {report['teacher']}",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )
    stars = ttk.Label(
        reportFrame,
        text=f"{report['stars']}/5",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )

    content = ttk.Label(
        reportFrame, text=report["message"], font=("Arial", 12), wraplength=800
    )

    title.grid(row=0, column=0, columnspan=4)
    credit.grid(row=1, column=0, padx=10)
    teacher.grid(row=1, column=1, padx=10)
    stars.grid(row=1, column=2, padx=10)
    content.grid(row=2, column=0, columnspan=4, pady=10)
    reportFrame.grid(row=0, column=0)


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
