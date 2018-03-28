from utils import *


class SearchMenu():
    """
    This class is responsible for the different search functionality.
    class is initialized with a TaskManager to be able to perform
    the searches and interact with exsisting tasks and delete/modify tasks
    """

    def __init__(self, taskmanager):
        self.taskmanager = taskmanager
        self.options = {}

        prompts = []
        prompts.append("What would you like to search by?")
        prompts.append("a) Exact date")
        prompts.append("b) Range of dates")
        prompts.append("c) Exact Search")
        prompts.append("d) Regex pattern")
        prompts.append("e) Return to menu")
        self.prompts = prompts

        self.options["a"] = self.exactdate
        self.options['c'] = self.keywordsearch
        self.options['b'] = self.daterangesearch
        self.options['d'] = self.regexsearch

    def showsearchmenu(self):
        while True:
            promptuser = "\n".join(self.prompts)
            print(promptuser)
            optionselected = input(">")
            if optionselected.lower() == 'e':
                break
            if optionselected in self.options:
                self.options[optionselected]()

    def showtasks(self, tasks):

        for i, task in enumerate(tasks):
            clear_screen()
            tasktitle = task.title
            taskdate = task.datestr
            timespent = task.timespent
            tasknotes = task.notes
            print("Date:{0}".format(taskdate))
            print("Task Title:{0}".format(tasktitle))
            print("Time Spent:{0}".format(timespent))
            print("Task Notes:{0}".format(tasknotes))
            print("\n")
            print("showing {0} of {1}".format(i + 1, len(tasks)))
            action = input("[N]ext, [E]dit, [D]elete, [R]eturn to main menu: ")

            if action.lower() == "n":
                continue

            if action.lower() == "e":
                self.edittask(task)

            if action.lower() == "r":
                return
            if action.lower() == "d":
                if self.taskmanager.delete_task(task):
                    print("Entry has been deleted")
                    asktocontinue()

    def edittask(self, task):

        print("Task Date:" + task.datestr)
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            if convertdate(response):
                task.datestr = response

        print("Task Title:" + task.title)
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            task.title = response

        print("Time Spent:" + task.timespent)
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            task.timespent = response

        print("Notes:" + task.notes)
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            task.notes = response

        self.taskmanager.edittask(task)

    def daterangesearch(self):
        searchedalready = False
        while True:
            if searchedalready:
                response = input("[B]ack to return or enter to search again: ")
                if response.lower() == 'b':
                    break

            searchedalready = True
            clear_screen()
            print("Enter a first date:")
            date1fromuser = input("Please use DD/MM/YYYY: ")
            print("Enter a second date:")
            date2fromuser = input("Please use DD/MM/YYYY: ")

            dateobj1 = convertdate(date1fromuser)
            dateobj2 = convertdate(date2fromuser)

            if dateobj1 is None:
                print(
                    "{0} is not a valid date. Try again".format(date1fromuser))
                enter = input("Press enter to try again: ")
                if enter == "":
                    continue

            if dateobj2 is None:
                print(
                    "{0} is not a valid date. Try again".format(date2fromuser))
                enter = input("Press enter to try again: ")
                if enter == "":
                    continue

            tasksfound = self.taskmanager.find_by_date_range(dateobj1,
                                                             dateobj2)
            if len(tasksfound) < 1:
                print("No tasks found with date range. ")
                enter = input("Press enter to try again: ")
                if enter == "":
                    continue
            self.showtasks(tasksfound)

    def exactdate(self):
        searchedalready = False
        while True:
            if searchedalready:
                response = input("[B]ack to return or enter to search again: ")
                if response.lower() == 'b':
                    break

            searchedalready = True
            clear_screen()
            print("Enter the Date")
            datefromuser = input("Please use DD/MM/YYYY: ")
            dateobj = convertdate(datefromuser)
            if dateobj is None:
                print(
                    "{0} is not a valid date. Try again".format(datefromuser))
                enter = input("Press enter to try again: ")
                if enter == "":
                    searchedalready = False
                    continue
            tasksfound = self.taskmanager.find_by_date(dateobj)
            if len(tasksfound) < 1:
                print("No tasks found with that date. ")
                enter = input("Press enter to try again: ")
                if enter == "":
                    searchedalready = False
                    continue
            self.showtasks(tasksfound)

    def keywordsearch(self):
        clear_screen()
        keyword = input("Enter a keyword to search by: ")

        tasksfound = self.taskmanager.keywordsearch(keyword)
        self.showtasks(tasksfound)

    def regexsearch(self):
        clear_screen()
        regex = input("Enter a regex to search by: ")

        tasksfound = self.taskmanager.regexsearch(regex)
        self.showtasks(tasksfound)
