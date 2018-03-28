import sys
from utils import *
from task import TaskManager, Task
from menu import SearchMenu


class Worklog:
    """
    Main entry to the worklog program. Mainmenu() kicks of the main screen
    asking for different actions. A TaskMananger object is instantiated and
    passed to the SearchMenu object for further search interactions.
    """

    def __init__(self):
        self.taskmanager = TaskManager()
        self.currentoption = None

    def searchworklog(self):
        clear_screen()
        search = SearchMenu(self.taskmanager)
        search.showsearchmenu()
        self.mainmenu()

    def addentry(self):
        print("Date of Task:")
        datefromuser = input("Please use DD/MM/YYYY:")
        tasktitle = input("Title of task:")
        timespent = input("Time spent:")
        tasknotes = input("Notes (optional):")

        task = Task(title=tasktitle, date=datefromuser, timespent=timespent,
                    notes=tasknotes)
        self.taskmanager.add_task(task)
        clear_screen()
        enter = input("Your task has been added. Enter to return to main menu")
        if enter == "":
            self.mainmenu()

    def mainmenu(self):
        print(showmainmenuoptions())
        useroption = input(showprompt())
        if useroption.lower() == "a":
            self.addentry()
        elif useroption.lower() == 'q':
            print("Thanks for using the work log system.")
            sys.exit(1)
        elif useroption.lower() == 'b':
            self.searchworklog()
        useroption = input(">")
        self.currentoption = "mainmenu"
        print(useroption)


if __name__ == "__main__":
    worklog = Worklog()
    worklog.mainmenu()
