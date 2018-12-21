"""
Christina Shafer
CIS 41A - Fall 2018
Dec 4,2018
Lab 5

Summary:
Class definitions used in Lab5.py. Course is parent class,  NonCreditCourse and CreditCourse are children classes.

"""
import re       #import needed for regex

class Course:
    """
    class that contains information for a course
    """
    def __init__(self,className,startTime,classDays):
        className, startTime,classDays = self._verify(className, startTime, classDays)
        self._className = className.upper()
        self._startTime = startTime
        self._classDays = classDays.upper()
        self._supplies = []

    def __str__(self):
        return self._className +', ' + self._startTime +', ' + self._classDays

    def __lt__(self, other):
        if self._className < other._className:
            return True
        else:
            return False

    def __gt__(self, other):
        if self._className > other._className:
            return True
        else:
            return False

    def addSupplies(self,supplyList=[]):
        """
        method to add supplies to the course
        :param supplyList: list of supplies needed for class
        :return: none
        """
        done =False
        if len(supplyList)>0:
            self._supplies.extend(supplyList)
            done=True
        while not done:
            supplies = input("Enter a comma-separated list of supplies:")
            if len(supplies)>0:
                new_supplies=(supplies.split(",").strip())
                for item in new_supplies:
                    self._supplies.append(item.strip())
                done=True

    def getSupplies(self):
        """
        method to return supply list from course object
        :return: list of supplies
        """
        return self._supplies

    def _verify(self,className,startTime,classDays):
        """private method to verify startTime and classDays are formatted correctly
        :param: className (must not be empty), startTime(formatted HH:MM with MM in 00 or 30), classDays in (M,T,W,R,F)
        """
        className=className.strip().upper()
        startTime=startTime.strip().upper()
        classDays=classDays.strip().upper()
        #verifyClassname
        if not(len(className)>0):
            raise ValueError("Classname must not be empty.")

        #verify startTime format
        done = False
        while not done:
            m=re.search("^\s*(\d\d?)((:?\d{2})?)\s*([ap]m)\s*",startTime,re.I)
            if not m:
                print(startTime,"is not valid.", end=" ")
                startTime= input("Enter new time: ").strip().upper()
                continue
            try:  #works if both hours and minutes are entered
                if not ((1<=int(m.group(1))<=12) and ( 0<=int(m.group(2).strip(":"))<=59)) :
                    print(startTime,"is not a valid time.", end=" ")
                    startTime= input("Enter new time: ").strip().upper()
                startTime=str(m.group(1))+":"+str(m.group(2).strip(":"))+m.group(4)
            except: #runs if only hours are entered
                if not (1<=int(m.group(1))<=12):
                    print(startTime,"is not a valid time.", end=" ")
                    startTime= input("Enter new time: ").strip().upper()
                startTime=str(m.group(1))+":00"+m.group(4)
            done=True
        #verify classDays
        if len(classDays)<1:
            raise ValueError("Class Days must not be empty. Possible values are: MTWRF")
        daySet=set(classDays)
        for char in daySet:
            if char.upper() not in ('M','T','W','R','F'):
                raise ValueError("Incorrect class day. Possible values are: MTWRF")
        return(className, startTime.upper(),classDays.upper())

class NonCreditCourse(Course):
    """
    child object of Course.  adds activities to object and printActivities method.
    """
    def __init__(self,className,startTime,classDays):
        super().__init__(className,startTime,classDays)
        self._activities = []

    #below is useful if you did not write the course class. we don't want to be the police
    #making sure that the parameters are the right ones. We pass the parameters to parent
    #class and let it do the checks and then when it succeeds, we do the part we are
    #implementing (in this case, adding activities)

    #def __init__(self, *args, **kwargs):
    # super().__init__(*args,**kwargs)
    # self._activities = []

    def addActivities(self,*args):
        """ Adds activities to Non-Credit Course
        :param *args: list of activities to add to non-credit course
        :return:
        """
        done =False
        if len(*args)>0:
            done=True
            self._activities.extend(*args)
        while not done:
            acts = input("Enter a comma-separated list of activities:")
            if len(acts)>0:
                self._activities.extend(*acts)
                done=True
    def printActivities(self):
        """prints out the course activities"""
        print(', '.join(self._activities)  #should have been sorted

class CreditCourse(Course):
    """
    child class of Course.  Adds course units as well as a dictionary of activities and the scores associated
    with them (_grades)
    """

    def __init__(self,className,startTime,classDays,units):
        super().__init__(className,startTime,classDays)
        self._verifyUnits(units)
        self._units = float(units)
        self._grades = {}

    def __str__(self):
        returnStr=self._className + ', ' + self._startTime + ', '
        returnStr +=self._classDays + ', ' + str(self._units) + ' units'
        returnStr="{:s}, {:s}, {:s}, {:.1f} units".format(self._className,self._startTime,self._classDays,self._units)
        return returnStr

    def _verifyUnits(self,units):
        """verifies that the units passed to the constructor are valid.
        @:return - none, but can throw an exception
        """
        _VALID_UNITS=[i/10 for i in range(5,51,5)]
        try:
            units=float(units.strip())
        except:
            raise ValueError("Invalid units entered. Units must be a number between .5 & 5.0")
        if units not in _VALID_UNITS:
            raise ValueError("Invalid units entered.  Please use format x.x")

    def getLetterGrade(self):
        """
        method to get average score and resulting letter grade
        :param *args: float scores
        :return: tuple of avg score and letter grade
        """
        _sum=0
        for val in self._grades.values():
            _sum+=val[0]
        _count=len(self._grades)
        if _count==0:
            return None
        avg=_sum/_count
        avgInt=int(_sum//_count)
        if avgInt==100:
            return(100.0, "A+")     #no need to compute, A+
        if avgInt<=59:
            return(avg,"F")         #no need to compute, F
        letter=chr(74-(avgInt//10))   #finds letter for scores 60-99
        if (avgInt%10>=8):       #adds a + if warranted
                letter+="+"
        if (avgInt%10<2):        #adds a - if warranted
                letter+="-"
        return(avg,letter)

    def addGrades(self,tasks=[],scores=[],letterGrades=[]):
        """Adds tasks and corresponding scores to the _grades dictionary when input is valid.
        prints an error message, but does not throw an exception in case of non-valid input
        """
        done=False
        lengthTest=set([len(tasks),len(scores),len(letterGrades)])
        if len(lengthTest)!=1: #meaning tasks, scores and lettersGrades are not the same size
            print("Incorrect data entered.  Number of tasks,corresponding scores and grades must all be the same.")
        elif len(tasks)>0:
            scores_tuple_list=[(scores[i],letterGrades[i].strip().upper()) for i in range(len(scores))]
            self._grades = dict(zip(tasks,scores_tuple_list))
            done=True

        while not done:
            tasks = input("Enter a comma-separated list of tasks:")
            while len(tasks)<1:
                tasks = input("Enter a comma-separated list of tasks:")
            tasks=tasks.split(",")
            scores = input("Enter a comma-separated list of corresponding scores:")
            while len(scores)<1:
                scores = input("Enter a comma-separated list of corresponding scores:")
            scores=scores.split(",")
            letterGrades = input("Enter a comma-separated list of corresponding letter grades:")
            while len(letterGrades)<1:
                scores = input("Enter a comma-separated list of corresponding letter grades:")
            letterGrades=letterGrades.split(",")
            try:
                for i in range(len(scores)):
                    scores[i]=float(scores[i])   #can raise an exception
            except:
                print("Type error in entered scores.")
                continue
            lengthTest=set([len(tasks),len(scores),len(letterGrades)])
            if len(lengthTest)==1: #meaning tasks, scores and lettersGrades are the same size
                scores_tuple_list=[(scores[i],letterGrades[i].strip().upper()) for i in range(len(scores))]
                self._grades = dict(zip(tasks,scores_tuple_list))
                done=True
            else:
                print("Incorrect data entered.  Number of tasks, corresponding scores and grades must be the same.")

    def printActivities(self):
        """prints _grades dictionary in alphabetic order"""
        for k in sorted(self._grades):
            print("{:15s} {:>10.1f} {:5s}".format(k.strip()+":",self._grades[k][0], self._grades[k][1].strip()))
        if len(self._grades)>0:
            avg,letter=self.getLetterGrade()
            print("Current Avg:{:>14.1f}".format(avg), letter)
#function
def printActivities(obj):
    """function that calls the object method 'printActivities()' for the passed object"""
    obj.printActivities()

def main() :
    c = CreditCourse("CIS 41A","9:30","MW","4.5")
    c.addSupplies(["laptop"])
    c.addGrades(["Assignments","Exams","Quizzes"],[92.5,86.0,88.4])
    print("Class:\n" + str(c))
    print("Supplies:", ', '.join(c._supplies))
    printActivities(c)

    print()
    nc = NonCreditCourse("Hiking","8:00","T")
    nc.addSupplies(["boots","sunscreen","hat"])
    nc.addActivities(["Big Sur","Coastal Trail","Mt. Diablo"])
    print("Class:\n" + str(nc))
    print("Supplies:" + ', '.join(nc._supplies))
    printActivities(nc)


#main()

