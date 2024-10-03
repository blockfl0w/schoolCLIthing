import cmd
import json
import datetime
import os
from getpass import getpass

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[96m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' # called to return to standard terminal text color

print(BLACK + "black" + RESET)
print(RED + "red" + RESET)
print(GREEN + "green" + RESET)
print(YELLOW + "yellow" + RESET)
print(BLUE + "blue" + RESET)
print(MAGENTA + "magenta" + RESET)
print(CYAN + "cyan" + RESET)
print(LIGHT_GRAY + "light gray" + RESET)
print(DARK_GRAY + "dark gray" + RESET)
print(BRIGHT_RED + "bright red" + RESET)
print(BRIGHT_GREEN + "bright green" + RESET)
print(BRIGHT_YELLOW + "bright yellow" + RESET)
print(BRIGHT_BLUE + "bright blue" + RESET)
print(BRIGHT_MAGENTA + "bright magenta" + RESET)
print(BRIGHT_CYAN + "bright cyan" + RESET)
print(WHITE + "white" + RESET)

logo = r"""
 ______   ______   ______  ______   ______  ______  ______    
/\  == \ /\  ___\ /\  == \/\  __ \ /\  == \/\__  _\/\  == \   
\ \  __< \ \  __\ \ \  _-/\ \ \/\ \\ \  __<\/_/\ \/\ \  __<   
 \ \_\ \_\\ \_____\\ \_\   \ \_____\\ \_\ \_\ \ \_\ \ \_\ \_\ 
  \/_/ /_/ \/_____/ \/_/    \/_____/ \/_/ /_/  \/_/  \/_/ /_/ 

"""

welcomeText = f"""\033[35m{logo}\033[97m
Welcome to \033[35mReportr\033[0m! A CLI tool for reporting teachers and their lesson from bad to good!
To get started type \033[96m'login'\033[0m to login to an account (or create one) or type \033[96m'help'\033[0m for help!
"""
username = ""
role = ""

def clearConsole():
  os.system('cls' if os.name == 'nt' else 'clear')
  
def printReport(data, user=False):
  clearConsole()
  print(f"Here are all reports made by {"all users" if user else "you"} \n")
  print(f"Name: {data['name']}")
  print(f"Teacher: {data['teacher']}")
  print(f"Subject: {data['subject']}")
  print(f"Room: {data['room']}")
  print(f"Date: {data['date']}")
  print(f"Rating: {data['rating']}/5")
  print(f"Review: {data['review']}")
  if user:
    print(f"Reviewer: {data['reviewer']}")
  print("\n")

def authenticateUser(usernameAttempt):
  file = open("./data/users.json", "r")
  users = json.load(file)
  
  for user in users:
    if user['username'] == usernameAttempt.strip():
      while True:
        password = getpass(prompt="Enter your password: ").strip()
        
        if user['password'] != password:
          print("\033[31mInvalid password!\033[0m")
          continue
        else:
          print("\033[32m" + user['username'] + ", you have been successfully logged in!\033[0m")
          global role
          role = user['role']
          global username
          username = user['username']
          return
  else:
    createAccount = input("would you like to create a new account? (Y/n)").lower()
    
    if createAccount == "" or createAccount == "y" or createAccount == "yes":
      password = getpass(prompt="Enter your password: ").strip()
      newUser = {}
      newUser['username'] = usernameAttempt
      newUser['password'] = password.strip()
      newUser['role'] = "user"
      
      users.append(newUser)
      
      file = open("./data/users.json", "w")
      json.dump(users, file)
      
      print("\033[32mAccount successfully created!\033[0m")
      
      role = user['role']
      username = user['username']

      file.close()
      return
    
  file.close()

def reportAdd():
  name = input("Enter a name for the report (leave blank to get an auto generated one): ")
  
  # if the users logged in ask if they want to submit anonymously
  if username != "":
    anonymous = input("Would you like to submit this report anonymously? (y/N): ").lower()
  else:
    anonymous = "n"

  teacher = input("What is the teacher's name: ")
  subject = input(f"What subject was {teacher} teaching?: ")
  room = input("What room was the class in?: ")
  period = input("What period did the class happen?: ")
  message = input("Enter a message for the report: ")
  rating = input("Enter a rating for the teacher (1-5): ")
  date = datetime.datetime.now().strftime("%Y-%m-%d")
  
  # auto generate a name if the user didn't enter one
  if name == "":
    name = f"Report for {teacher} at {date} by {"Anonymous" if anonymous == "y" or anonymous == "yes" else username}"
    
  # add data to a dictionary
  report = {}
  report['name'] = name
  report['reviewer'] = "Anonymous" if anonymous == "y" or anonymous == "yes" else username
  report['teacher'] = teacher
  report['date'] = date
  report['room'] = room
  report['period'] = period
  report['review'] = message
  report['rating'] = rating
  report['subject'] = subject
  
  # get contents of the reports file
  with open("./data/reports.json", "r") as file:
    reports = json.load(file)
    
  # add the new report to the past file
  reports.append(report)
  
  # rewrite the file with the new report
  with open("./data/reports.json", "w") as file:
    json.dump(reports, file)
  
  print("Report successfully added!")
  
  # ask the user if they want to quit for better UX
  quit = input("Would you like to quit? (Y/n)").lower()
  
  if quit == "y" or quit == "yes" or quit == "":
    exit()
    return
  
  
def reportView(args):
  if username == "":
    print("You must be logged in to view reports!")
    return
    
  if len(args) == 0 and role == "user":
    # view all reports for logged in user
    with open("./data/reports.json", "r") as file:
      reports = json.load(file)

      # filter reports by the logged in user 
      filteredReports = list(filter(lambda report: report['reviewer'] == username, reports))
      for i, report in enumerate(filteredReports):
        # clear the console for better UX
        printReport(report)
        
        if len(filteredReports) - (i + 1) != 0:
          prompt = input(f"Would you like to view the next report ({len(filteredReports) - (i + 1)} left)? (Y/n)").lower()
          if prompt == "n" or prompt == "no":
            break
        
  elif len(args) == 0 and role == "admin":
    # view all reports for admin
    with open("./data/reports.json", "r") as file:
      reports = json.load(file)
      print("Here are all reports made by all users \n")
      
      for i, report in enumerate(reports):
        printReport(report, user=True)
        
        if len(reports) - (i + 1) != 0:
          prompt = input(f"Would you like to view the next report ({len(reports) - (i + 1)} left)? (Y/n)").lower()
          if prompt == "n" or prompt == "no":
            break
          
        # clear the console for better UX
        clearConsole()
  elif len(args) != 0 and int(args[0]) >= 0:
    # added if clause to check admin or user in this check to cut down on code length
    if role == "user":
      with open("./data/reports.json", "r") as file:
        reports = json.load(file)
        report = reports[int(args[0])]
        try:
          if report['reviewer'] != username:
            print("You cannot view other user's reports!")
            return
          
          printReport(report)
        except IndexError:
          print("Invalid report ID!")
        finally:
          return
    if role == "admin":
      with open("./data/reports.json", "r") as file:
        reports = json.load(file)
        report = reports[int(args[0])]
        try:
          printReport(report, user=True) 
        except IndexError:
          print("Invalid report ID!")
        finally:
          return
        
def deleteReport(reports, report, account=False):
  conformation = input(f"Are you sure you want to delete this {"account" if account else "report"}? (Y/n)").lower()
  
  print(report)
  if conformation == "y" or conformation == "yes" or conformation == "":
    reports.remove(report)
    
    # rewrite the file with the new report
    if account:
      with open("./data/users.json", "w") as file:
        json.dump(reports, file)
    else:
      with open("./data/reports.json", "w") as file:
        json.dump(reports, file)
      
    print("'\033[32m'Report successfully deleted!\033[0m")
    return
  
def reportDelete(args):
  if username == "":
    print("You must be logged in to delete reports!")
    return
    
  if len(args) == 0 and role == "user":
    # delete all reports for logged in user
    with open("./data/reports.json", "r") as file:
      reports = json.load(file)

      # filter reports by the logged in user 
      filteredReports = list(filter(lambda report: report['reviewer'] == username, reports))
      for i, report in enumerate(filteredReports):
        # clear the console for better UX
        printReport(report)
        
        deleteReport(reports, report)
        
        if len(filteredReports) - (i + 1) != 0:
          prompt = input(f"Would you like to view the next report ({len(filteredReports) - (i + 1)} left)? (Y/n)").lower()
          if prompt == "n" or prompt == "no":
            break
          
        
  elif len(args) == 0 and role == "admin":
    # delete all reports for admin
    with open("./data/reports.json", "r") as file:
      reports = json.load(file)
      print("Here are all reports made by all users \n")
      
      for i, report in enumerate(reports):
        printReport(report, user=True)
        
        deleteReport(reports, report)
        
        if len(reports) - (i + 1) > 0:
          prompt = input(f"Would you like to view the next report ({len(reports) - (i + 1)} left)? (Y/n)").lower()
          if prompt == "n" or prompt == "no":
            break
          
          
  elif len(args) != 0 and int(args[0]) >= 0:
    # added if clause to check admin or user in this check to cut down on code length
    if role == "user":
      with open("./data/reports.json", "r") as file:
        reports = json.load(file)
        report = reports[int(args[0])]
        try:
          if report['reviewer'] != username:
            print("You cannot delete other user's reports!")
            return
          
          deleteReport(reports, report)
        except IndexError:
          print("Invalid report ID!")
        finally:
          return
  else:
    print("You have no reports to delete!")
  
class MyCLI(cmd.Cmd):
    prompt = '? '
    intro = welcomeText
      
    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World!")

    def do_login(self, line):
      """Login to reportr this allows you to view past reports!"""
      attemptUsername = input("Enter your username: ")
      
      authenticateUser(attemptUsername)
      
    def do_whoAmI(self, line):
      """Tells you who is currently logged in."""
      if username == "":
        print("You are not logged in!")
        return
      
      print("You are: " + username)
      print("Your role is: " + role)
      
    def do_reports(self, line):
      arguments = line.split(" ")
      
      msg = """Please enter a valid parameter! 
add - create a new report
view - view all reports
view \033[96m<report ID>\033[0m - to view a specific report
delete \033[96m<report ID>\033[0m - to delete a specific report"""
      
      if len(arguments) == 0:
        print(msg)
        return
      
      print()
      if arguments[0] == "add":
        reportAdd()
      elif arguments[0] == "view":
        arguments.remove(arguments[0])
        reportView(arguments)
      elif arguments[0] == "delete":
        arguments.remove(arguments[0])
        reportDelete(arguments)
      else:
        print(msg)
        
    def do_account(self, line):
      """View and manage your account"""
      args = line.split(" ")
      # args.remove(args[0])
      
      print(args)
      
      if len(args) == 0:
        print("Your account name is: " + username)
        print("Your account role is: " + role)
        
        with open("./data/reports.json", "r") as file:
          reports = json.load(file)

          # filter reports by the logged in user 
          filteredReports = list(filter(lambda report: report['reviewer'] == username, reports))
          
          print(f"You have made {len(filteredReports)} reports")
      elif args[0] == "delete":
        with open("./data/users.json", "r") as file:
          users = json.load(file)
          
          user = list(filter(lambda report: report['username'] == username, users))
          
          print(user)
          deleteReport(users, user[0], account=True)
      
    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':
    clearConsole()
    MyCLI().cmdloop()