import tkinter
from tkinter import ttk

from components import Input, Infomation

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


# The main window
root = tkinter.Tk()

# The frame for the sign up form
signUpFrame = ttk.Frame(root)

usernameEntry = Input(signUpFrame, "Username")
passwordEntry = Input(signUpFrame, "Password")
infomationLabel = Infomation(
    signUpFrame,
    "Passwords should be at least 8 characters long and contain a capital letter, number and a special character.",
)

signUpButton = ttk.Button(signUpFrame, text="Sign Up")

usernameEntry.pack()
passwordEntry.pack()
signUpButton.pack()

# The frame for the login form
loginFrame = ttk.Frame(root)

# Add the inputs for login
usernameEntry = Input(loginFrame, "Username")
passwordEntry = Input(loginFrame, "Password")

submitButton = ttk.Button(loginFrame, text="Login")

usernameEntry.pack()
passwordEntry.pack()
submitButton.pack()

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


# Sets the theme to dark
sv_ttk.set_theme(darkdetect.theme())
pywinstyles.change_header_color(
    root, "#141414" if sv_ttk.get_theme() == "dark" else "#141414"
)

root.mainloop()
