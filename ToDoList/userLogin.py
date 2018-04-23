#!/usr/bin/python3
import tkinter
from tkinter import*
from tkinter import messagebox
from userMainTaskPage import userTaskPageGUI

# ************* CLASS FOR USER LOGIN ***************** #
class userLoginGUI:

    def __init__(self):
        print("Construct login page #1")

        # Initiates tkinter object and frame
        self.root = tkinter.Tk()
        self.loginMainFrame = Frame(self.root, padx=10, pady=10)

        # Creates frames
        self.loginFrameTop = LabelFrame(self.loginMainFrame, padx=10, pady=10)
        self.loginFrameBottom = LabelFrame(self.loginMainFrame, padx=10, pady=10)

        # Add grid specifications for frames
        self.loginMainFrame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.loginFrameTop.grid(column=0, row=0, sticky=(N, S, E, W))
        self.loginFrameBottom.grid(column=0, row=1, sticky=(N, S, E, W))

        # Creates label, Entry and specifications for Username field
        self.usernameLabel = Label(self.loginFrameTop, text="Username:")
        self.usernameLabel.grid(column=0, row=0, sticky=(S, W), pady=10)
        self.usernameEntry = Entry(self.loginFrameTop)
        self.usernameEntry.grid(column=1, row=0, sticky=(S, E, W), pady=10, padx=5)

        # Creates label, Entry and specifications for Password field
        self.passwordLabel = Label(self.loginFrameTop, text="Password:")
        self.passwordLabel.grid(column=0, row=1, sticky=(S, W), pady=10)
        self.passwordEntry = Entry(self.loginFrameTop)
        self.passwordEntry.grid(column=1, row=1, sticky=(S, E, W), pady=10, padx=5)

        # Creates and pack Login button
        self.loginButton = Button(self.loginFrameBottom, text="Login", command=self.processLogin)
        self.loginButton.pack(fill=BOTH, expand=True)

        # Creates frame's tile and display integrated widgets
        self.root.title("Login")
        self.root.mainloop()

    def processLogin(self):
        print("processLogin clicked")
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        validation = 0

        try:
            fileDictionary = open("files/login.txt", "r+")
            readLine = fileDictionary.readline()

            # Checks if username and/or password is/are blank
            if ((username != "") and (password != "")):
                while readLine:
                    userDetails = readLine.split(" ")

                    if ((username == userDetails[0]) and (password == userDetails[1])):
                        validation = 1
                        # Close Login interface
                        self.root.destroy()
                        # Lunch/Display user's To-do list/task
                        userTaskPageGUI()
                        break
                    else:
                        #messagebox.showwarning("Login Error", "Invalid Username or Password")
                        print("Login Failed for some reason(s):...%s, %s", userDetails[0], userDetails[1])

                    readLine = fileDictionary.readline()

                # Checks if username and password passed are valid.
                if validation != 1:
                    messagebox.showwarning("Login Error", "Invalid Username or Password")

            else:
                messagebox.showwarning("Login Error", "Blank/Invalid Username or Password")

            # Close file
            fileDictionary.close()

        except FileNotFoundError:
            messagebox.showerror("File Error", "Login file cannot be open")
            print("File Error Cannot open this file)")

    # Description: Destroy/Delete object with print message
    def __del__(self):
        print("Destroyed", self.__class__.__name__)

# Main run application
#DisplayGUI = userLoginGUI()