#!/usr/bin/python3
import tkinter
from tkinter import*
from tkinter import messagebox
from userAddTaskPage import userAddAndEditTaskGUI, viewTaskDetailsGUI

# ************* CLASS FOR DISPLAYING USER TASK ***************** #
class userTaskPageGUI:
    # Constructor specifications
    def __init__(self):
        print("Construct Task Page page #1")

        # Initiates tkinter object and frame
        self.root = tkinter.Tk()
        self.userMainFrame = Frame(self.root, padx=10, pady=10)

        # Creates frames
        self.userFrameTop = LabelFrame(self.userMainFrame, padx=10, pady=10)
        self.userFrameTopMid = LabelFrame(self.userMainFrame, padx=10, pady=10)
        self.userFrameMiddle = LabelFrame(self.userMainFrame, padx=5, pady=5)
        self.userFrameBottom = LabelFrame(self.userMainFrame, padx=10, pady=10)

        # Add grid specifications for frames
        self.userMainFrame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.userFrameTop.grid(column=0, row=0, sticky=(N, S, E, W))
        self.userFrameTopMid.grid(column=0, row=1, sticky=(N, S, E, W))
        self.userFrameMiddle.grid(column=0, row=2, sticky=(N, S, E, W))
        self.userFrameBottom.grid(column=0, row=3, sticky=(N, S, E, W))

        # Monitors the status of the Show/Hide Completed Task
        self.hideTask = 0

        # Dictionary of user's pending to-do list, loading and creating the lists
        self.taskButtonDictionary = {}
        self.loadTask(frame=self.userFrameTop, buttonDictionary=self.taskButtonDictionary, status="Pending")
        self.createTaskButtons(self.userFrameTop, self.taskButtonDictionary)

        # Creates and pack Add button
        self.addTaskButton = Button(self.userFrameMiddle, text="++ New Task", command=self.onClickAdd)
        self.addTaskButton.pack(side=LEFT)

        # Creates and pack "Show/Hide Complete Task" button
        self.hideTaskButton = Button(self.userFrameMiddle, command=self.hideAndShowCompleteTask)
        self.hideTaskButton.config(text="Show Completed Task")
        self.hideTaskButton.pack(side=RIGHT)

        # Creates and pack an information label
        self.detailLabel = Label(self.userFrameBottom, text="Click any Task for Details or Modification...")
        self.detailLabel.pack(fill=BOTH, expand=True)

        # Creates frame's tile and display integrated widgets
        self.root.title("My To-Do List")
        self.root.mainloop()

    # Description: Loads user's task in a dictionary
    def loadTask (self, frame, buttonDictionary, status):
        print("loadTask process:")
        count = 0
        try:
            fileDictionary = open("files/taskFile.txt", "r+")
            readLine = fileDictionary.readline()

            # File reading process
            while(readLine):
                taskDetails = readLine.split("(&%^cvd)")
                # Check the status of current file line
                if taskDetails[3].split()[0] == status:
                    buttonDictionary["Task" + str(count + 1)] = Button(frame, text=taskDetails[0], width=40)
                    count += 1
                readLine = fileDictionary.readline()

            if count < 1:
                tasklabel = Label(frame, text="No take available")
                tasklabel.pack()

        except FileNotFoundError:
            messagebox.showerror("File Error", "Login file File cannot be open")
            print("File Error Cannot open this file)")

#   Create Button from a dictionary of buttons
    def createTaskButtons(self, frame, buttonDictionary):
        print("createTaskButtons:")
        i = 0
        for key in buttonDictionary:
            print("key: " + str(key) + ", val:" + str(buttonDictionary.get(key)))
            tasklabel = Label(frame, text="Task " + str(i + 1) + "")
            tasklabel.grid(column=0, row=i, sticky=(S, W), pady=5)

            buttonDictionary.get(key).grid(column=1, row=i, sticky=(S, W), pady=5, padx=5)
            buttonDictionary.get(key).config(command=lambda x=(buttonDictionary.get(key).cget("text")): self.onClickingATask(x))

            i += 1

    # Description: Initiates the detailed view of clicked task
    def onClickingATask(self, title):
        print("onClickingATask clicked: " + str(title))
        viewTaskDetailsGUI(title)

    # Description: Initiates Addition of new task (To-do)
    def onClickAdd(self):
        print("onClickAdd clicked!!")
        emptyArray = []
        userAddAndEditTaskGUI(emptyArray)

    # Description: Initiates Cancellation/Deletion the object in action
    def onClickCancel(self):
        print("onClickCancel clicked!!")
        self.__del__()

    # Description: Controls the display and hiding of completed task by user
    def hideAndShowCompleteTask(self):
        print("hideCompleteTask clicked:")
        buttonDictionary = {}
        if self.hideTask == 0:
            self.hideTaskButton.config(text="Hide Completed Task")
            self.userFrameMiddle = LabelFrame(self.userMainFrame, padx=5, pady=5)
            self.userFrameTopMid.grid(column=0, row=1, sticky=(N, S, E, W))

            self.loadTask(self.userFrameTopMid, buttonDictionary, "Done")
            self.createTaskButtons(self.userFrameTopMid, buttonDictionary)
            self.hideTask = 1
        else:
            self.hideTaskButton.config(text="Show Completed Task")
            self.userFrameTopMid.grid_forget()
            self.hideTask = 0

    def __del__(self):
        print("Destroyed", self.__class__.__name__)

#DisplayGUI = userTaskPageGUI()