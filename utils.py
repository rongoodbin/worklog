import os
import re
import datetime

#mulispaceregex = re.compile(r"\s{2}", re.MULTILINE)

def clear_screen():
    '''Method providing a way to clear the screen after
      interface selections'''
    os.system('cls' if os.name == 'nt' else 'clear')

def showprompt():
    return ">"


def asktocontinue():
    enter = input("Press enter to continue")
    if enter == "":
        return True
    else:
        return False


def convertdate(datestr):
    try:
        return datetime.datetime.strptime(datestr, '%m/%d/%Y')
    except:
        return None


def indexoffirstoccurence(lst, target):


    low,high = 0, len(lst)-1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid].date < target:
            low = mid + 1
        elif lst[mid].date > target:
            high = mid -1
        else:
            return mid
    return None


def _showsearchoptions():
    prompts = []
    starttext = "What would you like to search by?"
    prompts.append(starttext)
    prompts.append("a) Exact date")
    prompts.append("b) Range of dates")
    prompts.append("c) Exact Search")
    prompts.append("d) Regex pattern")
    prompts.append("d) Return to menu")



    return "\n".join(prompts)



def showmainmenuoptions():
    prompts = []
    starttext = "What would you like to do"
    prompts.append(starttext)
    prompts.append("a) add new entry")
    prompts.append("b) search existing")
    prompts.append("q) quit")

    return "\n".join(prompts)



def removewhitespace(string_with_whitespace):
    return re.sub("\s{3}","",string_with_whitespace)

