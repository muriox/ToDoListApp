#!/usr/bin/python3
import tkinter
from tkinter import*
from tkinter import messagebox

# ************* CLASS FOR ADDING AND EDITING TASK DETAILS ***************** #
class userAddAndEditTaskGUI:
    # Constructor specifications
    def __init__(self, passedArray):
        print("Construct AddTaskPage page #1")
        self.detailArray = passedArray
        print("vals:" + str(self.detailArray))

        # Initiates tkinter object and frame
        self.root = tkinter.Tk()
        self.addMainFrame = Frame(self.root, padx=10, pady=10)

        # Creates frames
        self.addFrameTop = LabelFrame(self.addMainFrame, padx=5, pady=5)
        self.addFrameMiddle = LabelFrame(self.addMainFrame, padx=5, pady=5)
        self.addFrameBottomTop = LabelFrame(self.addMainFrame, padx=5, pady=5)
        self.addFrameBottomDown = LabelFrame(self.addMainFrame, padx=5, pady=5)

        # Add grid specifications for frames
        self.addMainFrame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addFrameTop.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addFrameMiddle.grid(column=0, row=1, sticky=(N, S, E, W))
        self.addFrameBottomTop.grid(column=0, row=2, sticky=(N, S, E, W))
        self.addFrameBottomDown.grid(column=0, row=3, sticky=(N, S, E, W))

        # Creates label for Title field
        self.titleLabel = Label(self.addFrameTop, text="Task Title:")
        self.titleLabel.grid(column=0, row=0, sticky=(S, W), pady=10)

        # Creates label for Date field
        self.dateLabel = Label(self.addFrameTop, text="Date:")
        self.dateLabel.grid(column=0, row=1, sticky=(S, W), pady=10)

        # Creates label for Description field
        self.descriptionLabel = Label(self.addFrameMiddle, text="Description:")
        self.descriptionLabel.grid(column=0, row=0, sticky=(S, W))

        # Creates labels, Rdaiobuttons for Status field
        self.radioVal = "None"
        self.statusRadioLabel = Label(self.addFrameBottomTop, text="Status:")
        self.statusRadioLabel.grid(column=0, row=0, sticky=(S, W), pady=5)
        self.statusRadioButton1 = Radiobutton(self.addFrameBottomTop, text="Pending", value="Pending")
        self.statusRadioButton2 = Radiobutton(self.addFrameBottomTop, text="Done", value="Done")

        # Description: If a new add task is to be added to file, below fields and entries are used
        if len(self.detailArray) < 1:
            self.titleEntry = Entry(self.addFrameTop)
            self.titleEntry.grid(column=1, row=0, sticky=(S, W), pady=10)

            self.dateEntry = Entry(self.addFrameTop)
            self.dateEntry.grid(column=1, row=1, sticky=(S, W), pady=10)
            self.descriptionScroll = Scrollbar(self.addFrameMiddle)
            self.descriptionText = Text(self.addFrameMiddle, borderwidth=3, relief=GROOVE, width=25, height=10,
                                        yscrollcommand=self.descriptionScroll.set)
            self.descriptionText.grid(column=0, row=1, pady=5)
            self.descriptionScroll.config(command=self.descriptionText.yview)

            self.statusRadioButton1.config(command=lambda: self.updateRadioButton(self.statusRadioButton1.cget("value")))
            self.statusRadioButton1.grid(column=0, row=1)
            self.statusRadioButton2.config(command=lambda: self.updateRadioButton(self.statusRadioButton2.cget("value")))
            self.statusRadioButton2.grid(column=1, row=1)

            self.addTaskButton = Button(self.addFrameBottomDown, text="++ New Task", command=self.onClickAddNewTask)
            self.addTaskButton.pack(side=LEFT)

        # Description: If a task is for edit/update to file, below fields and entries are used
        else:
            self.titleEntry = Entry(self.addFrameTop)
            self.titleEntry.insert(0, self.detailArray[0])
            self.titleEntry.grid(column=1, row=0, sticky=(S, W), pady=10)

            self.dateEntry = Entry(self.addFrameTop)
            self.dateEntry.insert(0, self.detailArray[1])
            self.dateEntry.grid(column=1, row=1, sticky=(S, W), pady=10)

            self.descriptionScroll = Scrollbar(self.addFrameMiddle)
            self.descriptionText = Text(self.addFrameMiddle, borderwidth=3, relief=GROOVE, width=25, height=10,
                                        yscrollcommand=self.descriptionScroll.set)
            self.descriptionText.insert(1.0, self.detailArray[2])
            self.descriptionText.grid(column=0, row=1, pady=5)
            self.descriptionScroll.config(command=self.descriptionText.yview)

            self.statusRadioButton1.config(command=lambda: self.updateRadioButton(self.statusRadioButton1.cget("value")))
            self.statusRadioButton1.grid(column=0, row=1)
            self.statusRadioButton2.config(command=lambda: self.updateRadioButton(self.statusRadioButton2.cget("value")))
            self.statusRadioButton2.grid(column=1, row=1)

            self.editTaskButton = Button(self.addFrameBottomDown, text="++Edit/Complete Task",
                                         command=lambda: self.addOrUpdateTask(self.detailArray[0],self.detailArray[1],
                                                                              self.detailArray[2], self.radioVal))
            self.editTaskButton.pack(side=LEFT)

        # Creates and pack cancel button
        self.cancelTaskButton = Button(self.addFrameBottomDown, text="Cancel", anchor=W, justify=LEFT,
                                       command=self.onClickCancelTask)
        self.cancelTaskButton.pack(side=RIGHT)

        # Creates frame's tile and display integrated widgets
        self.root.title("++New Task")
        self.root.mainloop()

    def updateRadioButton(self, newValue):
        self.radioVal = newValue
        print("updateRadioButton Clicked!!", self.radioVal)

    # Description: Initiates writing new task into taskFile(if conditions are met),
    #   close and destroy userAddNewTaskGUI object
    def onClickAddNewTask(self):
        print("onClickAddNewTask Clicked!!")
        title = self.titleEntry.get()
        date = self.dateEntry.get()
        description = self.descriptionText.get(1.0, END)
        vRadio = self.radioVal

        print("Status:", vRadio)
        # Process writing into file
        self.addOrUpdateTask(title, date, description, vRadio)

    # Description: Don't write into taskFile, close and destroy userAddNewTaskGUI object
    def onClickCancelTask(self):
        print("onClickCancelTask Clicked!!")
        self.root.destroy()

    # Description: Checks if a task exist in file or not
    def checkIfTaskExist(self, title, date, status):
        alreadyExist = 0
        try:
            fileDictionary = open("files/taskFile.txt", "r+")
            readLine = fileDictionary.readline()

            # Checks and assign appropriate value to the function call
            while(readLine):
                taskDetails = readLine.split("(&%^cvd)")

                if taskDetails[0] == title and taskDetails[1] == date and taskDetails[3] == status:
                    alreadyExist = 1
                    break
                elif taskDetails[0] == title and taskDetails[1] == date and status == "Done":
                    alreadyExist = 2
                    break
                elif taskDetails[0] == title and taskDetails[1] == date and (status == "Pending" or status == "None"):
                    alreadyExist = 3
                    break
                readLine = fileDictionary.readline()

            fileDictionary.close()

        except FileNotFoundError:
            messagebox.showerror("File Error", "Login file File cannot be open")
            print("File Error Cannot open this file)")

        return alreadyExist

    # Description: Add or update a new task or an existing task respectively
    def addOrUpdateTask(self, title, date, description, status):
        taskExist = self.checkIfTaskExist(title, date, status)
        print("addOrUpdateTask process: Current check:", taskExist)

        # If task doesn't exist in file, write new task to file
        if taskExist == 0:
            resultString = "\n" + str(title) + "(&%^cvd)" + str(date) + "(&%^cvd)" + \
                           str(description)[:len(description) - 1] + "(&%^cvd)" + str(status)
            print("Value:" + resultString)

            # Check if the fields are not empty or "None" for status, else write to file
            if title == "" or date == "" or description == "" or status == "None":
                messagebox.showwarning("Empty Task", "Please fill the required fields")
            else:
                try:
                    taskFile = open("files/taskFile.txt", "a+")
                    # Write new task into taskFile.txt
                    taskFile.writelines(resultString)
                    print(resultString)

                    taskFile.close()
                    self.root.destroy()

                except FileNotFoundError:
                    messagebox.showerror("File Error", "Task file cannot be open")
                    print("File Error Cannot open this file)")

        # If task does exist and status has been updated to "Done", update task in file
        elif taskExist == 2:
            try:
                taskFile = open("files/taskFile.txt", "r+")
                readLines = taskFile.readlines()
                taskFile.seek(0)

                # Task updating process
                for i in readLines:
                    taskDetails = i.split("(&%^cvd)")
                    if taskDetails[0] != title and taskDetails[1] != date:
                        #print("To write:", taskDetails[0])
                        taskFile.write(i)
                    else:
                        taskDetails[3] = "Done"
                        lineToUpdate = taskDetails[0] + "(&%^cvd)" + taskDetails[1] + "(&%^cvd)" + \
                                       taskDetails[2] + "(&%^cvd)" + taskDetails[3]
                        #print("lineToUpdate:", lineToUpdate)
                        taskFile.write(lineToUpdate)

                # Truncate and close file
                taskFile.truncate()
                taskFile.close()
            except FileNotFoundError:
                messagebox.showerror("File Error", "Task file cannot be open")
                print("File Error Cannot open this file)")
        else:
            messagebox.showerror("Task Error", "Sorry, this already exist in your diary")
            print("Sorry, this already exist in your diary")
            self.root.destroy()

    # Description: Delete object, with a print message
    def __del__(self):
        print("Destroyed", self.__class__.__name__)


# ************* CLASS FOR VIEWING TASK DETAILS ***************** #
class viewTaskDetailsGUI:
    def __init__(self, taskTitle):
        print("Construct viewTaskDetails page #1")
        self.values = self.getTaskDetails(taskTitle)

        self.root = tkinter.Tk()
        self.addMainFrame = Frame(self.root, padx=10, pady=10)

        # Create frames
        self.addFrameTop = LabelFrame(self.addMainFrame, padx=10, pady=10)
        self.addFrameMiddle = LabelFrame(self.addMainFrame, padx=5, pady=5)
        self.addFrameBottom = LabelFrame(self.addMainFrame, padx=10, pady=10)

        # Add grid specifications to frames
        self.addMainFrame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addFrameTop.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addFrameMiddle.grid(column=0, row=1, sticky=(N, S, E, W))
        self.addFrameBottom.grid(column=0, row=2, sticky=(N, S, E, W))

        # Creates label and entry for Title field
        self.titleLabel = Label(self.addFrameTop, text="Task:")
        self.titleLabel.grid(column=0, row=0, sticky=(S, W), pady=5)
        self.titleEntry = Label(self.addFrameTop, text=self.values[0])
        self.titleEntry.grid(column=1, row=0, sticky=(S, W), pady=5)

        # Creates label and entry for Date field
        self.dateLabel = Label(self.addFrameTop, text="Date:")
        self.dateLabel.grid(column=0, row=1, sticky=(S, W), pady=5)
        self.dateEntry = Label(self.addFrameTop, text=self.values[1])
        self.dateEntry.grid(column=1, row=1, sticky=(S, W), pady=5)

        # Creates label and text for Description field
        self.descriptionLabel = Label(self.addFrameMiddle, text="Description:")
        self.descriptionLabel.grid(column=0, row=0, sticky=(N, W))
        self.descriptionText = Message(self.addFrameMiddle, text=self.values[2], width=150)
        self.descriptionText.grid(column=0, row=1, sticky=(N, W))

        # Creates label and radio buttons for Status field
        self.statusLabel = Label(self.addFrameMiddle, text="Status:")
        self.statusLabel.grid(column=0, row=2, sticky=(S, W), pady=5)
        self.statusEntry = Label(self.addFrameMiddle, text=self.values[3])
        self.statusEntry.grid(column=0, row=3, sticky=(S, W), padx=5)

        # Creates Edit button
        self.editTaskButton = Button(self.addFrameBottom, text="++Edit/Complete Task")
        self.editTaskButton.grid(column=0, row=0, sticky=(S, W), pady=5, padx=5)
        self.editTaskButton.config(command=lambda: self.onClickEdit())

        # Creates Delete button
        self.deleteTaskButton = Button(self.addFrameBottom, text="Delete Task")
        self.deleteTaskButton.config(command=lambda: self.onClickDelete(self.values[0], self.values[1], self.values[3]))
        self.deleteTaskButton.grid(column=1, row=0, sticky=(S, E), pady=5, padx=5)

        # Creates frame's tile and display integrated widgets
        self.root.title(taskTitle[:8] + "... Details")
        self.root.mainloop()

    # Description: Initiates the task editing interface
    def onClickEdit(self):
        print("onClickEdit Clicked:")
        print("Detail Values:", self.values)
        userAddAndEditTaskGUI(self.values)

    # Description: Initiates and delete a task
    def onClickDelete(self, title, date, status):
        print("OnclickDelete:", title, date, status)
        result = messagebox.askyesno("Delete Task", "Would like to proceed?")

        # Checks the button clicked by user (Yes or No in the dialogue box)
        if result:
            self.deleteATask(title, date, status)
            print("Deleted")
        else:
            print("No action")

    # Description: Fatches the content of a given task when clicked on.
    def getTaskDetails(self, title):
        print("getTaskDetails clicked")
        taskArrayString = ""

        # In case there is a task with no title (most likely none)
        if title == "":
            self.root.destroy()
        else:
            # File reading process
            try:
                taskFile = open("files/taskFile.txt", "r+")
                readLine = taskFile.readline()

                while(readLine):
                    arrayString = readLine.split("(&%^cvd)")

                    if arrayString[0] == title:
                        print("Task values: " + arrayString[0])
                        taskArrayString = arrayString
                        break

                    readLine = taskFile.readline()

                # Close file
                taskFile.close()
            except FileNotFoundError:
                messagebox.showerror("File Error", "Task file cannot be open")
                print("File Error Cannot open this file)")

        return taskArrayString

    # Description: Deletes a given task from file
    def deleteATask(self, title, date, status):
        print("deleteATask process")

        try:
            taskFile = open("files/taskFile.txt", "r+")
            readLines = taskFile.readlines()
            taskFile.seek(0)

            # File deleting process
            for i in readLines:
                taskDetails = i.split("(&%^cvd)")
                if taskDetails[0] != title and taskDetails[1] != date and taskDetails[3] != status:
                    taskFile.write(i)

            # Truncate and close file
            taskFile.truncate()
            taskFile.close()
        except FileNotFoundError:
            messagebox.showerror("File Error", "Task file cannot be open")
            print("File Error Cannot open this file)")


#display = viewTaskDetailsGUI("Lesson")
#v = []
#display = userAddAndEditTaskGUI(v)