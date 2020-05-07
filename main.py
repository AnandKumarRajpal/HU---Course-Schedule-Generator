from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import TkTreectrl as treectrl
from PIL import Image as I
from PIL import ImageTk, ImageSequence
import csv
from datetime import timedelta
import copy
exec(open('OpFunctions.py').read())



def Main2(m_initial, updated_cl):
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


    tree = PossibilityTree()
    tree.Initiate(sectionsList)
    PS, reports = tree.getLeafs()
    ReqSchCount = len(PS)
    print()

    print("Required Course's Schedules Possibilities:", '\n', )
    print("Number of Must have Schedules:", ReqSchCount, '\n')


    listOfSchedules = []
    for s in PS:
        listOfSchedules.append( s.getList())
        print('-' * 8)
    print()

    print('Clash Reports Uptil Now:', '\n')
    for i in ClashReport.Reports:
        i.printSchedule()

    return listOfSchedules

########################################## Frontend ################################

def LoadData(filename):
  Records = csv.reader(open(filename))# This function does not split the title like before
  dataset = []
  for rec in Records:
    dataset.append(tuple(rec))
  return dataset

courses = LoadData(r'C:\\Users\\anand\\Desktop\\Copy.csv') #Provide path to courses excel sheet
courses.pop(0)

updated_cl = {}
updated_cl[courses[0][3]] = [courses[0]]
current = courses[0][3]
for element in courses:
    if element[3] == current:
        if element not in updated_cl[element[3]]:
            updated_cl[element[3]] += [element]
    else:
        updated_cl[element[3]] = [element]
        current = element[3]

final_list = []
must_have_list = []
desired = []
m_initial = []

def final_output():
    global must_have_list
    global desired
    global m_initial
    for k in fc_lbox1.get(0, 'end'):
        must_have_list.append(k)
    for l in fc2_lbox.get(0,'end'):
        desired.append(l)
    listofschedules = Main2(m_initial, updated_cl)
    print("HERE",listofschedules)
    print('ok')
    exec(open('Output.py').read())

def scr2_to_scr4():
    for element in fc_lbox3.get(0, 'end'):
        fc2_lbox.insert(END, element)

def raise_frame(frame):
    global m_initial
    frame.tkraise()
    # for scren2 to clear list everytime
    fc_lbox.delete(0, 'end')
    for item in sel:
        m_initial.append(item)
        for i in range(len(updated_cl[item])):
            fc_lbox.insert(END, updated_cl[item][i][0], updated_cl[item][i][1], updated_cl[item][i][2], updated_cl[item][i][3], updated_cl[item][i][4], updated_cl[item][i][5], updated_cl[item][i][6], updated_cl[item][i][7], updated_cl[item][i][8], updated_cl[item][i][9], updated_cl[item][i][10])
    # for screen3 to get final course list
    for item in sel2:
        for i in range(len(updated_cl[item])):
            fc1_lbox.insert(END, updated_cl[item][i][0], updated_cl[item][i][1], updated_cl[item][i][2],
                           updated_cl[item][i][3], updated_cl[item][i][4], updated_cl[item][i][5],
                           updated_cl[item][i][6], updated_cl[item][i][7], updated_cl[item][i][8],
                           updated_cl[item][i][9], updated_cl[item][i][10])
    global final_list
    final_list = []
    final_list.append(fc_lbox1.get(0, 'end'))

s = {}
def selected():
    for i in fc_lbox.curselection():
        a = fc_lbox.get(i)
        s[a[0][3]+' '+a[0][2]+' '+a[0][1]] = a[0]
        fc_lbox1.insert(END, a[0][3]+' '+a[0][2]+' '+a[0][1])
        fc_lbox.delete(i)
    for i in fc1_lbox.curselection():
        a = fc1_lbox.get(i)
        s[a[0][3]+' '+a[0][2]+' '+a[0][1]] = a[0]
        fc2_lbox.insert(END, a[0][3]+' '+a[0][2]+' '+a[0][1])
        fc1_lbox.delete(i)
    for i in time_lbox.curselection():
        if time_lbox.get(i)[0][0] == 'Unpreffered Time':
            d = askstring('Unpreffered Time', 'Please enter your unpreffered time. (Format = Start Time, End Time E.g. 8:30a, 9:30a)')
            s[d] = (InUnpreferedRange, d)
            b = time_lbox.get(i)
            fc_lbox1.insert(END, 'UNPREFFERED TIME')
        if time_lbox.get(i)[0][0] == 'Start Range':
            d = askstring('Start Range', 'Please enter the time you want to start your courses at and end your courses before that. (Format = Start Time, End Time E.g. 8:30a, 9:30a)')
            d = d.split(',')
            s[d] = (DaysWithinStartEndRanges, d[0], d[1])
            b = time_lbox.get(i)
            fc_lbox1.insert(END, 'START RANGE, END RANGE')
        if time_lbox.get(i)[0][0] == 'Maximum Gap Time':
            d = askstring('Maximum Gap Time', 'Please enter the maximum number of gap hours and the percentage for the week it holds true. (Format = Hours, Percentage E.g. 8, 80%)')
            d = d.split(',')
            print(str(d[1][1])+str(d[1][2]), d[0])
            s[d] = (WithinGapLimit, int(str(d[1][1])+str(d[1][2]))/100, d[0])
            b = time_lbox.get(i)
            fc_lbox1.insert(END, 'GAP TIME')
        if time_lbox.get(i)[0][0] == 'Minimum Days Off':
            s['MINIMUM DAYS OFF'] = askstring('Minimum Days Off', 'Please enter the minimum number of working days you want an off. (Format = No. of Days, E.g. 2)')
            b = time_lbox.get(i)
            fc_lbox1.insert(END, 'MINIMUM DAYS OFF')
        time_lbox.selection_clear(0, END)


def selected1():
    for i in fc_lbox.curselection():
        a = fc_lbox.get(i)
        s[a[0][3]+' '+a[0][2]+' '+a[0][1]] = a[0]
        fc_lbox3.insert(END, a[0][3]+' '+a[0][2]+' '+a[0][1])
        fc_lbox.delete(i)
    for i in time_lbox.curselection():
        if time_lbox.get(i)[0][0] == 'Unpreffered Time':
            d = askstring('Unpreffered Time', 'Please enter your unpreffered time. (Format = Start Time, End Time E.g. 8:30a, 9:30a)')
            s[d] = (InUnpreferedRange, d)
            b = time_lbox.get(i)
            fc_lbox3.insert(END, 'UNPREFFERED TIME')
        if time_lbox.get(i)[0][0] == 'Start Range':
            d = askstring('Start Range', 'Please enter the time you want to start your courses at and end your courses before that. (Format = Start Time, End Time E.g. 8:30a, 9:30a)')
            d = d.split(',')
            s[d] = (DaysWithinStartEndRanges, d[0], d[1])
            b = time_lbox.get(i)
            fc_lbox3.insert(END, 'START RANGE, END RANGE')
        if time_lbox.get(i)[0][0] == 'Maximum Gap Time':
            d = askstring('Maximum Gap Time', 'Please enter the maximum number of gap hours and the percentage for the week it holds true. (Format = Hours, Percentage E.g. 8, 80%)')
            d = d.split(',')
            s[d] = (WithinGapLimit, int(d[1][:-1])/100, d[0] )
            b = time_lbox.get(i)
            fc_lbox3.insert(END, 'GAP TIME')
        if time_lbox.get(i)[0][0] == 'Minimum Days Off':
            s['MINIMUM DAYS OFF'] = askstring('Minimum Days Off', 'Please enter the minimum number of working days you want an off. (Format = No. of Days, E.g. 2)')
            b = time_lbox.get(i)
            fc_lbox3.insert(END, 'MINIMUM DAYS OFF')
        time_lbox.selection_clear(0, END)

def deselected():
    for i in fc_lbox1.curselection():
        a = fc_lbox1.get(i)
        if a == 'UNPREFFERED TIME' or a == 'START RANGE, END RANGE' or a == 'END RANGE' or a == 'GAP TIME' or a == 'MINIMUM DAYS OFF':
            fc_lbox1.delete(i)
        else:
            fc_lbox.insert(END, s[a][0], s[a][1],s[a][2],s[a][3],s[a][4],s[a][5],s[a][6],s[a][7],s[a][8],s[a][9],s[a][10])
            fc_lbox1.delete(i)
    for i in fc_lbox3.curselection():
        a = fc_lbox3.get(i)
        if a == 'UNPREFFERED TIME' or a == 'START RANGE, END RANGE' or a == 'END RANGE' or a == 'GAP TIME' or a == 'MINIMUM DAYS OFF':
            fc_lbox3.delete(i)
        else:
            fc_lbox.insert(END, s[a][0], s[a][1], s[a][2], s[a][3], s[a][4], s[a][5], s[a][6], s[a][7], s[a][8],
                           s[a][9], s[a][10])
            fc_lbox3.delete(i)
    for i in fc2_lbox.curselection():
        a = fc2_lbox.get(i)
        fc1_lbox.insert(END, s[a][0], s[a][1], s[a][2], s[a][3], s[a][4], s[a][5], s[a][6], s[a][7], s[a][8],
                           s[a][9], s[a][10])
        fc2_lbox.delete(i)

#for search on first page:
sel=list()
sel2 = list()

# First page:
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='white')

        self.grid(row=0, column=0, sticky='news')
        self.create_widgets()

    def CurSelet(self,evt):
        global sel
        temp=list()
        for i in self.lbox.curselection():
            temp.append(self.lbox.get(i))

        allitems=list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel:
            if i in allitems:
                if i not in temp:
                    sel.remove(i)

        for x in self.lbox.curselection():
            if self.lbox.get(x) not in sel:
                sel.append(self.lbox.get(x))

    def select(self):
        global sel
        s=', '.join(map(str,sel))
        self.cursel.set('Current Selection: '+s)

    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        #logo_frame
        self.logo_frame = Frame(self, bg='white')
        self.logo = PhotoImage(file='logo_new.png')
        self.logo_label = Label(self.logo_frame, image=self.logo, bg='white').pack(side=LEFT, fill=X)
        self.Label1 = Label(self.logo_frame, text='HU - Course Schedule Generator', font='Times 20', bg='white').pack(side=LEFT, expand=YES,fill=X)
        self.logo_frame.pack(fill=X, side='top')
        #frame with label2:
        self.frame1 = Frame(self, bg='white')
        self.Label2 = Label(self.frame1, text='Please select your courses from the list below:', font='Times 15', bg='white')
        self.Label2.pack(side='left', padx=(0, 100))
        self.frame1.pack(fill=X, side='top')
        #frame for search box:
        self.search_frame = Frame(self, bg='white')
        self.entry = Entry(self.search_frame, textvariable=self.search_var, width=13)
        self.search_label = Label(self.search_frame, text='Search:', bg='white')
        self.entry.pack(side='right', padx=(0, 5))
        self.search_label.pack(side='right')
        self.search_frame.pack(fill=X)
        #frame for list of courses with search
        self.frame = Frame(self, bg='white')
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.lbox = Listbox(self.frame, selectmode=MULTIPLE, yscrollcommand=self.scrollbar.set, bg='white', height=15)
        self.lbox.bind('<<ListboxSelect>>',self.CurSelet)
        self.scrollbar.config(command=self.lbox.yview)
        self.lbox.config(yscrollcommand=self.scrollbar.set)
        self.lbox.pack(side='left', fill=X, expand=1)
        self.scrollbar.pack(side="right", fill="y")
        self.frame.pack(side='top', fill=X)

        self.cursel = StringVar()
        self.lb1 = Label(self, textvariable=self.cursel, bg='white')
        self.lb1.pack(side='left')
        self.button_frame = Frame(self, bg='white', width=700)
        # next screen button
        self.next = Button(self.button_frame, text='Next', command=lambda: raise_frame(screen2)).pack(side='right', padx=(0,10), pady=(10,10))
        #submit course button
        self.btn=Button(self.button_frame,text='Submit selected courses', command=self.select, width=20).pack(side='right', padx=(0,10), pady=(10,10))
        self.button_frame.pack(fill=BOTH, expand=YES)
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self):
        global sel
        global l
        search_term = self.search_var.get()

        self.lbox.delete(0, END)
        j = 1
        for item in updated_cl:
                if search_term.lower() in item.lower():
                    self.lbox.insert(END, item)
                    j += 1

        allitems=list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel:
            if i in allitems:
                self.lbox.select_set(self.lbox.get(0, "end").index(i))
        if self.lbox.size() == 0:
            self.error = messagebox.showinfo('Error', 'No course found.')


class Application1(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='white')

        self.grid(row=0, column=0, sticky='news')
        self.create_widgets()

    def CurSelet(self,evt):
        global sel2
        temp=list()
        for i in self.lbox.curselection():
            temp.append(self.lbox.get(i))

        allitems=list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel2:
            if i in allitems:
                if i not in temp:
                    sel2.remove(i)

        for x in self.lbox.curselection():
            if self.lbox.get(x) not in sel2:
                sel2.append(self.lbox.get(x))

    def select(self):
        global sel2
        s=', '.join(map(str,sel2))
        self.cursel.set('Current Selection: '+s)

    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        #frame with label2:
        self.frame1 = Frame(self, bg='white')
        self.Label2 = Label(self.frame1, text='Please select your electives from the list below:', font='Times 15', bg='white')
        self.Label2.pack(side='left', padx=(0, 100))
        self.frame1.pack(fill=X, side='top', expand=YES)
        #frame for search box:
        self.search_frame = Frame(self, bg='white')
        self.entry = Entry(self.search_frame, textvariable=self.search_var, width=13)
        self.search_label = Label(self.search_frame, text='Search:', bg='white')
        self.entry.pack(side='right', padx=(0, 5))
        self.search_label.pack(side='right')
        self.search_frame.pack(fill=X)
        #frame for list of courses with search
        self.frame = Frame(self, bg='white')
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.lbox = Listbox(self.frame, selectmode=MULTIPLE, yscrollcommand=self.scrollbar.set, bg='white', height=28)
        self.lbox.bind('<<ListboxSelect>>',self.CurSelet)
        self.scrollbar.config(command=self.lbox.yview)
        self.lbox.config(yscrollcommand=self.scrollbar.set)
        self.lbox.pack(side='left', fill=X, expand=1)
        self.scrollbar.pack(side="right", fill="y")
        self.frame.pack(side='top', fill=X)

        self.cursel = StringVar()
        self.lb1 = Label(self, textvariable=self.cursel, bg='white')
        self.lb1.pack(side='left')
        self.button_frame = Frame(self, bg='white', width=700)
        # next screen button
        self.next = Button(self.button_frame, text='Next', command=lambda: raise_frame(screen5)).pack(side='right', padx=(0,10), pady=(10,10))
        #submit course button
        self.btn=Button(self.button_frame,text='Back', command=lambda: raise_frame(screen2), width=20).pack(side='right', padx=(0,10), pady=(10,10))
        self.button_frame.pack(fill=BOTH, expand=YES)
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self):
        global sel2
        global l
        search_term = self.search_var.get()

        self.lbox.delete(0, END)
        j = 1
        for item in updated_cl:
                if search_term.lower() in item.lower():
                    self.lbox.insert(END, item)
                    j += 1

        allitems=list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel2:
            if i in allitems:
                self.lbox.select_set(self.lbox.get(0, "end").index(i))
        if self.lbox.size() == 0:
            self.error = messagebox.showinfo('Error', 'No course found.')







root = Tk()
root.configure(background='white')
root.title('HU - Course Schedule Generator')


#Screen 5:
screen5 = Frame(root, width=800, height=550, bg='white')
c1_frame = Frame(screen5, bg='white')
c1_Label = Label(c1_frame, text='Please select the courses in order of preference, from highest to lowest, i.e. select the course with highest priority first.', font='Times 15', bg='white').pack(side='left')
c1_frame.pack(fill=BOTH)

fc1_frame = Frame(screen5, bg='white')
scrollbarfc1 = Scrollbar(fc1_frame, orient=VERTICAL)
fc1_lbox = treectrl.MultiListbox(fc1_frame, yscrollcommand=scrollbarfc1.set, height=215,width=1200, bg='white')
fc1_lbox.config(columns=('Course code', 'Section', 'Type', 'Course title', 'Credit hours', 'Day', 'Start time', 'End', 'Classroom', 'CourseID', 'Instructor'))
scrollbarfc1.config(command=fc1_lbox.yview)
fc1_lbox.config(yscrollcommand=scrollbarfc1.set)
fc1_lbox.pack(side='left', fill=X)
scrollbarfc1.pack(side="right", fill="y")
fc1_frame.pack(side='top', fill=X)

lu1_frame = Frame(screen5, bg='white')
down1 = Button(lu1_frame, text='Delete', command=deselected).pack(side='right', padx=(0,10), pady=(10,10))
up2 = Button(lu1_frame, text='Select', command=selected).pack(side='right', padx=(0,10), pady=(10,10))
lu1_frame.pack()

fc2_frame = Frame(screen5, bg='white')
scrollbarfc2 = Scrollbar(fc2_frame, orient=VERTICAL)
fc2_lbox = Listbox(fc2_frame, yscrollcommand=scrollbarfc1.set,width=200, height=13, bg='white')
scrollbarfc2.config(command=fc2_lbox.yview)
fc2_lbox.config(yscrollcommand=scrollbarfc2.set)
fc2_lbox.pack(side='left', fill=X)
scrollbarfc2.pack(side="right", fill="y")
fc2_frame.pack(side='top', fill=X)

#buttons to go to next screen screen3:
nexts5_frame = Frame(screen5, bg='white')
nexts5 = Button(nexts5_frame, text='Next', command=lambda: raise_frame(screen3)).pack(side='right', padx=(0,10), pady=(10,10))
submits5 = Button(nexts5_frame, text='Submit', command=final_output).pack(side='right', padx=(0,10), pady=(10,10))
backs2 = Button(nexts5_frame, text='Back', command=lambda: raise_frame(Application1(master=root))).pack(side='right', padx=(0,10), pady=(10,10))
nexts5_frame.pack(fill=X)
screen5.grid(row=0, column=0, sticky='news')

#Screen 4:
Application1(master=root)


#Screen 3;
screen3 = Frame(root, width=800, height=550, bg='white')
#loading screen
class App:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(parent, width=1000, height=550, bg='white')
        self.canvas.pack()
        self.sequence = [ImageTk.PhotoImage(img) for img in
                         ImageSequence.Iterator(I.open('Loading-Gif.gif'))]
        self.image = self.canvas.create_image(500, 275, image=self.sequence[0])
        self.loading = self.canvas.create_text(500, 400, text='Generating possibilities, Please, wait!', font='Times 15', fill='purple')
        self.animate(1)

    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        self.parent.after(10, lambda: self.animate(((counter + 1) % len(self.sequence))))

app = App(screen3)
screen3.grid(row=0, column=0, sticky='news')

#Screen 2:
screen2 = Frame(root, bg='white')
# frame with entry and label2:
c_frame = Frame(screen2, bg='white')
c_Label = Label(c_frame, text='Please select the courses in order of preference, from highest to lowest, i.e. select the course with highest priority first.', font='Times 15', bg='white').pack(side='left')
c_frame.pack(fill=BOTH, expand=YES)

# frame for list of courses with search
fc_frame = Frame(screen2, bg='white')
scrollbar = Scrollbar(fc_frame, orient=VERTICAL)
fc_lbox = treectrl.MultiListbox(fc_frame, yscrollcommand=scrollbar.set, height=200,width=850, bg='white')
fc_lbox.config(columns=('Course code', 'Section', 'Type', 'Course title', 'Credit hours', 'Day', 'Start time', 'End', 'Classroom', 'CourseID', 'Instructor'))
scrollbar.config(command=fc_lbox.yview)
fc_lbox.config(yscrollcommand=scrollbar.set)

scrollbar1 = Scrollbar(fc_frame, orient=VERTICAL)
time_lbox = treectrl.MultiListbox(fc_frame, yscrollcommand=scrollbar1.set, width=328, bg='white')
time_lbox.config(columns=['Time Preference'])
time_lbox.insert(END, 'Unpreffered Time')
time_lbox.insert(END, 'Maximum Gap Time')
time_lbox.insert(END, 'Minimum Days Off')
time_lbox.insert(END, 'Start Range, End Range')

scrollbar1.config(command=time_lbox.yview)
time_lbox.config(yscrollcommand=scrollbar1.set)
scrollbar1.pack(side="right", fill="y")
time_lbox.pack(side='right', fill=BOTH)
fc_lbox.pack(side='left', fill='both')
scrollbar.pack(side="right", fill="y")




fc_frame.pack(side='top', fill=X)


#buttons to add or delete courses from final list
lu_frame = Frame(screen2, bg='white')
down = Button(lu_frame, text='Delete', command=deselected).pack(side='right', padx=(0,10), pady=(10,10))
up1 = Button(lu_frame, text='Add to Desired', command=selected1).pack(side='right', padx=(0,10), pady=(10,10))
up = Button(lu_frame, text='Add to Must Have', command=selected).pack(side='right', padx=(0,10), pady=(10,10))
lu_frame.pack()

#final list box
label_frame = Frame(screen2)
fc_label = Label(label_frame, text='Must Have')
fc_label.pack(fill=X, side='left', padx=(250,0))

fc_label1 = Label(label_frame, text='Desired')
fc_label1.pack(fill=X, side='right', padx=(0,250))
label_frame.pack(fill=X)

fc_frame1 = Frame(screen2, bg='white')
scrollbar1 = Scrollbar(fc_frame1, orient=VERTICAL)
fc_lbox1 = Listbox(fc_frame1, yscrollcommand=scrollbar1.set, height=10, bg='white')
#fc_lbox1.config(columns=('Course code', 'Section', 'Type', 'Course title', 'Credit hours', 'Day', 'Start time', 'End', 'Classroom', 'CourseID', 'Instructor'))
scrollbar1.config(command=fc_lbox1.yview)
fc_lbox1.config(yscrollcommand=scrollbar1.set)
scrollbar3 = Scrollbar(fc_frame1, orient=VERTICAL)
fc_lbox3 = Listbox(fc_frame1, yscrollcommand=scrollbar3.set, height=10, bg='white')
#fc_lbox3.config(columns=('Course code', 'Section', 'Type', 'Course title', 'Credit hours', 'Day', 'Start time', 'End', 'Classroom', 'CourseID', 'Instructor'))
scrollbar3.config(command=fc_lbox3.yview)
fc_lbox3.config(yscrollcommand=scrollbar3.set)
scrollbar3.pack(side="right", fill="y")
fc_lbox3.pack(side='right', fill=BOTH, expand=1)
fc_lbox1.pack(side='left', fill=BOTH, expand=1)
scrollbar1.pack(side="right", fill="y")
fc_frame1.pack(side='top', fill=BOTH, expand=1)


#buttons to go to next screen scree3:
nexts2_frame = Frame(screen2, bg='white')
nexts2 = Button(nexts2_frame, text='Next', command=lambda: raise_frame(Application1(master=root))).pack(side='right', padx=(0,10), pady=(10,10))
submit = Button(nexts2_frame, text='Submit', command=scr2_to_scr4).pack(side='right', padx=(0,10), pady=(10,10))
backs2 = Button(nexts2_frame, text='Back', command=lambda: raise_frame(Application(master=root))).pack(side='right', padx=(0,10), pady=(10,10))
nexts2_frame.pack(fill=X)

screen2.grid(row=0, column=0, sticky='news')

#Main scrren:
Application(master=root)



########################################## Frontend Over ################################


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
        day = []
        for i in range(5):
            for crs in self.schedule[i]:
                day.append(crs.getInList())
        return day

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




sch = PS[0]

# t1 = timedelta(hours = 10,minutes = 30)
# t2 = timedelta(hours = 21,minutes = 35)
# t3 = timedelta(hours = 0,minutes = 30)

# t4 = (t2-t1)/(t3)
# print(t4)
# print((t1-sch.initialTime)/t3)





#print(listofschedules)


#####################################################################3



root.mainloop()
