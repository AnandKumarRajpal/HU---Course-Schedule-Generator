from datetime import timedelta
import copy
import csv


def Day_Num(days):  # This loooks much better!
    if 'Th' in days:
        days = days.replace('Th', 'H')
    final = []
    for i in days:
        if i == 'M':
            final.append(0)
        elif i == 'T':
            final.append(1)
        elif i == 'W':
            final.append(2)
        elif i == 'H':
            final.append(3)
        elif i == 'F':
            final.append(4)
        elif i == 'S':
            final.append(5)
    return final


def HoursMintsConv(t):  # t is str: e.g. '14:00
    t = str(t)
    pos1 = t.find(':')

    hours = int(t[:pos1])
    mints = int(t[pos1 + 1:])

    return hours, mints


def convert_to_24_time(time):
    if time == 'noon':
        return timedelta(hours=12, minutes=00)
    hours, mints = HoursMintsConv(time[:-1])
    if time[-1] == 'p':
        if hours == 12:
            outTime = timedelta(hours=hours, minutes=mints)
        else:
            outTime = timedelta(hours=hours + 12, minutes=mints)
    elif time[-1] == 'a':
        if hours == 12:
            outTime = timedelta(hours=0, minutes=mints)
        else:
            outTime = timedelta(hours=hours, minutes=mints)

    return outTime


# t1 = timedelta(hours = 18,minutes = 20)

def timeDeltaConv(t):  # t is str: e.g. '14:00
    t = str(t)
    pos1 = t.find(':')

    hours = int(t[:pos1])
    mints = int(t[pos1 + 1:])

    return hours, mints,


class Course():
    NumberOfCourses = 0

    def __init__(self, title, Id, inst, times, c, cr=None, sec=None, Type=None):
        self.Title = title
        self.CourseID = Id
        self.Instructor = inst  # instructor
        self.Time = times  # e.g. ([(0,2:30 p.m.,5:00 p.m,)] 0-1-2(DayOfWeekNumber e.g ('T' = 1),Starttiem,endtime)
        self.credits = c
        self.Section = sec
        Course.NumberOfCourses += 1
        self.classroom = cr
        self.Type = Type

    def search_time(self, day):
        i = 0
        while i < len(self.Time):
            if self.Time[i][0] == day:
                return self.Time[i]
            i += 1
        raise ValueError('Not Found by search_time()')


class CourseAtDay:  # Contains a single time

    def __init__(self, day, course):
        self.Title = course.Title
        self.CourseID = course.CourseID
        self.Instructor = course.Instructor  # list of instructors
        self.Time = course.search_time(
            day)
        # e.g. (0,2:30 p.m.,5:00 p.m) 0-1-2 (DayOfWeekNumber e.g ('T' = 1),Starttiem,endtime)
        self.Section = course.Section
        self.credits = course.credits
        self.classroom = course.classroom
        self.Type = course.Type

    def duration(self):
        return self.Time[2] - self.Time[1]

    def getInList(self):
        # h,m =timeDeltaConv()
        # st = h +':'+m

        tup = (self.CourseID, self.Section, self.Type, self.Title, self.credits, self.Time[0], str(self.Time[1]),
               str(self.Time[2]), self.classroom, None, self.Instructor)
        return tup


# class Report:

#   def __init__(self, course = None, CC = None,day = None):
#     self.insertedCourse = course
#     self.clashedCourse = CC # list of course objects
#     self.day = day

#   def printSchedule(self):
#     print('Course',self.insertedCourse.Title ,'was out of bounds', end =' ')
#     if self.day == None:
#       print()
#     else:
#       print('on day',self.day)
#       print()
class ClashReport:
    Reports = []

    def __init__(self, course=None, CC=None, day=None):

        self.insertedCourse = course
        self.clashedCourse = CC  # list of course objects
        self.day = day

        found = False
        for r in ClashReport.Reports:  # Assuming Course ID is unique for each course section
            if r.insertedCourse.CourseID == course.CourseID:
                if r.clashedCourse.CourseID == CC.CourseID:
                    if r.day == day:
                        found = True
                        break

        if not found:
            ClashReport.Reports.append(self)

    def printSchedule(self):
        print('Course', self.insertedCourse.Title, 'Clashes with:', self.clashedCourse.Title, end=' ')
        if self.day == None:
            print()
        else:
            print('on day', self.day)
            print()


# c = ClashReport(phy,chem,4)
# c2 = ClashReport(phy,chem,4)
# lst = []
# allclashreports = ClashReports.Reports

# allclashreports[i].printSchedule


class schedule:

    def __init__(self):
        # self.Status = "New"
        self.schedule = [[] for i in range(6)]  # Mon-Saturday
        self.finalTime = timedelta(hours=18, minutes=30)
        self.initialTime = timedelta(hours=8, minutes=30)

        # schedule.TotalCredits = 0
        self.CourseList = []

    def InRangeOfDay(self, wk, low, high):
        if len(self.schedule[wk]) == 0:
            return []
        elif (self.schedule[wk][0].Time[1] > high or self.schedule[wk][-1].Time[2] < low):
            return []
        else:
            Len = len(self.schedule[wk])
            l = 0
            h = Len - 1
            courses = []
            while True:
                if l >= Len or h < 0:
                    return []

                if self.schedule[wk][l].Time[1] < low:
                    l += 1
                    continue
                if self.schedule[wk][h].Time[2] > high:
                    h -= 1
                    continue

                break

            for i in range(l, h + 1):
                courses.append(self.schedule[wk][i])

            return courses

    def inRange(self, wk, low, high):  # Constraint: wk is int or code: 'All'  and low/high are timedelta
        if wk == 'all':
            courses = []
            for day in range(6):
                courses.extend(self.InRangeOfDay(day, low, high))  # TBM

        elif type(wk) is list:
            courses = []
            for day in wk:
                courses.extend(self.InRangeOfDay(day, low, high))

        else:
            return self.InRangeOfDay(wk, low, high)

    # def display(self):
    #   print('weekly Schedule')
    #   for i in range(6):
    #     print(" Day ",i, end = '  |')

    #   line = '\n'+(' '*9+'|')*6

    #   print(line,sep = '')

    def printSchedule(self):
        daysList = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
        print('                   <<< Schedule >>>')
        for i in range(6):
            print(daysList[i], ':')
            for j in self.schedule[i]:
                print(str(j.Time[1])[:-3] + '--' + str(j.Time[2])[:-3], end=' ')
                print(j.CourseID)
            print()
            # print(j.Time[1].time(),j.Time[2].time())

    def getList(self):
        wk = []
        for i in range(6):
            day = []
            for crs in self.schedule[i]:
                day.append(crs.getInList())
            wk.append(day)

        return wk

    def addCourse(self, course, pos=None):
        if pos == None:
            self.schedule[course.Time[0]].append(course)
        else:
            self.schedule[course.Time[0]].insert(pos, course)

    def nextSchedule(self, course):  # make sub class of course
        nextS = copy.deepcopy(self)

        for times in course.Time:
            day, startTime, endTime = times
            # print('day: ',day)
            crs = CourseAtDay(day, course)
            # print(course.Title, endTime, startTime)
            if endTime > self.finalTime or startTime < self.initialTime:
                return ("Out of Schedule Bounds"), None
            else:
                if len(self.schedule[day]) == 0:  # If No courses that day
                    nextS.addCourse(crs)
                else:

                    lst = self.schedule[day]  # Needs fixing: Only used once, rather use lst always or don't
                    if endTime < lst[0].Time[1]:  # start time of first course of the day greater than end time
                        nextS.addCourse(crs, 0)

                    else:
                        Len = len(lst)
                        i = 0
                        # print('  ', self.schedule)
                        while i < Len and self.schedule[day][i].Time[1] <= startTime:
                            # print(self.schedule[i])
                            i += 1

                        if i == Len:

                            if self.schedule[day][i - 1].Time[2] <= startTime:
                                nextS.addCourse(crs, i)
                            else:
                                return ClashReport(crs, self.schedule[day][i - 1], day)  # Clash
                        else:
                            if self.schedule[day][i - 1].Time[2] < startTime:
                                if self.schedule[day][i].Time[1] > endTime:
                                    nextS.addCourse(crs, i)

                                else:
                                    return ClashReport(crs, self.schedule[day][i], day)  # Clash
                            else:
                                return ClashReport(crs, self.schedule[day][i - 1], day)  # Clash
        nextS.CourseList.append(course)
        return nextS


class DesiredSchedule(schedule):
    MaxCredits = 20

    def __init__(self, sch, TC=0, Clst=[]):

        self.schedule = sch.schedule  # Mon-Saturday
        self.finalTime = sch.finalTime
        self.initialTime = sch.initialTime
        self.TotalCredits = TC
        self.ReqCourseList = Clst
        self.CourseList = sch.CourseList  # Contains Course IDs of those in schedule
        # self.MaxCredits = 20

    def nextSchedule(self, course):  # make sub class of course
        if self.TotalCredits + course.credits > DesiredSchedule.MaxCredits:
            return 'Max credits reached'

        nextS = copy.deepcopy(self)

        for times in course.Time:
            day, startTime, endTime = times
            # print('day: ',day)
            crs = CourseAtDay(day, course)
            # print(course.Title, endTime, startTime)
            if endTime > self.finalTime or startTime < self.initialTime:
                return ("Out of Schedule Bounds"), None
            else:
                if len(self.schedule[day]) == 0:  # If No courses that day
                    nextS.addCourse(crs)
                else:

                    lst = self.schedule[day]  # Needs fixing: Only used once, rather use lst always or don't
                    if endTime < lst[0].Time[1]:  # start time of first course of the day greater than end time
                        nextS.addCourse(crs, 0)

                    else:
                        Len = len(lst)
                        i = 0
                        # print('  ', self.schedule)
                        while i < Len and self.schedule[day][i].Time[1] <= startTime:
                            # print(self.schedule[i])
                            i += 1

                        if i == Len:

                            if self.schedule[day][i - 1].Time[2] <= startTime:
                                nextS.addCourse(crs, i)
                            else:
                                return ClashReport(crs, self.schedule[day][i - 1], day)  # Clash
                        else:
                            if self.schedule[day][i - 1].Time[2] < startTime:
                                if self.schedule[day][i].Time[1] > endTime:
                                    nextS.addCourse(crs, i)

                                else:
                                    return ClashReport(crs, self.schedule[day][i], day)  # Clash
                            else:
                                return ClashReport(crs, self.schedule[day][i - 1], day)  # Clash
        nextS.CourseList.append(course)
        nextS.TotalCredits += course.credits
        return nextS


class PossibilityTree():

    def __init__(self, d=[[], [], [], [], [], []]):
        self.data = d
        self.children = []

    def Initiate(self, sectionsList):
        sch = schedule()
        self.data = sch
        self.GenerateTree(sectionsList, 0, len(sectionsList), sch)

    def addChild(self, child):
        self.children.append(child)

    def GenerateTree(self, sectionsList, i, LEN, root):
        if type(root) is schedule:
            if i < LEN:
                crsList = sectionsList[i]
                for j in range(len(crsList)):
                    nextSch = root.nextSchedule(crsList[j])
                    child = PossibilityTree(nextSch)
                    self.addChild(child)
                    self.children[j].GenerateTree(sectionsList, i + 1, LEN, nextSch)

    def GenerateAllPosb(self, crsList):
        NumOfDes = len(crsList)  # Number of desired courses
        DS = self.data  # Asumming this is of type desiredSchedule
        # print(crsList)
        # print('NumOfDes:',NumOfDes) # T
        for i in range(NumOfDes):
            # print('i1',i) # T
            # print('crsList[i]',j,crsList[i])
            j = 0
            while j < len(crsList[i]):
                # print('crsList[i]',j,crsList[i])
                sec = crsList[i][j]
                nextS = DS.nextSchedule(sec)
                # print(sec.Title)
                # print(nextS, j) # T
                # print()
                if type(nextS) is DesiredSchedule:
                    child = PossibilityTree(nextS)
                    self.addChild(child)  # T
                    # print('added')
                    j += 1
                else:
                    crsList[i].remove(sec)

        # print('Children',self.children)
        k = 0

        NumOfDes = len(crsList)
        # print(crsList)
        for i in range(NumOfDes):
            NumChilds = len(self.children)
            NumOfSec = len(crsList[i])
            # print('hello', NumOfSec)  # T
            # print(NumOfSec)
            for j in range(k, k + NumOfSec):
                # print(i,j)
                # print('Children',self.children)
                self.children[j].GenerateAllPosb(crsList[i + 1:])
            k = k + NumOfSec

    def addNodePath(self, path):  # called from root node

        if self.data == None:

            self.data = path[0]

            self.adder(path[1:])

        elif self.data == path[0]:

            self.adder(path[1:])

        else:
            raise ValueError("Incorrect Path Input")

    def adder(self, path):
        if len(path) == 0:  # File is already present
            return

        for c in self.children:
            if c.data == path[0]:
                return c.adder(path[1:])  # perform next adding and end current function

        # if not found insert path into children
        self.insertPath(path)

    def insertPath(self, path):
        # print(path)

        if len(path) == 0:  # Stop if all p
            return None
        child = SimpleTree(path[0])
        self.children.append(child)
        child.insertPath(path[1:])

    def getSchedules(self):  # For start Node
        lst = []
        for c in self.children:
            lst.extend(c.GetAllSchedules())
        return lst

    def GetAllSchedules(self):
        lst = [self.data]
        for c in self.children:
            lst.extend(c.GetAllSchedules())
        return lst

    def getDesiredSchedules(self):
        lst = []
        for c in self.children:
            for gc in c.children:
                lst.extend(gc.GetAllSchedules())
        return lst

    def PrintAllSchedules(self, schedules=None):
        if schedules == None:
            schedules = self.getSchedules()
        for sch in schedules:
            print('-' * 8)
            print(sch.CourseList)
            print()
            sch.printSchedule()

    def PrintDesiredSchedules(self):
        schedules = self.getDesiredSchedules()
        self.PrintAllSchedules(schedules)

    def Preorder(self):
        print('-' * 8)
        print(self.data.CourseList)
        print()
        self.data.printSchedule()

        for i in self.children:
            i.Preorder()

    def count(self):
        # c += 1
        c = 1
        for i in self.children:
            c += i.count()

        return c

    def getLeafs(self):
        PossibleSchedules = []
        reports = []
        if len(self.children) == 0:
            if type(self.data) is schedule:  # or type(self.data) is DesiredSchedule:
                PossibleSchedules.append(self.data)
            else:  # type(key) is ClashReports or type(key) is Reports:
                reports.append(self.data)

        else:
            for c in self.children:
                ps, r = c.getLeafs()
                PossibleSchedules.extend(ps)
                reports.extend(r)

        return PossibleSchedules, reports,

    def SearchPath(self, key):  # Assumes item is in the list
        lst = []
        # print('Inside Function', self.data) # test
        if self.data == None:
            print(self.data, 'returning None')
            return None
        elif self.data == key:
            print(self.data, 'returning []')
            return []
        else:
            for c in self.children:
                rv = c.SearchPath(key)
                if isinstance(rv, list):
                    print(self.data, 'returning data')
                    rv.append(self.data)
                    print(rv)
                    return rv
        return []


# Runs other file

# file = open('Anand.py').read()
# exec(file)


times = [(0, timedelta(hours=12, minutes=30), timedelta(hours=13, minutes=20)),
         (2, timedelta(hours=12, minutes=30), timedelta(hours=13, minutes=20))]

times2 = [(1, timedelta(hours=14, minutes=30), timedelta(hours=15, minutes=30)),
          (3, timedelta(hours=14, minutes=30), timedelta(hours=15, minutes=20))]

times3 = [(0, timedelta(hours=17, minutes=20), timedelta(hours=18, minutes=30)),
          (2, timedelta(hours=17, minutes=32), timedelta(hours=18, minutes=30)),
          (4, timedelta(hours=17, minutes=32), timedelta(hours=18, minutes=30))]

phy = Course('Physics Mechanics', 'Phy101-L1', 'Lee Hang', times, 2)

phyL2 = Course('Physics Mechanics', 'Phy101-L2', 'Lee Hang', times2, 2)

# for j in phy.search_time(0):
#   print(j)
EM = Course('Electro-Magnetism', 'EM203-L1', 'Han Lee yung', times3, 2)

chem = Course(
    'Chemistry 101',
    'Chem101-L1',
    'Maham Haider',
    [
        (0, timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=45))]
    , 3)

chem2 = Course(
    'Chemistry 101',
    'Chem101-L2',
    'Maham Haider',
    [
        (2, timedelta(hours=13, minutes=30), timedelta(hours=14, minutes=45))]
    , 3)
eca = Course('Electric Circuit Analysis Course', 'EE101-L1', 'Lee Hang',
             [(0, timedelta(hours=14, minutes=30), timedelta(hours=15, minutes=20))], 4)

eca1 = Course('Electric Circuit Analysis Course', 'EE101-L2', 'Tariq Mumtaz',
              [(0, timedelta(hours=9, minutes=30), timedelta(hours=13, minutes=20))], 4)

sectionsLst = [[phy, phyL2], [EM], [chem, chem2], [eca, eca1]]  # of Must haves

photo = Course('Intro to Photography', 'PHOTO101-L1', 'Lee Hang',
               [(0, timedelta(hours=14, minutes=00), timedelta(hours=16, minutes=00))], 1)

photo2 = Course('Intro to Photography', 'PHOTO101-L2', 'Lee Wanink',
                [(4, timedelta(hours=14, minutes=00), timedelta(hours=16, minutes=00))], 1)

CShistory = Course('CS history ', 'CS105-L1', 'Kakashi',
                   [(0, timedelta(hours=12, minutes=30), timedelta(hours=13, minutes=20)),
                    (2, timedelta(hours=12, minutes=30), timedelta(hours=13, minutes=20))], 2)

CShistory2 = Course('CS history ', 'CS105-L2', 'Kakashi',
                    [(0, timedelta(hours=13, minutes=30), timedelta(hours=14, minutes=20)),
                     (2, timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=20))], 2)

ElectivesList = [[photo, photo2], [CShistory, CShistory2]]
# Of Desired Courses

# Temp for testing
Lst = [phy, EM, chem, eca]  # of Must haves
sch = schedule()
for i in Lst:
    sch = sch.nextSchedule(i)
sch.printSchedule()

exec(open('OpFunctions.py').read())

tree = PossibilityTree()
tree.Initiate(sectionsLst)
PS, reports = tree.getLeafs()
ReqSchCount = len(PS)
print()

'''
print("Required Course's Schedules Possibilities:",'\n',)
print("Number of Must have Schedules:",ReqSchCount,'\n')

for s in PS:
    s.printSchedule()
    print('-' * 8)
print()

print('Clash Reports Uptil Now:','\n')
for i in ClashReport.Reports:
    i.printSchedule()
'''
# for r in reports:
#     r.printSchedule()

# for x in PS[0].schedule[0]:
#     print(x.Title, x.Time[1])


tree = PossibilityTree('S')

for s in PS:
    root = PossibilityTree(DesiredSchedule(s))
    root.GenerateAllPosb(ElectivesList)
    tree.addChild(root)
DesCount = tree.count() - ReqSchCount - 1
print()
print("Desired Course's Schedules Possibilities:", '\n', )
print("Number of Wanted Schedules:", DesCount, '\n')
tree.PrintDesiredSchedules()

# for s in PS:
#     s.printSchedule()
#     print('-' * 8)
# print()
print('Clash Reports (Final):', '\n')
for i in ClashReport.Reports:
    i.printSchedule()

print()
print('Number of Total Possible Schedules:', DesCount + ReqSchCount)
print()

l = HierarchyLevels(tree.getSchedules())
l.nextLevel(HasFaculty, ['Intro to Photography', 'Lee Wanink'])
# l.nextLevel(InCreditRange,[2,5])
l.nextLevel(HasCourse, ['CS history'])
l.printLevels()
print()
print('get all levels', l.getAllLevels())
print()


# print(l.Finished)


def pattern():
    a = ''
    for n in range(7):
        a += (n * ' ' + '*' + '*' * 2 * (6 - n) + '*' + ' ' * n) * 4 + '\n'
    for n in range(6, -1, -1):
        a += (n * ' ' + '*' + '*' * 2 * (6 - n) + '*' + ' ' * n) * 4 + '\n'
    print(a)


pattern()

sch = PS[0]

# t1 = timedelta(hours = 10,minutes = 30)
# t2 = timedelta(hours = 21,minutes = 35)
# t3 = timedelta(hours = 0,minutes = 30)

# t4 = (t2-t1)/(t3)
# print(t4)
# print((t1-sch.initialTime)/t3)

pref = dict()
pref['Saturday Off'] = SaturdayOff, []
pref['Has Faculty Tariq Mumtaz'] = HasFaculty, ['Electric Circuit Analysis Course', 'Tariq Mumtaz']

PrefList = ['Saturday Off', 'Has Faculty Tariq Mumtaz']

schLevels = HierarchyLevels(tree.getSchedules())
for p in PrefList:
    schLevels.nextLevel(*pref[p])
    if schLevels.Finished == True:
        break

schLevels.printLevels()

m_initial = ['Calculus II', 'Advanced Differential Equation', 'Data Structures & Algorithms']

MustHaveCrs = []
sectionsList = []
for t in m_initial:
    sec = updated_cl[t]

    lst = []

    for par in sec:
        t = []
        start = convert_to_24_time(par[6])
        end = convert_to_24_time(par[7])
        for d in Day_Num(par[5]):
            t.append((d, start, end))
        crs = Course(title=par[3],

                     Id=par[0], Type=par[2],
                     c=par[4], cr=par[8],

                     sec=par[1], inst=par[10],
                     times=t
                     )
        # for y in MustHaveCrs:
        #   if len(y) != 0:

        lst.append(crs)
    sectionsList.append(lst)

print('   here')
for i in sectionsList:
    print(len(i))
    for j in i:
        print(j.Title, j.Section)

print(sectionsList[0][0].Time)

tree = PossibilityTree()
tree.Initiate(sectionsList)
PS, reports = tree.getLeafs()
ReqSchCount = len(PS)
print()

print("Required Course's Schedules Possibilities:", '\n', )
print("Number of Must have Schedules:", ReqSchCount, '\n')

for s in PS:
    s.printSchedule()
    print('-' * 8)
print()

print('Clash Reports Uptil Now:', '\n')
for i in ClashReport.Reports:
    i.printSchedule()

for j in PS[0].getList():
    print(j)

t1 = timedelta(hours=18, minutes=20)
print(str(t1))