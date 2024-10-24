import tkinter as tk
from tkinter import ttk

from helpers import createAuthForm, getUserReports

from components import Input, Infomation, NavButton, Navigation, ReportPreview

# modules that makes tkinter look good
import sv_ttk
import pywinstyles, sys
import darkdetect


def showLogin():
    wellcomeFrame.pack_forget()
    loginFrame.pack()


def showSignUp():
    wellcomeFrame.pack_forget()
    signUpFrame.pack()


def openMainWindow(pastFrame):
    pastFrame.pack_forget()

    nav = Navigation(
        mainWindowFrame,
        user,
        [showSignUp, showSignUp, showSignUp, showSignUp, showSignUp],
    )

    homeLabel = ttk.Label(contentFrame, text="Home", font=("Arial", 20, "bold"))

    recentReportsFrame = ttk.Frame(contentFrame)
    recentReports = ttk.Label(recentReportsFrame, text="Recent reports")

    userReports = getUserReports(user)

    print(userReports)
    for i in userReports:
        report = ReportPreview(recentReportsFrame, i, userReports.index(i))

    recentReports.grid(row=0, column=0)
    recentReportsFrame.grid(row=2, column=0)
    homeLabel.grid(row=0, column=0)
    contentFrame.grid(row=0, column=1, padx=10, pady=10)

    mainWindowFrame.pack()


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
wellcomeLabel = ttk.Label(wellcomeFrame, text="Wellcome to reportr")
wellcomeSubtext = ttk.Label(
    wellcomeFrame,
    text="To continue using repotr you will need to login with your account. If you do not have one you can create one for free.",
)

# Button for the users to select wether to login or create an account
loginButton = ttk.Button(wellcomeFrame, text="Login", command=showLogin)
createAccountButton = ttk.Button(
    wellcomeFrame, text="Create Account", command=showSignUp
)

wellcomeLabel.pack()
wellcomeSubtext.pack()

loginButton.pack()
createAccountButton.pack()
wellcomeFrame.pack()

# Main window
mainWindowFrame = ttk.Frame(root)

contentFrame = tk.Frame(mainWindowFrame, width=800, height=600)
contentFrame.grid_propagate(False)


# Sets the theme to dark
sv_ttk.set_theme(darkdetect.theme())
pywinstyles.change_header_color(
    root, "#141414" if sv_ttk.get_theme() == "dark" else "#141414"
)

root.mainloop()
