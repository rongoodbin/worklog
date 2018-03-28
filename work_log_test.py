import shutil, tempfile
import unittest
import tempfile
from task import *


class WorkLogTests(unittest.TestCase):

    def setUp(self):
       self.test_dir = tempfile.mkdtemp()
       self.file = os.path.join(self.test_dir, 'test1.txt')
       self.taskmanager = TaskManager(persistfile=self.file)

    def test_insert_task(self):
        sometask1 = Task(title="new task2", date="01/11/2017", timespent="2",
                         notes="this task is part of a test")
        expected = ['1,new task2,01/11/2017,2,this task is part of a test']
        self.taskmanager.add_task(sometask1)
        tasklist = [str(t) for t in self.taskmanager.tasklist]
        self.assertEqual(tasklist, expected)

    def test_find_task(self):

        sometask1 = Task(title="new task1", date="01/11/2017", timespent="4",
                         notes="rocked out this task")
        sometask2= Task(title="new task2", date="03/15/2018", timespent="22",
                         notes="yea h baby")
        self.taskmanager.add_task(sometask1,sometask2)
        expected = ['1,new task1,01/11/2017,4,rocked out this task']
        datesfound = self.taskmanager.find_by_date(
            datetime.datetime.strptime("01/11/2017", '%m/%d/%Y'))
        tasksfound = [str(t) for t in datesfound]
        self.assertEqual(tasksfound, expected)

    def test_modify_task(self):
        sometask1 = Task(taskid=1, title="new task to modify",
                         date="03/27/2018", timespent="4",
                         notes="rocked out this task")

        modifiedtask = Task(taskid=1,title="modified", date="03/27/2018",
                            timespent="4",notes="rocked out this task")

        expected = ['1,modified,03/27/2018,4,rocked out this task']

        self.taskmanager.add_task(sometask1)
        self.taskmanager.edittask(modifiedtask)
        taskspresent = [str(t) for t in self.taskmanager.tasklist]
        self.assertEqual(expected,taskspresent)


    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
