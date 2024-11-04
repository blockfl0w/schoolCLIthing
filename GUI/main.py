import tkinter as tk
from tkinter import ttk

import datetime

# abstracted functions to a helper file
from helpers import (
    createAuthForm,
    getUserReports,
    createReport,
    updateAccount,
    signOut,
    deleteAccount,
    getUsers,
    makeAdmin,
    getTeachersReports,
    getTeachers,
    setUpData,
)

# Some custom widgets
from components import (
    Input,
    Navigation,
    ReportPreview,
    UserPreview,
    TeacherPreview,
)

# modules that makes tkinter look good
import sv_ttk
import darkdetect

# Make sure the data is set up
setUpData()


# Function to open the wellcome screen
def openWellcome(prev):
    # if there is a previous frame close it
    if prev != None:
        prev.grid_forget()

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


# Function to show the login form
def showLogin():
    wellcomeFrame.grid_forget()
    loginFrame.grid(column=0, row=0, sticky="nsew", pady=200)


# Function to show the sign up form
def showSignUp():
    wellcomeFrame.grid_forget()
    signUpFrame.grid(column=0, row=0)


# Function to open the home frame
def openMainWindow(pastFrame):
    pastFrame.grid_forget()

    print(user)
    # create the home frame
    homeFrame = ttk.Frame(contentFrame)
    contentFrame.columnconfigure(10, weight=1)

    # set current frame
    currentFrame = homeFrame

    # Reset navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    # the title of the home frame
    homeLabel = ttk.Label(homeFrame, text="Home", font=("Arial", 20, "bold"))

    # the frame for the recent reports
    recentReportsFrame = ttk.Frame(homeFrame)
    recentReports = ttk.Label(recentReportsFrame, text="Recent reports")

    # Get the reports for the current user
    userReports = getUserReports(user)

    # Loop through the reports and create a preview widget for each and bind a event so it opens the report when clicked
    for i in userReports:
        report = ReportPreview(recentReportsFrame, i, userReports.index(i))
        report.bind("<Button-1>", lambda e, i=i: openReport(homeFrame, i))

    # render all widgets in grid
    recentReports.grid(row=0, column=0)
    recentReportsFrame.grid(row=2, column=0)
    homeLabel.grid(row=0, column=0)
    homeFrame.grid(row=0, column=0)
    contentFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nesw", columnspan=10)

    mainWindowFrame.grid(row=0, column=0, sticky="nsew")


# Function to open the create report form
def openCreateReport(prev):
    # close the previous frame
    prev.grid_forget()

    createReportFrame = ttk.Frame(contentFrame)
    contentFrame.columnconfigure(0, weight=1)

    # Set the current frame so previous frames can be closed porperly
    currentFrame = createReportFrame

    # Reset the navigation so the user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
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


# function to show confomation to the user when a report is created
def reportSuccsess(prev, report):
    prev.grid_forget()
    reportSuccsessFrame = ttk.Frame(contentFrame)

    # set current frame so previous frames can be closed properly
    currentFrame = reportSuccsessFrame

    # reset navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    # The message shown when a report is created
    titleReport = ttk.Label(
        reportSuccsessFrame,
        text="Report created successfully",
        font=("Arial", 20, "bold"),
        justify="center",
    )

    # buttons to navigate to the home screen or view the report
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

    # render all widgets in grid
    titleReport.grid(row=0, column=0, columnspan=2, pady=10)
    homeButton.grid(row=1, column=0)
    viewReportButton.grid(row=1, column=1)
    reportSuccsessFrame.grid(row=0, column=0)


# function to open a report
def openReport(prev, report):
    # Close previous frame
    prev.grid_forget()

    reportFrame = ttk.Frame(contentFrame)

    # set the current frame so previous frames can be closed properly
    currentFrame = reportFrame

    # Makes sure that contents are centered horizontally
    contentFrame.columnconfigure(0, weight=1)

    # reset navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(
        reportFrame, text=report["name"], font=("Arial", 20, "bold"), justify="left"
    )
    # Who created the report and when
    credit = ttk.Label(
        reportFrame,
        text=f"By {report['reporter']} on {report['date']}",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )
    # Which teacher the report is about
    teacher = ttk.Label(
        reportFrame,
        text=f"Teacher: {report['teacher']}",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )
    # How many stars are associated with the report
    stars = ttk.Label(
        reportFrame,
        text=f"{report['stars']}/5",
        font=("Arial", 8, "bold"),
        foreground="#e0e0e0",
    )

    # The content of the report
    content = ttk.Label(
        reportFrame, text=report["message"], font=("Arial", 12), wraplength=800
    )

    # render all widgets in grid
    title.grid(row=0, column=0, columnspan=4)
    credit.grid(row=1, column=0, padx=10)
    teacher.grid(row=1, column=1, padx=10)
    stars.grid(row=1, column=2, padx=10)
    content.grid(row=2, column=0, columnspan=4, pady=10)
    reportFrame.grid(row=0, column=0)


# Function to open the account frame
def openAccount(prev):
    prev.grid_forget()

    accountFrame = ttk.Frame(contentFrame)

    # set the curent frame so previous frames can be closed properly
    currentFrame = accountFrame

    # reset the navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(accountFrame, text="Account", font=("Arial", 20, "bold"))

    # section to modify account details
    modifytitle = ttk.Label(
        accountFrame,
        text="Change account details",
        font=("Arial", 13, "bold"),
        justify="left",
    )
    usernameFrame = ttk.Frame(accountFrame)
    usernameLabel = ttk.Label(usernameFrame, text="Username")
    userNameInput = ttk.Entry(usernameFrame, textvariable=user["username"])

    passwordFrame = ttk.Frame(accountFrame)
    passwordLabel = ttk.Label(passwordFrame, text="Password")
    passwordInput = ttk.Entry(passwordFrame, text="Enter a password", show="*")

    # saves changes to the account
    saveButton = ttk.Button(
        accountFrame,
        text="Save",
        command=lambda: updateAccount(
            user["username"], userNameInput.get(), passwordInput.get(), user
        ),
    )

    # sign out and delete account buttons
    signOutLabel = ttk.Label(accountFrame, text="Sign out", font=("Arial", 13, "bold"))
    signOutButton = ttk.Button(
        accountFrame,
        text="Sign out",
        command=lambda: signOut(user, openWellcome(currentFrame)),
    )

    deleteAccountLabel = ttk.Label(
        accountFrame, text="Delete account", font=("Arial", 13, "bold")
    )
    deleteAccountButton = ttk.Button(
        accountFrame,
        text="Delete account",
        command=lambda: deleteAccount(user["username"], openWellcome, mainWindowFrame),
    )

    # render all widgets in grid
    title.grid(row=0, column=0, columnspan=2)
    modifytitle.grid(row=1, column=0, columnspan=2)
    usernameFrame.grid(row=2, column=0, pady=10)
    usernameLabel.grid(row=0, column=0, padx=10)
    userNameInput.grid(row=0, column=1)

    passwordFrame.grid(row=3, column=0, pady=10)
    passwordLabel.grid(row=0, column=0, padx=10)
    passwordInput.grid(row=0, column=1)

    saveButton.grid(row=4, column=0, columnspan=2, pady=10)

    signOutLabel.grid(row=2, column=1, pady=10, padx=20)
    signOutButton.grid(row=2, column=2, pady=10, padx=20)

    deleteAccountLabel.grid(row=3, column=1, pady=10, padx=20)
    deleteAccountButton.grid(row=3, column=2, pady=10, padx=20)
    accountFrame.grid(row=0, column=0)


# Function to open the users tab only available to admins
def openUsers(prev):
    prev.grid_forget()

    usersFrame = ttk.Frame(contentFrame)
    # set the current frame so previous frames can be closed properly
    currentFrame = usersFrame

    # reset the naviagtion so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(usersFrame, text="Users", font=("Arial", 20, "bold"))

    # Get all the users
    users = getUsers()

    # create a preview widget for each user and bind a event so it opens the user when clicked
    for i in users:
        userAccount = UserPreview(usersFrame, i, users.index(i))
        userAccount.bind("<Button-1>", lambda e, i=i: openUser(i, usersFrame))

    # render the widgets in grid
    title.grid(row=0, column=0)
    usersFrame.grid(row=0, column=0)


# opens a user profile of a different user only available to admins
def openUser(userPrev, prev):
    prev.grid_forget()

    userFrame = ttk.Frame(contentFrame)

    # set the current frame so previous frames can be closed properly
    currentFrame = userFrame

    # Makes sure that content are not all in one collumn
    contentFrame.columnconfigure(10, weight=1)

    # reset the navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(userFrame, text=userPrev["username"], font=("Arial", 20, "bold"))
    userInfoFrame = ttk.Frame(userFrame)
    # Shows the role of the user
    role = tk.Label(
        userInfoFrame,
        text=userPrev["role"],
        font=("Arial", 13, "bold"),
        background="red",
        foreground="white",
        padx=10,
        pady=10,
    )

    # Sets the background color of the role label to green if the user is an admin
    if userPrev["role"] == "admin":
        role.config(background="green")

    makeAdminButton = ttk.Button(
        userInfoFrame,
        text="Make admin",
        command=lambda: makeAdmin(userPrev["username"]),
    )

    # Get all the reports for the user
    reports = getUserReports(userPrev, True)
    reportsFrameUser = ttk.Frame(userFrame)

    # create a preview widget for each report and bind a event so it opens the report when clicked
    for i in reports:
        report = ReportPreview(reportsFrameUser, i, reports.index(i))
        report.bind("<Button-1>", lambda e, i=i: openReport(userFrame, i))

    # render all widgets in grid
    title.grid(row=0, column=0)
    role.grid(row=0, column=0)

    # only render make admin button if the user is not an admin
    if userPrev["role"] != "admin":
        makeAdminButton.grid(row=0, column=2)
    userInfoFrame.grid(row=1, column=0)
    reportsFrameUser.grid(row=2, column=0)
    userFrame.grid(row=0, column=0)


# Tab for admins to view reports based on teachers
def openTeachers(prev):
    prev.grid_forget()

    teachersFrame = ttk.Frame(contentFrame)
    # set the current frame so previous frames can be closed properly
    currentFrame = teachersFrame

    # makes sure all content is not in one column
    contentFrame.columnconfigure(10, weight=1)

    # reset the navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(teachersFrame, text="Teachers", font=("Arial", 20, "bold"))

    # Gets all the teachers
    teachers = getTeachers()

    teachersListFrame = ttk.Frame(teachersFrame)

    # Iterates over all the teachers and creates a clickable preview widget for each
    for i in teachers:
        teacher = TeacherPreview(teachersListFrame, i, teachers.index(i))
        teacher.bind("<Button-1>", lambda e, i=i: openTeacher(i, teachersFrame))

    # Render all the widgets in grid
    title.grid(row=0, column=0)
    teachersListFrame.grid(row=1, column=0)
    teachersFrame.grid(row=0, column=0)


# function to open a teacher profile
def openTeacher(teacher, prev):
    prev.grid_forget()

    teacherFrame = ttk.Frame(contentFrame)

    # set the current frame so previous frames can be closed properly
    currentFrame = teacherFrame

    # reset the navigation so user variable updates
    Navigation(
        mainWindowFrame,
        user,
        [openMainWindow, openCreateReport, openAccount, openUsers, openTeachers],
        currentFrame,
    )

    title = ttk.Label(teacherFrame, text=teacher, font=("Arial", 20, "bold"))

    # Get all the reports based on the teacher
    reports = getTeachersReports(teacher)

    teacherReportsFrame = ttk.Frame(teacherFrame)

    # create a preview widget for each report and bind a event so it opens the report when clicked
    for i in reports:
        report = ReportPreview(teacherReportsFrame, i, reports.index(i))
        report.bind("<Button-1>", lambda e, i=i: openReport(teacherFrame, i))

    # render all widgets in grid
    title.grid(row=0, column=0)
    teacherReportsFrame.grid(row=1, column=0)
    teacherFrame.grid(row=0, column=0)


# The current user
user = {
    "username": "",
    "role": "",
}

# The main window
root = tk.Tk()
root.geometry("1000x600")

# The frame for the sign up form
signUpFrame = tk.Frame(root)
signUpFrame.columnconfigure(0, weight=1)

# create the form for the signUp
createAuthForm(signUpFrame, user, openMainWindow, "signUp")

# The frame for the login form
loginFrame = tk.Frame(root)
loginFrame.columnconfigure(0, weight=1)


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


# Main window
mainWindowFrame = ttk.Frame(root)

# global variable to keep track of the current frame
global currentFrame

# The main content frame
contentFrame = tk.Frame(mainWindowFrame, width=800, height=600)
contentFrame.grid_propagate(False)


# Sets the theme to dark
sv_ttk.set_theme(darkdetect.theme())

# Prevent the window from being resized
root.resizable(False, False)

# Centers content by default
root.columnconfigure(0, weight=1)

# Open the wellcome screen
openWellcome(None)

# Start the main loop
root.mainloop()
