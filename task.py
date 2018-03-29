import os
import datetime
from functools import total_ordering
import re
from utils import index_of_first_occurence


class TaskManager:
    """
       Taskmanager is responsible for managing the tasks. Persists the tasks
       to csv file. The taskmanager provides methods adding/deleting and
       for methods for finding tasks. The class also assigns a unique id
       to every task object, ensuring tasks have a unique identifier.

    """

    persistfile = "work_log.csv"

    def __init__(self, persistfile=None):
        self.tasklist = []
        self.taskidsfound = []

        if persistfile:
            self.persistfile = persistfile
        if not os.path.isfile(self.persistfile):
            file = open(self.persistfile, "w")
            file.write("taskid,title,date,timespent,notes" + os.linesep)
            file.close()
        self.loadTasks()

    def loadTasks(self):
        """

        :return: None
        """
        if os.path.isfile(self.persistfile):
            f = open(self.persistfile, "r")
            lines = f.readlines()
            if len(lines) < 1:
                return
            lines.pop(0)
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                fields = line.split(",")
                title = fields[1]
                datestr = fields[2]
                timespent = fields[3]
                notes = fields[4]
                taskid = int(fields[0])
                self.taskidsfound.append(taskid)
                task = Task(title=title, date=datestr, timespent=timespent,
                            notes=notes, taskid=taskid)
                self.tasklist.append(task)
            f.close()

    def getmaxid(self):
        if self.taskidsfound:
            return max(self.taskidsfound)
        return 0

    def edittask(self, task):
        self.delete_task(task.taskid)
        replacedtask = Task(title=task.title, date=task.datestr,
                            timespent=task.timespent, notes=task.notes)
        self.add_task(replacedtask)

    def delete_task(self, taskid):
        for i, t in enumerate(self.tasklist):
            if t.taskid == taskid:
                del self.tasklist[i]
                self.taskidsfound.remove(taskid)
                self._persist_tasks()
                return True
        return False

    def add_task(self, *args):
        """
        :param args: single or multiple Task objects to be added
        :return: None
        """
        file = open(self.persistfile, "a")
        for task in args:
            if task.taskid in self.taskidsfound:
                return
            task.taskid = self.getmaxid() + 1
            self.taskidsfound.append(task.taskid)
            file.write(str(task) + os.linesep)
            self.tasklist.append(task)
        file.close()

    def find_by_date_range(self, date1, date2):
        """
            search existing tasks by a date range

            :param date: find by date
            :return: list: of task objects found, sorted by datetime
         """
        taskstortn = []
        for t in self.tasklist:
            if t.date >= date1 and t.date < date2:
                taskstortn.append(t)
        return sorted(taskstortn)

    def find_by_date(self, targetdate):
        """
        search existing tasks by a date.

        :param date: find by date
        :return: list of task objects found, sorted by datetime
         """
        taskstortn = []
        sortedtasklist = sorted(self.tasklist)
        firstindex = index_of_first_occurence(
            sortedtasklist, targetdate
        )
        if firstindex is None:
            return taskstortn
        for i in range(firstindex, len(sortedtasklist)):
            if sortedtasklist[i].date == targetdate:
                taskstortn.append(sortedtasklist[i])
        return taskstortn

    def keywordsearch(self, keyword):
        """
        Returns all task with keyword in title or notes.

        :param keyword: keyword to search by
        :return: list of task objects found
        """
        taskstortn = []
        for task in self.tasklist:
            if keyword in task.title or keyword in task.notes:
                taskstortn.append(task)
        return taskstortn

    def regexsearch(self, regex):
        """
        Returns all task with that satisfies regex condition.

        :param regex: regex to search by
        :return: list of task objects found
        """
        regexcompiled = re.compile(regex)
        taskstortn = []
        for task in self.tasklist:
            if regexcompiled.search(task.title) \
                    or regexcompiled.search(task.notes):
                taskstortn.append(task)
        return taskstortn

    def _persist_tasks(self):
        """
        Persist all tasks to file. Uses "w" mode to recreate the file if
        already exists
        :return: None
        """
        file = open(self.persistfile, "w")
        file.write("taskid,title,date,timespent,notes" + os.linesep)
        for task in self.tasklist:
            file.write(str(task) + os.linesep)
        file.close()


@total_ordering
class Task(object):
    """
    Task object that contains attributes that represent a task.
    A task is equal if the taskid's are the same. Tasks are ordered by
    date, which allows for sorting of tasks and implementing
    efficient searches.
    """

    def __repr__(self):
        return self.taskid

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.datestr = kwargs.get('date')
        self.date = datetime.datetime.strptime(kwargs.get('date'), '%m/%d/%Y')
        self.timespent = kwargs.get('timespent')
        self.notes = kwargs.get('notes')
        self.taskid = kwargs.get('taskid', None)

    def __str__(self):
        datestr = self.date.strftime('%m/%d/%Y')
        return "{0},{1},{2},{3},{4}".format(self.taskid, self.title, datestr,
                                            self.timespent, self.notes)

    def __eq__(self, o):
        if self.taskid is None or o.taskid is None:
            return False
        return self.taskid == o.taskid

    def __lt__(self, o):
        """
        comare two Task objects and use date object as means of comparison
        """
        return self.date < o.date
