import bcrypt
import json
from components import Input, Infomation
from tkinter import ttk
import os


def createUser(username, password, role, userObj):
    """
    A simple function to create a new user and store it in the users.json file.

    args:
      username (str) The username of the user to be created.
      password (str) The password of the user to be created.
      role (str) The role of the user to be created.

    returns:
      - "200" if the user was created successfully.
      - "400" if the username is already taken.
    """

    # opens the file to read the contents
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()
    # The new user we are trying to create
    newUser = {}

    # check if the username is already taken
    for user in users:
        if user["username"] == username:
            return "400"

    # add info to the new user
    newUser["username"] = username
    newUser["role"] = role

    # Encrypt the password for sercurity
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    # store the passoword
    newUser["password"] = hashed.decode("utf-8", errors="strict")

    # add the new user to the list of users
    users.append(newUser)

    # wrtie the new list to the users.json file
    fileWrite = open("./data/users.json", "w")
    json.dump(users, fileWrite)

    file.close()

    userObj["username"] = newUser["username"]
    userObj["role"] = newUser["role"]

    return "200"


def loginUser(username, password, userObj):
    """
    A simple function to authenticate a user returns the username and role of the user if successful.

    args:
      username (str) The username of the user attempting to log in.
      password (str) The password of the user attempting to log in.
      user (dict) The user obj from main

    returns:
      str: A int indicating an error code:
        - 200 if the user is authenticated successfully.
        - 401 if the password is incorrect.
        - 404 if the username is not found.
        - 400 if an unexpected error occurs.
    """

    # opens the file to read the contents
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()

    loginStatus = 400
    # loop over the users
    for user in users:
        # if the entered username is the same as the username in the file
        if user["username"] == username:

            # check the password to see if it is the same as stored hashed password
            print(
                bcrypt.checkpw(
                    password.encode("utf-8"), user["password"].encode("utf-8")
                )
            )
            if bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            ):
                # return the users details if all info is correct
                userObj["username"] = user["username"]
                userObj["role"] = user["role"]

                # return succsess code
                loginStatus = 200
                return loginStatus
            else:
                # if not return 401
                loginStatus = 401
                return loginStatus
        else:
            # if user cant be found return 404
            loginStatus = 404
            continue

    # return 400 by default just in case
    return loginStatus


def handleAuth(callBack, username, password, formType, user, parent):
    """
    A function to handle the authentication of a user made so I can show errors.

    args:
        callBack (function) The function to call after the user is authenticated.
        username (str) The username of the user attempting to log in.
        password (str) The password of the user attempting to log in.
        formType (str) The type of form to create. Either "login" or "signUp".
        user (dict) The user object from main.
        parent (tk.Frame) The parent frame to place the form in.
    """
    if formType == "login":
        status = loginUser(username, password, user)
        print("Satus", status)
        if status == 200:
            callBack(parent)
        elif status == 401:
            Infomation(parent, "Incorrect password")
        elif status == 404:
            Infomation(parent, "User not found")
        else:
            Infomation(parent, "An unexpected error occured")
    else:
        status = createUser(username, password, "user", user)
        if status == "200":
            callBack(parent)
        else:
            Infomation(parent, "Username already taken")


def createAuthForm(parent, user, callBack, type="login" or "signUp"):
    """
    A function to create a login or sign up form.

    args:
        parent (tk.Frame) The parent frame to place the form in.
        user (dict) The user object from main.
        callBack (function) The function to call after the user is authenticated.
        type (str) The type of form to create. Either "login" or "signUp".
    """
    usernameEntry = Input(parent, "Username")
    passwordEntry = Input(parent, "Password", show="*")

    if type == "signUp":
        Infomation(
            parent,
            "Passwords should be at least 8 characters long and contain a capital letter, number and a special character.",
        )

    authButton = ttk.Button(
        parent,
        text=f"{'Sign Up' if type == 'signUp' else 'Login'}",
        command=lambda: (
            handleAuth(
                callBack,
                usernameEntry.entry.get(),
                passwordEntry.entry.get(),
                type,
                user,
                parent,
            )
        ),
    )

    usernameEntry.grid(row=0, column=0)
    passwordEntry.grid(row=1, column=0)
    authButton.grid(row=2, column=0)


def getUserReports(user, forceLoacal=False):
    """
    A function to get reports for a user. if the user is an admin it will return all reports.

    args:
        user (dict) The user object from main.
        forceLoacal (bool) A bool to force the function to return only the users reports incase they are admin.
    """
    file = open("./data/reports.json", "r")
    allReports = json.load(file)
    file.close()

    reports = []

    if user["role"] == "admin" and not forceLoacal:
        return allReports

    for report in allReports:
        if report["reporter"] == user["username"]:
            reports.append(report)

    return reports


def createReport(
    name, teacher, subject, room, stars, message, reporter, date, callBack, prev
):
    """
    A function to create a new report and store it in the reports.json file.

    args:
        name (str) The name of the student.
        teacher (str) The name of the teacher.
        subject (str) The subject the report is about.
        room (str) The room the teacher teaches in.
        stars (int) The number of stars the report has.
        message (str) The message of the report.
        reporter (str) The username of the reporter.
        date (str) The date the report was made.
        callBack (function) The function to call after the report is created.
        prev (tk.Frame) The previous frame to go back to.
    """
    file = open("./data/reports.json", "r")
    reports = json.load(file)
    file.close()

    newReport = {
        "name": name,
        "teacher": teacher,
        "subject": subject,
        "room": room,
        "stars": stars,
        "message": message,
        "reporter": reporter,
        "date": date,
    }

    reports.append(newReport)

    file = open("./data/reports.json", "w")
    json.dump(reports, file)
    file.close()

    callBack(prev, newReport)


def updateAccount(perviousUsername, newUsername, newPassword, userObj):
    """
    A function to update user data

    args:
        perviousUsername (str) The pervious username of the user.
        newUsername (str) The new username of the user.
        newPassword (str) The new password of the user.
        userObj (dict) The user object from main.
    """
    # Get contents from users file
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()

    # Loop over users and update the user with the pervious username
    for user in users:
        if user["username"] == perviousUsername:
            user["username"] = newUsername
            if newPassword != "":
                user["password"] = bcrypt.hashpw(
                    newPassword.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")

    # Write the updated users to the file
    file = open("./data/users.json", "w")
    json.dump(users, file)
    file.close()

    # Get contents from reports file
    file = open("./data/reports.json", "r")
    reports = json.load(file)
    file.close()

    for report in reports:
        if report["reporter"] == perviousUsername:
            report["reporter"] = newUsername

    # Write the updated reports to the file
    file = open("./data/reports.json", "w")
    json.dump(reports, file)
    file.close()

    userObj["username"] = newUsername


def signOut(user, callback):
    """
    A function to sign out the user

    args:
        user (dict) The user object from main
        callback (function) The function to call after the user is signed out.
    """
    user["username"] = ""
    user["role"] = ""

    print(type(callback))
    callback()


def deleteAccount(username, callback, pastFrame):
    """
    A simple function to delete a user from the users.json file.

    args:
        username (str) The username of the user to delete.
        callback (function) The function to call after the user is deleted.
    """

    # Get contents from users file
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()

    for user in users:
        if user["username"] == username:
            users.remove(user)

    # Write the updated users to the file
    file = open("./data/users.json", "w")
    json.dump(users, file)
    file.close()

    # Delete all reports from the user
    file = open("./data/reports.json", "r")
    reports = json.load(file)
    file.close()

    for report in reports:
        if report["reporter"] == username:
            reports.remove(report)

    file = open("./data/reports.json", "w")
    json.dump(reports, file)
    file.close()

    callback(pastFrame)


def getUsers():
    """
    A simple function to get all the users from the users.json file.

    returns array: A list of all the users.
    """
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()
    return users


def makeAdmin(username):
    """
    A simple function to make a user an admin.

    args:
        username (str) The username of the user to make an admin.
    """
    file = open("./data/users.json", "r")
    users = json.load(file)
    file.close()

    for user in users:
        if user["username"] == username:
            user["role"] = "admin"

    file = open("./data/users.json", "w")
    json.dump(users, file)
    file.close()


def getTeachersReports(teacher):
    """
    A simple function to get all the reports for a specific teacher.

    args:
        teacher (str) The name of the teacher to get the reports for.

    returns array: A list of all the reports for the teacher.
    """
    file = open("./data/reports.json", "r")
    reports = json.load(file)
    file.close()

    teacherReports = []

    for report in reports:
        if report["teacher"] == teacher:
            teacherReports.append(report)

    return teacherReports


def getTeachers():
    """
    A simple function to get all the teachers from the teachers.json file.

    returns array: A list of all the teachers.
    """
    file = open("./data/teachers.json", "r")
    teachers = json.load(file)
    file.close()
    return teachers


def setUpData():

    # Checks wether the data folder exists and creates it if not
    if not os.path.exists("./data"):
        os.makedirs("./data")

        # Create needed files into folder
        files = ["users.json", "reports.json", "teachers.json"]
        for file in files:
            with open(f"./data/{file}", "w") as f:
                if file == "teachers.json":
                    # Write the teachers to the file
                    f.write(
                        '["Aloysius Akpanobong","Shawn Appleyard","Dinika Paramalingam","Jessica Bassey","Jordan Veitch-McAllister","Fahim Uz Zaman","Corey VMcAllister","Susan Turnbull","William Ledwith","Holly Richardson","Murphy Bernard","Samantha Nixon"]'
                    )
                else:
                    f.write("[]")
