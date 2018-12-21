"""
Christina Shafer
CIS 41A - Fall 2018
Dec 4, 2018
Lab 5

Summary:
A program that maintains a class list for a student.  The student can take for-credit classes or non-credit classes
Program lets student enter data on their current classes, then the program prints out the class list, the supplies
needed for each class day and the grade record for each for-credit class

"""
from course import *

class ClassList:
    FILE="lab5.txt"   #create a class variable, use as self.FILE
    """
    object that holds a list of courses
    """
    def __init__(self):
        self._courses=[]
        self.addCourses("lab5.txt")

    def getCourses(self):
        """
        method to return the list of courses
        :return: _courses
        """
        return self._courses

    def addCourses(self,filename=None):
        """
        method to prompt user for courses for the ClassList
        :return:
        """
        if not filename:
            goodCourseNum=False
            while goodCourseNum==False:
                try:
                    numCourses=int(input("How many courses do you want to enter?"))  #can throw an exception
                    goodCourseNum=True
                except:
                    print("Number of courses must be a digit")


            for i in range(numCourses):
                choice =input("Enter 'c' for credit or 'nc' for non-credit:")
                while choice.upper() not in ("C","NC"):
                    print("Invalid Class type. ")
                    choice =input("Enter 'c' for credit or 'nc' for non-credit:")
                if choice.upper() =="C" :
                    done=False
                    while done==False:
                        info = input("Enter comma-separated class name, time, days, units: ")
                        info=info.split(",")
                        while len(info)!=4:
                            print("Incorrect number of fields entered.")
                            info = input("Enter comma-separated class name, time, days, units: ")
                            info=info.split(",")
                        try:
                            newCourse=CreditCourse(*info)
                            newCourse.addSupplies()
                            newCourse.addGrades()
                            done=True
                        except (ValueError):
                            print("Incorrect data entered")

                else:
                    done=False
                    while done==False:
                        info = input("Enter comma-separated class name, time, days: ")
                        info=info.split(",")
                        while len(info)!=3:
                            print("Incorrect number of fields entered.")
                            info = input("Enter comma-sarated class name, time, days: ")
                            info=info.split(",")
                        try:
                            newCourse= NonCreditCourse(*info)
                            newCourse.addSupplies()
                            newCourse.addActivities()
                            done=True
                        except (ValueError):
                            print("Incorrect data entered")
                self._courses.append(newCourse)
        else:
            #this is where we do the work for parsing a file and creating classes
            self.readClassList()
    def readClassList(self) :
        """
        method that reads in class data from a file and populates the classList
        :return: None
        """
        try:
            filename="lab5.txt"
            with open(filename) as infile :  #possible IO Exception
                done = False
                while not done :
                    line=infile.readline()
                    if line=="":    #end of file reached
                        done=True
                        continue
                        #CreditCourse processing
                    if line.strip().upper()=="C":
                        line=infile.readline()  #read in course info line
                        info=line.split(",")
                        newCourse=CreditCourse(*info) #unpack
                        #read in supplies
                        supplies=[i.strip() for i in infile.readline().split(",")]
                        newCourse.addSupplies(supplies)
                        tasks=[i.strip() for i in infile.readline().split(",")]
                        scores=[float(i) for i in infile.readline().split(",")]
                        letterGrades=[i.strip() for i in infile.readline().split(",")]
                        newCourse.addGrades(tasks, scores, letterGrades)
                        self._courses.append(newCourse)
                        continue
                        #NonCreditCourse processing
                    if line.strip().upper()=="NC":
                        info=infile.readline().split(",")  #read in course info line
                        newCourse=NonCreditCourse(*info) #unpack
                        supplies=[i.strip() for i in infile.readline().split(",")]
                        newCourse.addSupplies(supplies)
                        activities=[i.strip() for i in infile.readline().split(",")]
                        newCourse.addActivities(activities)
                        self._courses.append(newCourse)
                        continue
                        #error lines
                    if len(line.strip())>0 and line.strip().upper not in ("C","NC"):
                        print("Invalid line:",line, end="")
        except IOError :
            print("Can't open " + filename)
            SystemExit(1)
    def printSupplies(self,day):
        """
        method to print the supplies needed in all courses for a particular day
        :param day: could be M,T,W,R,F
        :return: no return, just a print
        """
        supplySet=set()
        #create a list of courses on the day
        daysClasses=set([course for course in self._courses if day in course._classDays])
        for course in daysClasses:
            courseSupplies=set(course.getSupplies())
            supplySet=supplySet.union(courseSupplies)
        items= sorted(supplySet)
        if len(items)>0:
            print(day + ": " , end="")
            print(', '.join(items))


    def report(self):
        """
        method to print all info on classList. calls two methods: printSupplies, printClassList
        :return:
        """
        menu="\nC. Class List\nS. Supplies\nA. Activities\nQ. Quit"
        print()
        print(menu)
        quit=False
        while not quit:
            choice= input("Choice:").upper().strip()
            if choice not in ('A','S','C','Q'):
                print("Invalid Choice.")
                print()
                continue
            if (choice=='S'):
                print()
                print("Supplies for each day of class:")
                allDays=['M','T','W','R','F']
                for day in allDays:
                    self.printSupplies(day)
                print()
                continue
            if (choice=='A'):
                print()
                self.printClassList()
                print()
                continue
            if (choice=='C'):
                print()
                for c in sorted(self._courses):
                    print(c)
                print()
                continue
            if (choice=='Q'):
                print("\nGood-bye!")
                quit=True



    def printClassList(self):
        """
        method to print out all class info for classes in ClassList in alphabetical order
        :return:
        """
        print()
        print("Activities for each class")
        alphaList=sorted(self._courses)
        for i in range(len(alphaList)):
            print()
            print(str(alphaList[i]))
            alphaList[i].printActivities()




def main():
    """the main"""
    L=ClassList()
    L.report()

main()


