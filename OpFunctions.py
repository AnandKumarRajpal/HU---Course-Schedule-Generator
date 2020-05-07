def DayAvgGap(day):  # day is a list containing the times
    if len(day) <= 1:
        # return timedelta(hours = 0,minutes =0)
        return None
    else:
        gaps = timedelta(hours=0, minutes=0)
        LEN = len(day)
        for i in range(LEN - 1):
            gap = day[i + 1].Time[1] - day[i].Time[2]
            gaps += gap

        avg = gaps / (LEN - 1)
        return avg


def DayMaxGap(day):
    if len(day) <= 1:
        return timedelta(hours=0, minutes=0)
    else:
        Max = timedelta(hours=0, minutes=0)
        LEN = len(day)
        for i in range(LEN - 1):
            gap = day[i + 1].Time[1] - day[i].Time[2]
            if gap > Max:
                Max = gap

        return Max


def TotalDayTime(day):
    total = timedelta(hours=0, minutes=0)
    for c in day:
        time = c.Time[2] - c.Time[1]
        total += time

    return total


# def WeeklyTotalHours():
#   total = timedelta(hours = 0,minutes =0)
#   for i in range(len(sectionsList)):


def DayStartTime(sch, day):
    if len(sch[day]) == 0:
        return None
    else:
        return sch[day][0].Time[1]


def DayEndTime(sch, day):
    if len(sch.schedule[day]) == 0:
        return None
    else:
        return sch.schedule[day][-1].Time[1]


# DayGapAverage(sch.schedule[0])


def WeeklyLargeGaps(wkSch, Gaptime=timedelta(hours=5, minutes=0)):
    n = 0
    for day in wkSch:
        if DayMaxGap(day) >= Gaptime:
            n += 1
    return n


def WithinGapLimit(sch, perc=0.65, Gaptime=timedelta(hours=5, minutes=0)):
    wk = sch.schedule
    total = daysOnOff(wk)[0]
    n = WeeklyLargeGap(wkSch, GapTime)
    percentage

    if percentage >= perc:
        return True
    else:
        return False


def DaysOff(wkSch):
    daysList = []
    for day in range(5):
        if len(wkSch[day]) == 0:
            daysList.append(day)
    return daysList


def DaysOn(wkSch):
    daysList = []
    for day in range(5):
        if len(wkSch[day]) > 0:
            daysList.append(day)
    return daysList


def AverageDailyHours(wk):
    total_WkTime = timedelta(hours=0, minutes=0)
    n = 0
    for day in wk:
        if len(day) != 0:
            total_WkTime += TotalDayTime(day)
            n += 1
    return (total_WkTime / n)


earlyRange = [timedelta(hours=7, minutes=30), timedelta(hours=10, minutes=00)]
lateRange = [timedelta(hours=4, minutes=00), timedelta(hours=6, minutes=30)]


def daysOnOff(wk):
    on = 0
    off = 0

    for day in range(5):
        if len(wk[day]) > 0:
            on += 1
        else:
            off += 1

    return on, off


# Following funcs have not been tested

def StartEndInRange(sch, day, StartRange, EndRange):
    st = DayStartTime(sch, day)
    if StartRange[0] <= st <= StartRange[1]:
        et = DayEndTime(sch, day)
        if EndRange[0] <= et <= EndRange[1]:
            return True

    return False


def DaysWithinStartEndRanges(sch, percent, StartRange, EndRange):
    wk = sch.schedule
    c = 0
    t = 0
    for day in daysOn(wk):
        if StartEndInRange(sch, day, StartRange, EndRange):
            c += 1
        t += 1

    if (c / t) > percent:
        return True
    else:
        return False


def InUnpreferedRange(sch, day, low, high):  # where range is tuple (day,startTime,endTime)
    crs = sch.InRangeOfDay(sch, day, low, high)
    if len(crs) == 0:
        return True
    else:
        return False


def WorkingDaysOff(sch, n):
    if daysOnOff(sch.schedule)[1] >= n:
        return True
    else:
        return False


def InCreditRange(sch, lower, upper):
    if sch.TotalCredits >= lower and sch.TotalCredits <= upper:
        return True
    else:
        return False


def HasCourse(sch, crsName):  # tested
    for course in sch.CourseList:
        if course.Title == crsName:
            return True
        else:
            return False

    # if course not found
    return False


def HasMinDaysOff(sch):
    pass


def HasSection(sch, crsName, sec):  # Won't be needed
    for course in sch.CourseList:
        if course.Title == crsName:
            if course.Section == sec:
                return True
            else:
                return False

    # if course not found
    return False


def HasFaculty(sch, crsName, inst):  # tested
    for course in sch.CourseList:
        if course.Title == crsName:
            if course.Instructor == inst:
                return True
            else:
                return False

    # if course not found
    return False


def SaturdayOff(sch):
    if len(sch.schedule[-1]) == 0:
        return True
    else:
        return False


print('\n' * 6)
n = HasSection
l = ['Electric Circuit Analysis Course', 6]
# print(n(sch, *l))


class HierarchyLevels:

    def __init__(self, values=[]):
        self.levels = [values]
        self.Finished = False

    def nextLevel(self, func, param):
        lst = []
        i = 0
        while i < (len(self.levels[-1])):
            if func(self.levels[-1][i], *param) == True:

                data = self.levels[-1].pop(i)
                lst.append(data)
            else:
                i += 1
        if len(lst) == 0:
            self.Finished = True
        else:
            self.levels.append(lst)

    def UpgradeLevel(self, func, param):
        lst = []
        i = 0
        while i < (len(self.levels[-1])):
            if func(self.levels[-1][i], *param) == True:

                data = self.levels[-1].pop(i)
                lst.append(data)
            else:
                i += 1
        if len(lst) == 0:
            self.Finished = True
        else:
            self.levels[-1] = lst

    def getTopLevel(self):
        return self.levels[-1]

    def getAllLevels(self):
        lst = []
        for x in (self.levels[::-1]):
            lst.extend(x)
        return lst

    def NumOfLevels(self):
        return len(self.levels)

    def printLevels(self):
        for l in range(len(self.levels)):
            print('     Level', l, ':')
            print('   ', self.levels[l])

    def printSchedules(self):
        for l in range(len(self.levels)[::-1]):
            print('Level', l, ':')
            for s in self.levels[l]:
                s.printSchedule()
            print('-' * 8)
            print()